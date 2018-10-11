import { Typegoose } from 'typegoose';
import { Document, Model } from 'mongoose';
import { Meeting } from './Meeting';
declare class Section extends Typegoose {
    dept: string;
    courseNum: string;
    name: string;
    crn: number;
    sectionNum: string;
    termCode: number;
    meetings: Meeting[];
}
declare const sectionModel: Model<Document>;
export { Section, sectionModel };
