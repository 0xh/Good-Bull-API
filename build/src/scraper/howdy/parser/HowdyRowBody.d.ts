/// <reference types="cheerio" />
declare type RowBodyFields = {
    instructor: string | null;
    meetings: Meeting[];
};
export declare class HowdyRowBody {
    private instructor;
    private meetings;
    constructor(dddefault: Cheerio);
    private parseTable;
    private convertTable;
    private parseBlock;
    readonly fields: RowBodyFields;
}
export {};
