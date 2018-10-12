type TermCode = number;
type HoursSinceMidnight = number;

type Meeting = {
  location: string|null; meetingDays: string | null; startTime: number | null;
  endTime: number | null;
  meetingType: string | null;
};

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

type SectionFields = {
  courseNum: string; name: string; crn: number; sectionNum: string;
  honors: boolean;
  sptp: boolean;
  meetings: Meeting[];
  instructor: string | null;
};