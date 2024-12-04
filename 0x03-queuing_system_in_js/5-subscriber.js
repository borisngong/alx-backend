import { createClient } from "redis";

const redisClient = createClient();
const exitMessage = "KILL_SERVER";
const channelName = "holberton school channel";

// Handle connection errors
redisClient.on("error", (error) => {
  console.error("Redis client not connected to the server:", error.toString());
});

// Log when the client connects
redisClient.on("connect", () => {
  console.log("Redis client connected to the server");
});

// Subscribe to the channel
redisClient.subscribe(channelName);

// Listen for messages on the subscribed channel
redisClient.on("message", (receivedChannel, message) => {
  console.log(message);
  if (message === exitMessage) {
    redisClient.unsubscribe(channelName);
    redisClient.quit(); // Close the client connection
  }
});
