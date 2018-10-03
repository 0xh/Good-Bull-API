import mongoose = require('mongoose');
import { prop, Typegoose } from 'typegoose';
mongoose.connect('mongodb://localhost:27017/good-bull')

enum MeetingOptions {
    Lecture = "Lecture",
    Laboratory = "Laboratory",
    Recitation = "Recitation",
    Dissertation = "Dissertation",
    IndependentStudy = "Independent Study",
    Research = "Research"
}

class Meeting extends Typegoose {

    @prop({ required: true })
    location!: string;

    @prop()
    meetingDays!: string;

    @prop()
    startTime!: Date;

    @prop()
    endTime!: Date;

    @prop({ enum: MeetingOptions })
    meetingType!: MeetingOptions;
}

const MeetingModel = new Meeting().getModelForClass(Meeting);

export { Meeting, MeetingModel };