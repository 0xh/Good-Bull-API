const HONORS = "HNR";
const SPECIAL_TOPICS_ABBR = "SPTP";

const SPECIAL_TOPICS_COURSE_NUMS = new Set(["289", "489", "689"]);

type RowTitleFields = {
  dept: string;
  courseNum: string;
  sectionNum: string;
  name: string;
  crn: number;
  honors: boolean;
  sptp: boolean;
};
function isBetween(x: number, lowerBound: number, upperBound: number) {
  return x >= lowerBound && x < upperBound;
}

export default class HowdyRowTitle {
  private text: string;
  private dept: string;
  private courseNum: string;
  private sectionNum: string;
  private name: string;
  private crn: number;
  private honors: boolean;
  private sptp: boolean;

  private parseAbbreviation(): [number, string, string, string] {
    const splitTitle = this.text.match(/\w+/g);
    if (!splitTitle) {
      throw Error(`Title is weird. Can't parse abbreviation: ${this.text}`);
    }
    const [crnStr, dept, courseNum, sectionNum] = splitTitle.splice(-4);
    return [parseInt(crnStr), dept, courseNum, sectionNum];
  }

  private parseSectionFlags(): [string, boolean, boolean] {
    const splitTitle = this.text.match(/\w+/g);
    if (!splitTitle) {
      throw Error(`Title is weird. Can't parse flags: ${this.text}`);
    }
    let name = splitTitle;
    let honors = false;
    let sptp = false;
    const sectionNum = splitTitle[splitTitle.length - 1];
    try {
      const sectionNumInt = parseInt(sectionNum);
      if (splitTitle[0].includes(HONORS)) {
        honors = true;
        name = name.slice(1);
      } else if (isBetween(sectionNumInt, 200, 300)) {
        honors = true;
      }
    } catch (err) {
      // Don't do anything. section number is non-numeric, no way to
      // tell if honors or not.
    }
    if (splitTitle[0].includes(SPECIAL_TOPICS_ABBR)) {
      sptp = true;
      name = name.slice(1);
    } else if (SPECIAL_TOPICS_COURSE_NUMS.has(sectionNum)) {
      sptp = true;
    }

    return [name.slice(0, -4).join(" "), honors, sptp];
  }

  constructor(titleText: string) {
    this.text = titleText;
    [
      this.crn,
      this.dept,
      this.courseNum,
      this.sectionNum
    ] = this.parseAbbreviation();
    [this.name, this.honors, this.sptp] = this.parseSectionFlags();
  }

  public get fields(): RowTitleFields {
    return {
      dept: this.dept,
      courseNum: this.courseNum,
      sectionNum: this.sectionNum,
      name: this.name,
      crn: this.crn,
      honors: this.honors,
      sptp: this.sptp
    };
  }
}
