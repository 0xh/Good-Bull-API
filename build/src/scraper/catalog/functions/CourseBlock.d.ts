/// <reference types="cheerio" />
export declare class CourseBlock {
    courseBlock: Cheerio;
    constructor(courseBlock: Cheerio);
    readonly titleFields: [string, string, string | null];
}
