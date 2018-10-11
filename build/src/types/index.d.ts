declare type TermCode = number;
declare type HoursSinceMidnight = number;
declare type CourseFields = {
    dept: string;
    courseNum: string;
    distributionOfHours: string | null;
    description: string | null;
    prereqs: string | null;
    coreqs: string | null;
    crossListings: string | null;
    minCredits: number | null;
    maxCredits: number | null;
    name: string | null;
    searchableName: string;
};
