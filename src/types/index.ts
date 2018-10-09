type TermCode = number;
type CRN = number;
type SectionFields = {
    dept: string;
    courseNum: string;
    sectionNum: string;
    name: string;
    crn: CRN
    honors: boolean;
    sptp: boolean;
}

type InstructorName = string;

type HoursSinceMidnight = number;

type MeetingFields = {
    type: string
    startTime: HoursSinceMidnight | null
    endTime: HoursSinceMidnight | null
    daysStr: string
    building: string
};