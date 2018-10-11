declare type TermCode = number;
declare type CRN = number;
declare type SectionFields = {
    dept: string;
    courseNum: string;
    sectionNum: string;
    name: string;
    crn: CRN;
    honors: boolean;
    sptp: boolean;
    instructor: string | null;
    meetings: any;
};
declare type InstructorName = string;
declare type HoursSinceMidnight = number;
declare class Meeting {
    location: string | null;
    meetingDays: string | null;
    startTime: HoursSinceMidnight | null;
    endTime: HoursSinceMidnight | null;
    meetingType: string | null;
}
