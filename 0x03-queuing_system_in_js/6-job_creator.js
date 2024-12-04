import kue from "kue";

// Create a queue named 'push_notification_code'
const queue = kue.createQueue();

// Create an object containing the job data
const jobData = {
  phoneNumber: "4153518780",
  message: "This is the code to verify your account",
};

// Create a job with the job data
const job = queue.create("push_notification_code", jobData).save((err) => {
  if (err) {
    console.error("Error creating job:", err);
  } else {
    console.log(`Notification job created: ${job.id}`);
  }
});

job
  .on("complete", () => {
    console.log("Notification job completed");
  })
  .on("failed", (errorMessage) => {
    console.log("Notification job failed:", errorMessage);
  });
