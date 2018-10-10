import { Meeting } from "../../../server/models/courses/Meeting";
import { StringCounter } from "../Counter";
import cheerio = require("cheerio");

type RowBodyFields = {
  instructor: string,
  meetings: Meeting[]
}

function isTBA(str: string) {
  return str.trim() === "TBA";
}

function convertTime(timeString: string): HoursSinceMidnight {
  let [hrStr, minStr, amPmStr] = timeString.trim().split(/[: ]/g);
  let hrs = parseInt(hrStr);
  let min = parseInt(minStr);
  if (amPmStr.toLowerCase() === "pm" && hrs != 12) {
    hrs += 12;
  }
  return hrs + min / 60;
}

const sanitizeProfs = (value: string[], index: number, array: string[][]) =>
  value[value.length - 1].split(",")[0].trim();

function convertTimeRange(
  timeRangeString: string
): [HoursSinceMidnight | null, HoursSinceMidnight | null] {
  if (isTBA(timeRangeString)) {
    return [null, null];
  }
  let [startTimeStr, endTimeStr] = timeRangeString.split(" - ");
  const startTime = convertTime(startTimeStr);
  const endTime = convertTime(endTimeStr);

  return [startTime, endTime];
}

export default class HowdyRowBody {
  private instructor: string;
  private meetings: Meeting[];

  constructor(dddefault: Cheerio) {
    [this.instructor, this.meetings] = this.parseBlock(dddefault);
  }

  private parseTable(datadisplaytable: Cheerio): string[][] {
    const trs = datadisplaytable.find("tr");
    let rows: string[][] = [];
    trs.each((i, tr) => {
      if (i == 0) {
        return;
      }
      let row: string[] = [];
      const $ = cheerio.load(tr);
      $(tr)
        .find("td")
        .each((i, elem) => {
          let text = $(elem)
            .text()
            .replace(/\s+/g, " ");
          row.push(text.replace(/\(P\)/g, "").trim());
        });
      rows.push(row);
    });
    return rows;
  }

  private convertTable(table: string[][]): Meeting[] {
    let converted: Meeting[] = [];
    for (let [type, timeRange, daysStr, locationStr, ..._] of table) {
      let days = null;
      if (daysStr !== "") {
        days = daysStr;
      }

      let location = null;
      if (!isTBA(locationStr)) {
          location = locationStr;
      }

      let [startTime, endTime] = convertTimeRange(timeRange);
      converted.push({
        meetingType: type,
        startTime,
        endTime,
        meetingDays: days,
        location
      });
    }
    return converted;
  }

  private parseBlock(dddefault: Cheerio): [string | null, Meeting[]] {
    const meetingData = this.parseTable(dddefault.find(".datadisplaytable"));
    const table = this.convertTable(meetingData);
    const instructors = meetingData.map(sanitizeProfs);
    if (instructors.length === 0) {
      return [null, table];
    }
    let counter: StringCounter = new StringCounter(instructors);
    let [[mostCommonInstructor, _]] = counter.mostCommon(1);

    return [mostCommonInstructor, table];
  }

  public get fields(): RowBodyFields {
    return { instructor: this.instructor, meetings: this.meetings };
  }
}
