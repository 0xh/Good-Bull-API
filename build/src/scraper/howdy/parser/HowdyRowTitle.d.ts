declare type RowTitleFields = {
    dept: string;
    courseNum: string;
    sectionNum: string;
    name: string;
    crn: number;
    honors: boolean;
    sptp: boolean;
};
export declare class HowdyRowTitle {
    private text;
    private dept;
    private courseNum;
    private sectionNum;
    private name;
    private crn;
    private honors;
    private sptp;
    private parseAbbreviation;
    private parseSectionFlags;
    constructor(titleText: string);
    readonly fields: RowTitleFields;
}
export {};
