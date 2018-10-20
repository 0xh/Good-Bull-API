type TermCode = number;
type CollegeAbbrev = string;
type HoursSinceMidnight = number;

type CourseFields = {
  dept: string; courseNum: string; distributionOfHours: string | null;
  description: string | null;
  prereqs: string | null;
  coreqs: string | null;
  crossListings: string | null;
  minCredits: number | null;
  maxCredits: number | null;
  name: string | null;
  searchableName: string;
};

type MeetingFields = {
  location: Document|string|null; meetingDays: string | null;
  startTime: number | null;
  endTime: number | null;
  meetingType: string | null;
};

type SectionFields = {
  courseNum: string; name: string; crn: number; sectionNum: string;
  honors: boolean;
  sptp: boolean;
  meetings: MeetingFields[];
  instructor: string | null;
};

type GradeDistributionFields = {
  grades: number[],
  GPA: number,
}

type RowBodyFields = {
  instructor: string|null,
  meetings: MeetingFields[]
};

type RowTitleFields = {
  courseNum: string; sectionNum: string; name: string; crn: number;
  honors: boolean;
  sptp: boolean;
};

type DescriptionFields = {
  description: string|null; prereqs: string | null; coreqs: string | null;
  crossListings: string | null;
};