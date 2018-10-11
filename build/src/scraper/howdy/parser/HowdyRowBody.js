"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const Counter_1 = require("../Counter");
const cheerio = require("cheerio");
function isTBA(str) {
    return str.trim() === 'TBA';
}
function convertTime(timeString) {
    const [hrStr, minStr, amPmStr] = timeString.trim().split(/[: ]/g);
    let hrs = Number(hrStr);
    const min = Number(minStr);
    if (amPmStr.toLowerCase() === 'pm' && hrs !== 12) {
        hrs += 12;
    }
    return hrs + min / 60;
}
const sanitizeProfs = (value, index, array) => value[value.length - 1].split(',')[0].trim();
function convertTimeRange(timeRangeString) {
    if (isTBA(timeRangeString)) {
        return [null, null];
    }
    const [startTimeStr, endTimeStr] = timeRangeString.split(' - ');
    const startTime = convertTime(startTimeStr);
    const endTime = convertTime(endTimeStr);
    return [startTime, endTime];
}
class HowdyRowBody {
    constructor(dddefault) {
        [this.instructor, this.meetings] = this.parseBlock(dddefault);
    }
    parseTable(datadisplaytable) {
        const trs = datadisplaytable.find('tr');
        const rows = [];
        trs.each((i, tr) => {
            if (i === 0) {
                return;
            }
            const row = [];
            const $ = cheerio.load(tr);
            $(tr).find('td').each((i, elem) => {
                const text = $(elem).text().replace(/\s+/g, ' ');
                row.push(text.replace(/\(P\)/g, '').trim());
            });
            rows.push(row);
        });
        return rows;
    }
    convertTable(table) {
        const converted = [];
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
            converted.push({ meetingType: type, startTime, endTime, meetingDays: days, location });
        }
        return converted;
    }
    parseBlock(dddefault) {
        const meetingData = this.parseTable(dddefault.find('.datadisplaytable'));
        const table = this.convertTable(meetingData);
        const instructors = meetingData.map(sanitizeProfs);
        if (instructors.length === 0) {
            return [null, table];
        }
        const counter = new Counter_1.StringCounter(instructors);
        const [[mostCommonInstructor, _]] = counter.mostCommon(1);
        return [mostCommonInstructor, table];
    }
    get fields() {
        return { instructor: this.instructor, meetings: this.meetings };
    }
}
exports.HowdyRowBody = HowdyRowBody;
//# sourceMappingURL=HowdyRowBody.js.map