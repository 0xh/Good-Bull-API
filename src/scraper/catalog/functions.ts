import cheerio = require('cheerio');
import rp = require('request-promise');
import { CourseModel } from "../../server/models/courses/Course";

export async function getDepartmentNames(levelUrl: string): Promise<string[]> {
    try {
        let html = await rp(levelUrl);
        const $ = cheerio.load(html);
        let deptAbbrs: string[] = [];
        $('#atozindex > ul > li > a').each(function (i, elem) {
            const elemText = $(elem).text();
            let deptAbbr = elemText.slice(0, elemText.indexOf('-'));
            if (!elemText.includes('-')) {
                deptAbbr = elemText.slice(0, 4);
            }
            deptAbbrs.push(deptAbbr.trim());
        })
        return deptAbbrs;
    } catch (err) {
        throw err;
    }
}

function removeCrossReference(courseTitle: string): string {
    if (courseTitle.includes('/')) {
        courseTitle = courseTitle.replace(/\/\w{3,4}\s[\d\w]{3,4}/g, '')
    }
    return courseTitle
}

function scrapeTitle(courseBlock: CheerioElement): [string, string, string] {
    const $ = cheerio.load(courseBlock)
    let title = $('.courseblocktitle').text()
    title = removeCrossReference(title);
    let [dept, courseNum, ...name] = title.split(/\s/g)
    return [dept, courseNum, name.join(' ')]
}

function scrapeHours(courseBlock: CheerioElement): [number | null, number | null, string] {
    const $ = cheerio.load(courseBlock)
    const hourText = $('.hours').text().trim()

    const MANY_WHITESPACE = /\s{2,}/g
    let [credits, ...distribution] = hourText.replace(MANY_WHITESPACE, '\n').split('\n')
    const hourMatches = credits.match(/(\d+(\.\d+)?)/g)
    let joinedDist = distribution.join(' ')
    if (!hourMatches) {
        return [null, null, joinedDist]
    }
    if (hourMatches.length === 1) {
        const creditHours = parseFloat(hourMatches[0])
        return [creditHours, creditHours, joinedDist]
    }

    const [minCredits, maxCredits] = hourMatches.map(elem => parseFloat(elem))

    return [minCredits, maxCredits, joinedDist]
}

function scrapeDescription(courseBlock: CheerioElement): [string | null, string | null, string | null, string | null] {
    const $ = cheerio.load(courseBlock)
    const hourText = $('.courseblockdesc').text().trim()

    const DESCRIPTION_PATTERN = /(.+?(?= Prerequisites?: | Corequisites?: | Cross Listings?: |$))/g
    let matches = hourText.match(DESCRIPTION_PATTERN)
    if (!matches) {
        return [null, null, null, null]
    }
    const description = matches[0].trim()
    if (matches.length === 1) {
        return [description, null, null, null]
    }

    let prereqs = null;
    let coreqs = null;
    let crosslistings = null;

    for (let match of matches.slice(1)) {
        match = match.trim()
        const colonIndex = match.indexOf(':')
        const info = match.slice(colonIndex + 2).trim()
        if (match.startsWith('Prereq')) {
            prereqs = info
        } else if (match.startsWith('Coreq')) {
            coreqs = info
        } else if (match.startsWith('Cross')) {
            crosslistings = info
        }
    }
    return [description, prereqs, coreqs, crosslistings]
}

function scrapeBlock(courseBlock: CheerioElement) {
    const [dept, courseNum, name] = scrapeTitle(courseBlock);
    const [minCredits, maxCredits, distributionOfHours] = scrapeHours(courseBlock);
    const [description, prereqs, coreqs, crosslistings] = scrapeDescription(courseBlock);
    let scheduleName = `${dept}-${courseNum}`;
    if (name) {
        scheduleName += `: ${name}`;
    }
    return { dept, courseNum, name, minCredits, maxCredits, distributionOfHours, description, prereqs, coreqs, crosslistings, scheduleName };
}

function buildBulkUpdate(courseFields: any): object {
    return {
        updateOne: {
            filter: {
                dept: courseFields['dept'],
                courseNum: courseFields['courseNum']
            },
            update: {
                ...courseFields,
                $setOnInsert: {
                    terms: {}
                }
            },
            upsert: true
        }
    }
}

export async function scrapeCatalogPage(levelUrl: string, dept: string): Promise<any> {
    const url = levelUrl + dept.toLowerCase();
    try {
        let html = await rp(url);
        const $ = cheerio.load(html);
        let bulkOps: object[] = []
        $('.courseblock').each(function (i, courseBlock) {
            const courseFields = scrapeBlock(courseBlock);
            bulkOps.push(buildBulkUpdate(courseFields))
        })
        CourseModel.bulkWrite(bulkOps)
        return html;
    } catch (err) {
        throw err;
    }
}