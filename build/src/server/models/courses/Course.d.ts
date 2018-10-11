import mongoose = require('mongoose');
import { Typegoose, Ref } from 'typegoose';
import { Section } from './Section';
declare class Course extends Typegoose {
    dept: string;
    courseNum: string;
    distributionOfHours: string | null;
    description: string | null;
    prereqs: string | null;
    coreqs: string | null;
    minCredits: number | null;
    maxCredits: number | null;
    name: string | null;
    searchableName: string;
    terms?: {
        [termCode: string]: Array<Ref<Section>>;
    };
    crossListings: string | null;
}
declare const courseModel: mongoose.Model<import("typegoose").InstanceType<Course>> & Course & typeof Course;
export { Course, courseModel };
