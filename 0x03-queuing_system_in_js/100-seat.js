import express from "express";
import { promisify } from "util";
import { createQueue } from "kue";
import { createClient } from "redis";

const app = express();
const redisClient = createClient({ name: "reserve_seat" });
const reservationQueue = createQueue();
const INITIAL_SEATS_COUNT = 50;
let isReservationEnabled = false;
const PORT = 1245;

const updateAvailableSeats = async (number) => {
  return promisify(redisClient.SET).bind(redisClient)(
    "available_seats",
    number
  );
};

const fetchCurrentAvailableSeats = async () => {
  return promisify(redisClient.GET).bind(redisClient)("available_seats");
};

app.get("/available_seats", (_, res) => {
  fetchCurrentAvailableSeats()
    .then((numberOfAvailableSeats) => {
      res.json({ numberOfAvailableSeats: numberOfAvailableSeats || "0" });
    })
    .catch((err) => {
      console.error("Error fetching available seats:", err);
      res.status(500).json({ error: "Internal Server Error" });
    });
});

app.get("/reserve_seat", (_req, res) => {
  if (!isReservationEnabled) {
    res.json({ status: "Reservations are blocked" });
    return;
  }
  try {
    const job = reservationQueue.create("reserve_seat");

    job.on("failed", (err) => {
      console.log(
        "Seat reservation job",
        job.id,
        "failed:",
        err.message || err.toString()
      );
    });
    job.on("complete", () => {
      console.log("Seat reservation job", job.id, "completed");
    });
    job.save();
    res.json({ status: "Reservation in process" });
  } catch (error) {
    console.error("Error creating reservation job:", error);
    res.json({ status: "Reservation failed" });
  }
});

app.get("/process", (_req, res) => {
  res.json({ status: "Queue processing" });
  reservationQueue.process("reserve_seat", (_job, done) => {
    fetchCurrentAvailableSeats()
      .then((result) => Number.parseInt(result || 0))
      .then((availableSeats) => {
        isReservationEnabled = availableSeats > 1; // Update reservation status

        if (availableSeats >= 1) {
          updateAvailableSeats(availableSeats - 1)
            .then(() => done())
            .catch((err) => {
              console.error("Error updating available seats:", err);
              done(new Error("Failed to update seats"));
            });
        } else {
          done(new Error("Not enough seats available"));
        }
      })
      .catch((err) => {
        console.error("Error fetching current available seats:", err);
        done(new Error("Failed to fetch current available seats"));
      });
  });
});

const initializeAvailableSeats = async (initialSeatsCount) => {
  return promisify(redisClient.SET).bind(redisClient)(
    "available_seats",
    Number.parseInt(initialSeatsCount)
  );
};

app.listen(PORT, () => {
  initializeAvailableSeats(
    process.env.INITIAL_SEATS_COUNT || INITIAL_SEATS_COUNT
  )
    .then(() => {
      isReservationEnabled = true;
      console.log(`API available on localhost port ${PORT}`);
    })
    .catch((err) => {
      console.error("Error initializing available seats:", err);
    });
});

export default app;
