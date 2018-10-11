"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const cheerio = require("cheerio");
const rp = require("request-promise");
const Course_1 = require("../../server/models/courses/Course");
function getDepartmentNames(levelUrl) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const html = yield rp(levelUrl);
            const $ = cheerio.load(html);
            const deptAbbrs = [];
            $('#atozindex > ul > li > a').each((i, elem) => {
                const elemText = $(elem).text();
                let deptAbbr = elemText.slice(0, elemText.indexOf('-'));
                if (!elemText.includes('-')) {
                    deptAbbr = elemText.slice(0, 4);
                }
                deptAbbrs.push(deptAbbr.trim());
            });
            return deptAbbrs;
        }
        catch (err) {
            throw err;
        }
    });
}
exports.getDepartmentNames = getDepartmentNames;
const CROSSREFERENCE_PATTERN = /\/\w{3,4}\s[\d\w]{3,4}/g;
function removeCrossReference(courseTitle) {
    if (courseTitle.includes('/')) {
        courseTitle = courseTitle.replace(CROSSREFERENCE_PATTERN, '');
    }
    return courseTitle;
}
function scrapeTitle(courseBlock) {
    const $ = cheerio.load(courseBlock);
    let title = $('.courseblocktitle').text();
    title = removeCrossReference(title);
    const [dept, courseNum, ...name] = title.split(/\s/g);
    return [dept, courseNum, name.join(' ')];
}
function scrapeHours(courseBlock) {
    const $ = cheerio.load(courseBlock);
    const hourText = $('.hours').text().trim();
    const MANY_WHITESPACE = /\s{2,}/g;
    const [credits, ...distribution] = hourText.replace(MANY_WHITESPACE, '\n').split('\n');
    const hourMatches = credits.match(/(\d+(\.\d+)?)/g);
    const joinedDist = distribution.join(' ');
    if (!hourMatches) {
        return [null, null, joinedDist];
    }
    if (hourMatches.length === 1) {
        const creditHours = Number(hourMatches[0]);
        return [creditHours, creditHours, joinedDist];
    }
    const [minCredits, maxCredits] = hourMatches.map(elem => Number(elem));
    return [minCredits, maxCredits, joinedDist];
}
function scrapeDescription(courseBlock) {
    const $ = cheerio.load(courseBlock);
    const hourText = $('.courseblockdesc').text().trim();
    const DESCRIPTION_PATTERN = /(.+?(?= Prerequisites?: | Corequisites?: | Cross Listings?: |$))/g;
    const matches = hourText.match(DESCRIPTION_PATTERN);
    if (!matches) {
        return [null, null, null, null];
    }
    const description = matches[0].trim();
    if (matches.length === 1) {
        return [description, null, null, null];
    }
    let prereqs = null;
    let coreqs = null;
    let crosslistings = null;
    for (let match of matches.slice(1)) {
        match = match.trim();
        const colonIndex = match.indexOf(':');
        const info = match.slice(colonIndex + 2).trim();
        if (match.startsWith('Prereq')) {
            prereqs = info;
        }
        else if (match.startsWith('Coreq')) {
            coreqs = info;
        }
        else if (match.startsWith('Cross')) {
            crosslistings = info;
        }
    }
    return [description, prereqs, coreqs, crosslistings];
}
function scrapeBlock(courseBlock) {
    const [dept, courseNum, name] = scrapeTitle(courseBlock);
    const [minCredits, maxCredits, distributionOfHours] = scrapeHours(courseBlock);
    const [description, prereqs, coreqs, crossListings] = scrapeDescription(courseBlock);
    let searchableName = `${dept}-${courseNum}`;
    if (name) {
        searchableName += `: ${name}`;
    }
    return {
        dept,
        courseNum,
        name,
        minCredits,
        maxCredits,
        distributionOfHours,
        description,
        prereqs,
        coreqs,
        crossListings,
        searchableName
    };
}
function buildBulkUpdate(courseFields) {
    return {
        updateOne: {
            filter: { dept: courseFields.dept, courseNum: courseFields.courseNum },
            update: Object.assign({}, courseFields, { $setOnInsert: { terms: {} } }),
            upsert: true
        }
    };
}
function scrapeCatalogPage(levelUrl, dept) {
    return __awaiter(this, void 0, void 0, function* () {
        const url = levelUrl + dept.toLowerCase();
        try {
            const html = yield rp(url);
            const $ = cheerio.load(html);
            const bulkOps = [];
            $('.courseblock').each((i, courseBlock) => {
                const courseFields = scrapeBlock(courseBlock);
                bulkOps.push(buildBulkUpdate(courseFields));
            });
            Course_1.courseModel.bulkWrite(bulkOps);
            return html;
        }
        catch (err) {
            throw err;
        }
    });
}
exports.scrapeCatalogPage = scrapeCatalogPage;
//# sourceMappingURL=functions.js.map