export declare function requestTermCodes(retryDepth?: number): Promise<TermCode[]>;
export declare function requestDepts(termCode: TermCode, retryDepth?: number): Promise<string[]>;
export declare function scrapeDeptSections(termCode: number, dept: string, retryDepth?: number): Promise<{
    [courseNum: string]: SectionFields[];
}>;
