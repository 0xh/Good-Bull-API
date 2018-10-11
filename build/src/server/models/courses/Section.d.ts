/// <reference types="mongoose" />
import { Ref, Typegoose } from 'typegoose';
declare class GpaDistribution extends Typegoose {
    gpa: number;
    ABCDFISQUX: number[];
}
declare class Section extends Typegoose {
    dept: string;
    courseNum: string;
    name: string;
    crn: number;
    sectionNum: string;
    readonly fullName: string;
    termCode: number;
    meetings: Meeting[];
    gpaDistribution?: Ref<GpaDistribution>;
}
declare const sectionModel: import("mongoose").Model<import("typegoose").InstanceType<Section>> & Section & typeof Section;
export { Section, sectionModel };
