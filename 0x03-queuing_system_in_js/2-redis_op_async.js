import redis from "redis";
import { promisify } from "util";

const client = redis.createClient();

client.on("connect", () => {
  console.log("Redis client connected to the server");
});

client.on("error", (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Promisify the get function
const getAsync = promisify(client.get).bind(client);

// Function to set a new school value
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

// Async function to display the school value
async function displaySchoolValue(schoolName) {
  try {
    const reply = await getAsync(schoolName);
    console.log(`Value for ${schoolName}: ${reply}`);
  } catch (err) {
    console.log(`Error retrieving value for ${schoolName}: ${err}`);
  }
}

displaySchoolValue("Holberton");
setNewSchool("HolbertonSanFrancisco", "100");
displaySchoolValue("HolbertonSanFrancisco");

process.on("SIGINT", () => {
  client.quit(() => {
    console.log("Redis client disconnected");
    process.exit(0);
  });
});
