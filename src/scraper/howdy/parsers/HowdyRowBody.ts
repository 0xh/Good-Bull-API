import {StringCounter} from './Counter';
import cheerio = require('cheerio');

type RowBodyFields = {
  instructor: string|null,
  meetings: Meeting[]
};

function isTBA(str: string) {
  return str.trim() === 'TBA';
}

function convertTime(timeString: string): HoursSinceMidnight {
  const [hrStr, minStr, amPmStr] = timeString.trim().split(/[: ]/g);
  let hrs = Number(hrStr);
  const min = Number(minStr);
  if (amPmStr.toLowerCase() === 'pm' && hrs !== 12) {
    hrs += 12;
  }
  return hrs + min / 60;
}

const sanitizeProfs = (value: string[], index: number, array: string[][]) =>
    value[value.length - 1].split(',')[0].trim();

function convertTimeRange(timeRangeString: string):
    [HoursSinceMidnight|null, HoursSinceMidnight|null] {
  if (isTBA(timeRangeString)) {
    return [null, null];
  }
  const [startTime, endTime] = timeRangeString.split(' - ').map(convertTime);

  return [startTime, endTime];
}

export class HowdyRowBody {
  private dddefault: Cheerio;

  constructor(dddefault: Cheerio) {
    this.dddefault = dddefault;
  }

  private parseTable(datadisplaytable: Cheerio): string[][] {
    const trs = datadisplaytable.find('tr');
    const rows: string[][] = [];
    trs.each((i, tr) => {
      if (i === 0) {
        return;
      }
      const row: string[] = [];
      const $ = cheerio.load(tr);
      $(tr).find('td').each((i, elem) => {
        const text = $(elem).text().replace(/\s+/g, ' ');
        row.push(text.replace(/\(P\)/g, '').trim());
      });
      rows.push(row);
    });
    return rows;
  }

  private convertTable(table: string[][]): Meeting[] {
    const converted: Meeting[] = [];
    for (const [type, timeRange, daysStr, locationStr, ..._] of table) {
      let days = null;
      if (daysStr !== '') {
        days = daysStr;
      }

      let location = null;
      if (!isTBA(locationStr)) {
        location = locationStr;
      }

      const [startTime, endTime] = convertTimeRange(timeRange);
      converted.push(
          {meetingType: type, startTime, endTime, meetingDays: days, location});
    }
    return converted;
  }

  private parseBlock(): {instructor: string|null, meetings: Meeting[]} {
    const meetingData =
        this.parseTable(this.dddefault.find('.datadisplaytable'));
    const table = this.convertTable(meetingData);
    const instructors = meetingData.map(sanitizeProfs);
    if (instructors.length === 0) {
      return {instructor: null, meetings: table};
    }
    const counter: StringCounter = new StringCounter(instructors);
    const [[mostCommonInstructor, _]] = counter.mostCommon(1);

    return {instructor: mostCommonInstructor, meetings: table};
  }

  get fields(): RowBodyFields {
    return this.parseBlock();
  }
}
