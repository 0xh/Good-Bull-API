const HONORS = 'HNR';
const SPECIAL_TOPICS_ABBR = 'SPTP';

const SPECIAL_TOPICS_COURSE_NUMS = new Set(['289', '489', '689']);

function isBetween(x: number, lowerBound: number, upperBound: number) {
  return x >= lowerBound && x < upperBound;
}

export class HowdyRowTitle {
  private text: string;

  private parseAbbreviation():
      {crn: number, courseNum: string, sectionNum: string} {
    const splitTitle = this.text.match(/\w+/g);
    if (!splitTitle) {
      throw Error(`Title is weird. Can't parse abbreviation: ${this.text}`);
    }
    const [crnStr, dept, courseNum, sectionNum] = splitTitle.splice(-4);
    return {crn: Number(crnStr), courseNum, sectionNum};
  }

  private parseSectionFlags(): {name: string, honors: boolean, sptp: boolean} {
    const splitTitle = this.text.match(/\w+/g);
    if (!splitTitle) {
      throw Error(`Title is weird. Can't parse flags: ${this.text}`);
    }
    let name = splitTitle;
    let honors = false;
    let sptp = false;
    const sectionNum = splitTitle[splitTitle.length - 1];
    try {
      const sectionNumInt = Number(sectionNum);
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

    return {name: name.slice(0, -4).join(' '), honors, sptp};
  }

  constructor(titleText: string) {
    this.text = titleText;
  }

  get fields(): RowTitleFields {
    const {crn, courseNum, sectionNum} = this.parseAbbreviation();
    const {name, honors, sptp} = this.parseSectionFlags();
    return {courseNum, sectionNum, name, crn, honors, sptp};
  }
}
