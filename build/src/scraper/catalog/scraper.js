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
const Course_1 = require("../../server/models/courses/Course");
const requestFunctions_1 = require("./functions/requestFunctions");
const UNDERGRADUATE_URL = 'http://catalog.tamu.edu/undergraduate/course-descriptions/';
const GRADUATE_URL = 'http://catalog.tamu.edu/graduate/course-descriptions/';
const URLS = [UNDERGRADUATE_URL, GRADUATE_URL];
const buildBulkUpdateCourseOp = (updateFields) => {
    return {
        updateOne: {
            filter: { dept: updateFields.dept, courseNum: updateFields.courseNum },
            update: Object.assign({}, updateFields, { $setOnInsert: { terms: {} } }),
            upsert: true
        }
    };
};
function scrape() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            for (const url of URLS) {
                const depts = yield requestFunctions_1.requestCatalogDepts(url);
                for (const dept of depts) {
                    console.log(dept);
                    const courseBlocks = yield requestFunctions_1.requestCourses(url, dept);
                    const bulkOps = [];
                    for (const block of courseBlocks) {
                        bulkOps.push(buildBulkUpdateCourseOp(block.fields));
                    }
                    Course_1.courseModel.bulkWrite(bulkOps);
                }
            }
        }
        catch (err) {
            console.error(`Error scraping course catalog.`);
        }
    });
}
scrape().then(() => {
    console.log('Finished scraping courses successfully!');
    process.exit();
});
//# sourceMappingURL=scraper.js.map