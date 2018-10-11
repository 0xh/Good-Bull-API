/// <reference types="cheerio" />
declare type DescriptionFields = {
    description: string | null;
    prereqs: string | null;
    coreqs: string | null;
    crossListings: string | null;
};
export declare class CourseBlock {
    courseBlock: Cheerio;
    constructor(courseBlock: Cheerio);
    readonly titleFields: {
        dept: string;
        courseNum: string;
        name: string | null;
    };
    readonly hoursFields: {
        minCredits: number | null;
        maxCredits: number | null;
        distributionOfHours: string;
    };
    readonly descriptionFields: DescriptionFields;
    readonly fields: CourseFields;
}
export {};
