/// <reference types="cheerio" />
export declare class HowdyRow {
    private title;
    private body;
    constructor(tr: CheerioElement);
    readonly titleFields: {
        dept: string;
        courseNum: string;
        sectionNum: string;
        name: string;
        crn: number;
        honors: boolean;
        sptp: boolean;
    };
    readonly bodyFields: {
        instructor: string | null;
        meetings: Meeting[];
    };
    readonly asSection: SectionFields;
}
