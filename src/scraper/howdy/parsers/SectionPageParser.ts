import cheerio = require('cheerio');
import {HowdyRow} from './HowdyRow';

type SectionFields = {
  courseNum: string; name: string; crn: number; sectionNum: string;
  meetings: Meeting[];
  instructor: string | null;
};

export class SectionPageParser implements IterableIterator<HowdyRow> {
  private i = 0;
  private rows: HowdyRow[];

  private mergeTRs(trs: Cheerio): HowdyRow[] {
    const merged: CheerioElement[] = [];
    trs.each((i, elem) => {
      const $ = cheerio.load(elem);
      if ($(elem).find('th.ddtitle').length > 0) {
        merged.push(elem);
      } else if ($(elem).find('td.dddefault').length > 0) {
        $(elem).appendTo($(merged[merged.length - 1]));
      }
    });
    return merged.map(elem => new HowdyRow(elem));
  }

  constructor(html: string) {
    const $ = cheerio.load(html);
    const trs = $('.pagebodydiv > .datadisplaytable > tbody > tr');
    this.rows = this.mergeTRs(trs);
  }
  next(): IteratorResult<HowdyRow> {
    if (this.i < this.rows.length) {
      return {done: false, value: this.rows[this.i++]};
    }
    return {done: true, value: this.rows[this.i++]};
  }
  [Symbol.iterator]() {
    return this;
  }


  get courses(): {[courseNum: string]: SectionFields[]} {
    const courses: {[courseNum: string]: SectionFields[]} = {};
    for (const row of this) {
      if (!(row.fields.courseNum in courses)) {
        courses[row.fields.courseNum] = [row.fields];
      } else {
        courses[row.fields.courseNum].push(row.fields);
      }
    }
    return courses;
  }
}
