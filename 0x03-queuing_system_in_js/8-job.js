import { Queue } from "kue";
export const createPushNotificationsJobs = (jobs, queue) => {
  if (!(jobs instanceof Array)) {
    throw new Error("Jobs is not an array");
  }

  // Prevent job creation if jobs array is empty
  if (jobs.length === 0) {
    return; // Early return to avoid creating jobs
  }

  for (const jobInfo of jobs) {
    const job = queue.create("push_notification_code_3", jobInfo);

    job
      .on("enqueue", () => {
        console.log("Notification job created:", job.id);
      })
      .on("complete", () => {
        console.log("Notification job", job.id, "completed");
      })
      .on("failed", (err) => {
        console.log(
          "Notification job",
          job.id,
          "failed:",
          err.message || err.toString()
        );
      })
      .on("progress", (progress) => {
        console.log("Notification job", job.id, `${progress}% complete`);
      });

    // Save the job to the queue
    job.save();
  }
};

export default createPushNotificationsJobs;
