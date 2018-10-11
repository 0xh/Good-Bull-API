import mongoose = require('mongoose');
import { prop, Typegoose, staticMethod, ModelType, Ref, index } from 'typegoose';
import { Section } from './Section';

mongoose.connect('mongodb://localhost:27017/good-bull');

@index({ searchableName: 'text' })
export class Course extends Typegoose {
    @prop({ required: true, index: true })
    dept!: string;

    @prop({ required: true, index: true })
    courseNum!: string;

    @prop()
    distributionOfHours!: string | null;

    @prop()
    description!: string | null;

    @prop()
    prereqs!: string | null;

    @prop()
    coreqs!: string | null;

    @prop()
    minCredits!: number | null;

    @prop()
    maxCredits!: number | null;

    @prop()
    name!: string | null;

    @prop()
    get fullName(): string {
        let fullName = `${this.dept}-${this.courseNum}`;
        if (this.name) {
            fullName += `: ${this.name}`;
        }
        return fullName;
    }

    @prop()
    searchableName!: string;

    @prop()
    terms!: {
        [termCode: string]: Array<Ref<Section>>
    };
}

export const CourseModel = new Course().getModelForClass(Course, { existingMongoose: mongoose });