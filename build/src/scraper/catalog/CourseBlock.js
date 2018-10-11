"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class CourseBlock {
    constructor(courseBlock) {
        this.courseBlock = courseBlock;
    }
    get titleFields() {
        const titleText = this.courseBlock.find('.courseblocktitle').text();
        const [dept, courseNum, ...name] = titleText.split(/\s+/g);
        return { dept, courseNum, name: name.join(' ') };
    }
    get hoursFields() {
        const hourText = this.courseBlock.find('.courseblock > .hours').text().trim();
        const [credits, distributionOfHours] = hourText.split(/\s{2,}/g);
        let minCredits = null;
        let maxCredits = null;
        const matches = credits.match(/[0-9\.]+/g);
        if (!matches) {
        }
        else {
            minCredits = Number(matches[0]);
            if (matches.length === 1) {
                maxCredits = Number(matches[0]);
            }
            else if (matches.length === 2) {
                maxCredits = Number(matches[1]);
            }
        }
        return { minCredits, maxCredits, distributionOfHours };
    }
    get descriptionFields() {
        const descriptionText = this.courseBlock.find('.courseblockdesc').text().trim();
        const DESCRIPTION_PATTERN = /(.+?(?= Prerequisites?: | Corequisites?: | Cross Listings?: |$))/g;
        const matches = descriptionText.match(DESCRIPTION_PATTERN);
        const output = { description: null, prereqs: null, coreqs: null, crossListings: null };
        if (!matches) {
            return output;
        }
        output.description = matches[0].trim();
        for (let match of matches.slice(1)) {
            match = match.trim();
            const colonIndex = match.indexOf(':');
            const info = match.slice(colonIndex + 2).trim();
            if (match.startsWith('Prereq')) {
                output.prereqs = info;
            }
            else if (match.startsWith('Coreq')) {
                output.coreqs = info;
            }
            else if (match.startsWith('Cross')) {
                output.crossListings = info;
            }
        }
        return output;
    }
    get fields() {
        const { dept, courseNum, name } = this.titleFields;
        const searchableName = `${dept} ${courseNum}: ${name}`;
        return Object.assign({}, this.titleFields, this.hoursFields, this.descriptionFields, { searchableName });
    }
}
exports.CourseBlock = CourseBlock;
//# sourceMappingURL=CourseBlock.js.map