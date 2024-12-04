import redis from "redis";
import { promisify } from "util";

const client = redis.createClient();

client.on("connect", () => {
  console.log("Redis client connected to the server");
});

client.on("error", (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Promisify the hgetall function
const hgetallAsync = promisify(client.hgetall).bind(client);

// Function to create a hash
function createHash() {
  const hashKey = "HolbertonSchools";
  const schools = {
    Portland: 50,
    Seattle: 80,
    NewYork: 20,
    Bogota: 20,
    Cali: 40,
    Paris: 2,
  };

  for (const [city, value] of Object.entries(schools)) {
    client.hset(hashKey, city, value, redis.print);
  }
}

// Function to display the hash
async function displayHash() {
  try {
    const hash = await hgetallAsync("HolbertonSchools");
    console.log(hash);
  } catch (err) {
    console.log(`Error retrieving hash: ${err}`);
  }
}

createHash();
displayHash();

process.on("SIGINT", () => {
  client.quit(() => {
    console.log("Redis client disconnected");
    process.exit(0);
  });
});
