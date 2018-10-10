type TermCode = number;
type CRN = number;
type SectionFields = {
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

type InstructorName = string;

type HoursSinceMidnight = number;
