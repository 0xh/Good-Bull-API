import rp = require('request-promise');
import cheerio = require('cheerio');
import { StringCounter } from './Counter';
import { Meeting } from '../../server/models/courses/Meeting';
import { Section } from '../../server/models/courses/Section';

export async function requestTermCodes(retryDepth: number = 0): Promise<TermCode[]> {
    try {
        const TERM_CODE_URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched';
        const html = await rp(TERM_CODE_URL);
        const $ = cheerio.load(html);
        const options = $('select[name=p_term] > option');
        let values: TermCode[] = []
        options.each((i, elem) => {
            if (i == 0) {
                return;
            }
            const value = parseInt(elem.attribs['value'])
            values.push(value)
        })
        return values;
    } catch (err)   {
        if (retryDepth < 5) {
            return requestTermCodes(retryDepth + 1);
        }
        return [];
    }
}

export async function requestDepts(termCode: TermCode, retryDepth: number = 0): Promise<string[]> {
    try {
        const DEPT_LIST_URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckgens.p_proc_term_date'
        const FORM_DATA = {
            'p_calling_proc': 'bwckschd.p_disp_dyn_sched',
            'p_term': termCode
        }
        const html = await rp.post(DEPT_LIST_URL, { formData: FORM_DATA })
        const $ = cheerio.load(html)
        const options = $('select[name=sel_subj] > option')
        let values: string[] = []
        options.each((_, elem) => {
            values.push(elem.attribs['value'])
        })
        return values
    } catch (err) {
        console.error(termCode, err.message, retryDepth)
        if (retryDepth < 5) {
            return requestDepts(termCode, retryDepth + 1)
        }
        return [];
    }
}

function mergeTRs(trs: Cheerio): CheerioElement[] {
    let merged: CheerioElement[] = [];
    trs.each(function (i, elem) {
        const $ = cheerio.load(elem)
        if ($(elem).find('th.ddtitle').length > 0) {
            merged.push(elem);
        }
        else if ($(elem).find('td.dddefault').length > 0)
            $(elem).appendTo($(merged[merged.length - 1]));
    });
    return merged;
}


function parseTable(datadisplaytable: Cheerio): string[][] {
    const trs = datadisplaytable.find('tr');
    let meetings: string[][] = []
    trs.each((i, tr) => {
        if (i == 0) {
            return;
        }
        let newMeeting: string[] = [];
        const $ = cheerio.load(tr)
        $(tr).find('td').each((i, elem) => {
            let text = $(elem).text().replace(/\s+/g, ' ')
            newMeeting.push(text.replace(/\(P\)/g, '').trim())
        })
        meetings.push(newMeeting);
    })
    return meetings;
}

function convertTime(timeString: string): HoursSinceMidnight {
    let [hrStr, minStr, amPmStr] = timeString.trim().split(/[: ]/g)
    let hrs = parseInt(hrStr);
    let min = parseInt(minStr);
    if (amPmStr.toLowerCase() === 'pm' && hrs != 12) {
        hrs += 12;
    }
    return hrs + min / 60;

}

function convertTimeRange(timeRangeString: string): [HoursSinceMidnight | null, HoursSinceMidnight | null] {
    if (timeRangeString === 'TBA') {
        return [null, null]
    }
    let [startTimeStr, endTimeStr] = timeRangeString.split(' - ')
    const startTime = convertTime(startTimeStr)
    const endTime = convertTime(endTimeStr)

    return [startTime, endTime];
}

function convertTable(table: string[][]): MeetingFields[] {
    let converted: MeetingFields[] = []
    for (let [type, timeRange, daysStr, where, ...rest] of table) {
        let days = null;
        if (days !== '') {
            days = daysStr;
        }

        let [startTime, endTime] = convertTimeRange(timeRange);
        converted.push({ type, startTime, endTime, daysStr, building: where })
    }
    return converted;
}

function parseBlock(dddefault: Cheerio): [InstructorName | null, MeetingFields[]] {
    const meetingData = parseTable(dddefault.find('.datadisplaytable'));
    let table = convertTable(meetingData);
    const instructors = meetingData.map(elem => elem[elem.length - 1])
    if (instructors.length === 0) {
        return [null, table];
    }
    let counter: StringCounter = new StringCounter(instructors)
    let [[mostCommonInstructor, _]] = counter.mostCommon(1);
    return [mostCommonInstructor, table];
}

function parseTitle(titleText: string): SectionFields {
    const splitTitle = titleText.match(/\w+/g);
    if (!splitTitle) {
        console.error("No title.");
        throw Error(`Title is weird. ${titleText}`);
    }
    let [crnStr, dept, courseNum, sectionNum] = splitTitle.splice(-4);
    let honors = false;
    let sptp = false;
    const crn = parseInt(crnStr);

    let name = splitTitle;
    if (name[0].includes('HNR')) {
        honors = true;
        name = name.slice(1);
    }
    else if (name[0].includes('SPTP')) {
        sptp = true;
        name = name.slice(1);
    }
    const nameStr = name.join(' ');
    return { dept, courseNum, sectionNum, name: nameStr, crn, honors, sptp };
}

export async function scrapeDeptSections(termCode: number, dept: string, retryDepth: number = 0): Promise<{ [courseNum: string]: SectionFields[] }> {
    const URL = `https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in=${termCode}&sel_subj=${dept}&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=${dept}&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a`;
    try {
        const html = await rp(URL);
        const $ = cheerio.load(html);
        const trs = mergeTRs($('.pagebodydiv > .datadisplaytable > tbody > tr'));
        let courses: { [courseNum: string]: [any] } = {};
        for (let tr of trs) {
            const titleText = $(tr).find('.ddtitle > a').text()
            const { dept, courseNum, sectionNum, name, crn, honors, sptp } = parseTitle(titleText)
            const dddefault = $(tr).find('.dddefault')
            const [mostCommonInstructor, table] = parseBlock(dddefault);
            const courseFields = { dept, courseNum, sectionNum, name, crn, honors, sptp, instructor: mostCommonInstructor, meetings: table }
            if (courseNum in courses) {
                courses[courseNum].push(courseFields)
            } else {
                courses[courseNum] = [courseFields];
            }
        }
        return courses;
    } catch (err) {
        if (retryDepth < 5) {
            return scrapeDeptSections(termCode, dept, retryDepth + 1);
        }
        return {};
    }
}