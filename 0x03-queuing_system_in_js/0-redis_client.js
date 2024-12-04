import redis from "redis";

const client = redis.createClient();

client.on("connect", () => {
  console.log("Redis client connected to the server");
});

client.on("error", (err) => {
  console.log("Something went wrong: " + err);
});

process.on("SIGINT", () => {
  client.quit(() => {
    console.log("Redis client disconnected");
    process.exit(0);
  });
});
