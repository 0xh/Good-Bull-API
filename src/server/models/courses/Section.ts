const mongoose = require('mongoose');
import {arrayProp, prop, Ref, Typegoose} from 'typegoose';
import {Document, Model} from 'mongoose';
mongoose.connect('mongodb://localhost:27017/good-bull');

export class GpaDistribution extends Typegoose {
  @prop() gpa!: number;

  @prop() ABCDFISQUX!: number[];
}

export class Meeting {
  location!: string|null;
  meetingDays!: string|null;
  startTime!: number|null;
  endTime!: number|null;
  meetingType!: string|null;
}

class Section extends Typegoose {
  @prop() dept!: string;

  @prop() courseNum!: string;

  @prop() name!: string;

  @prop({required: true, index: true}) crn!: number;

  @prop({required: true, index: true}) sectionNum!: string;

  @prop({required: true, index: true}) termCode!: number;

  @arrayProp({items: Meeting, _id: false}) meetings!: Meeting[];
}

const sectionModel: Model<Document> = new Section().getModelForClass(Section);

export {Section, sectionModel};
