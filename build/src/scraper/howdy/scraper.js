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
const perf_hooks_1 = require("perf_hooks");
const Course_1 = require("../../server/models/courses/Course");
const Section_1 = require("../../server/models/courses/Section");
const functions_1 = require("./functions");
function courseUpdateBulkOp(termCode, dept, courseNum, sectionData) {
    const fieldName = `terms.${termCode}`;
    const setOnInsertOp = { $setOnInsert: {} };
    setOnInsertOp.$setOnInsert[fieldName] = sectionData;
    const bulkOperation = {
        updateOne: {
            filter: { dept, courseNum },
            update: Object.assign({}, sectionData, setOnInsertOp),
            upsert: true
        }
    };
    return bulkOperation;
}
function sectionUpdateBulkOp(termCode, crn, section) {
    return { updateOne: { filter: { termCode, crn }, update: section, upsert: true } };
}
function scrapeHowdy(fullScrape = false) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            let termCodes = yield functions_1.requestTermCodes();
            if (fullScrape) {
                termCodes = termCodes.slice(0, 8);
            }
            for (const termCode of termCodes) {
                console.log(`TERM: ${termCode}`);
                const depts = yield functions_1.requestDepts(termCode);
                for (const dept of depts) {
                    console.log(dept);
                    const sectionData = yield functions_1.scrapeDeptSections(termCode, dept);
                    const courseBulkOps = [];
                    const sectionBulkOps = [];
                    for (const courseNum of Object.keys(sectionData)) {
                        for (const section of sectionData[courseNum]) {
                            sectionBulkOps.push(sectionUpdateBulkOp(termCode, section.crn, section));
                        }
                        courseBulkOps.push(courseUpdateBulkOp(termCode, dept, courseNum, sectionData[courseNum]));
                    }
                    if (courseBulkOps.length > 0) {
                        Course_1.courseModel.bulkWrite(courseBulkOps);
                    }
                    if (sectionBulkOps.length > 0) {
                        Section_1.sectionModel.bulkWrite(sectionBulkOps);
                    }
                }
            }
        }
        catch (err) {
            throw err;
        }
    });
}
exports.scrapeHowdy = scrapeHowdy;
const startTime = perf_hooks_1.performance.now();
scrapeHowdy().then(() => {
    console.log(`Finished scraping Howdy in ${(perf_hooks_1.performance.now() - startTime) / 1000}s`);
    process.exit();
});
//# sourceMappingURL=scraper.js.map