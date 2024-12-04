import sinon from "sinon";
import { expect } from "chai";
import { createQueue } from "kue";
import createPushNotificationsJobs from "./8-job.js";

describe("createPushNotificationsJobs", () => {
  const consoleSpy = sinon.spy(console);
  const notificationQueue = createQueue({
    name: "push_notification_code_test",
  }); // More descriptive name for the queue

  before(() => {
    notificationQueue.testMode.enter(true);
  });

  after(() => {
    notificationQueue.testMode.clear();
    notificationQueue.testMode.exit();
  });

  afterEach(() => {
    consoleSpy.log.resetHistory();
  });

  it("displays an error message if jobs is not an array", () => {
    expect(
      createPushNotificationsJobs.bind(
        createPushNotificationsJobs,
        {},
        notificationQueue
      )
    ).to.throw("Jobs is not an array");
  });

  it("adds jobs to the queue with the correct type", (done) => {
    expect(notificationQueue.testMode.jobs.length).to.equal(0);
    const jobDataArray = [
      {
        phoneNumber: "44556677889",
        message: "Use the code 1982 to verify your account",
      },
      {
        phoneNumber: "98877665544",
        message: "Use the code 1738 to verify your account",
      },
    ];
    createPushNotificationsJobs(jobDataArray, notificationQueue);
    expect(notificationQueue.testMode.jobs.length).to.equal(2);
    expect(notificationQueue.testMode.jobs[0].data).to.deep.equal(
      jobDataArray[0]
    );
    expect(notificationQueue.testMode.jobs[0].type).to.equal(
      "push_notification_code_3"
    );

    notificationQueue.process("push_notification_code_3", () => {
      expect(
        consoleSpy.log.calledWith(
          "Notification job created:",
          notificationQueue.testMode.jobs[0].id
        )
      ).to.be.true;
      done();
    });
  });

  it("registers the progress event handler for a job", (done) => {
    notificationQueue.testMode.jobs[0].addListener("progress", () => {
      expect(
        consoleSpy.log.calledWith(
          "Notification job",
          notificationQueue.testMode.jobs[0].id,
          "25% complete"
        )
      ).to.be.true;
      done();
    });
    notificationQueue.testMode.jobs[0].emit("progress", 25);
  });

  it("registers the failed event handler for a job", (done) => {
    notificationQueue.testMode.jobs[0].addListener("failed", () => {
      expect(
        consoleSpy.log.calledWith(
          "Notification job",
          notificationQueue.testMode.jobs[0].id,
          "failed:",
          "Failed to send"
        )
      ).to.be.true;
      done();
    });
    notificationQueue.testMode.jobs[0].emit(
      "failed",
      new Error("Failed to send")
    );
  });

  it("registers the complete event handler for a job", (done) => {
    notificationQueue.testMode.jobs[0].addListener("complete", () => {
      expect(
        consoleSpy.log.calledWith(
          "Notification job",
          notificationQueue.testMode.jobs[0].id,
          "completed"
        )
      ).to.be.true;
      done();
    });
    notificationQueue.testMode.jobs[0].emit("complete");
  });
});
