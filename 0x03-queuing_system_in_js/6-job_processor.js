import kue from "kue";

// Create a queue named 'push_notification_code'
const queue = kue.createQueue();

// Function to send a notification
function sendNotification(phoneNumber, message) {
  console.log(
    `Sending notification to ${phoneNumber}, with message: ${message}`
  );
}

// Process jobs on the 'push_notification_code' queue
queue.process("push_notification_code", (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message);
  done();
});

// Handle job completion
queue.on("job complete", (id) => {
  console.log(`Notification job ${id} completed`);
});

// Handle job failure
queue.on("job failed", (id, error) => {
  console.log(`Notification job ${id} failed: ${error}`);
});

// Handle job progress
queue.on("job progress", (id, progress) => {
  console.log(`Notification job ${id} ${progress}% complete`);
});
