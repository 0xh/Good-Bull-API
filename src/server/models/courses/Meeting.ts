import mongoose = require("mongoose");
mongoose.connect("mongodb://localhost:27017/good-bull");

export class Meeting {
  location!: string | null;
  meetingDays!: string | null;
  startTime!: HoursSinceMidnight | null;
  endTime!: HoursSinceMidnight | null;
  meetingType!: string | null;
}
