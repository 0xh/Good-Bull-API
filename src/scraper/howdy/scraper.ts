import { requestDepts, requestTermCodes, scrapeDeptSections } from "./functions";
import { performance } from "perf_hooks";

import { SectionModel } from '../../server/models/courses/Section';
import { MeetingModel } from '../../server/models/courses/Meeting';
import { CourseModel } from '../../server/models/courses/Course';

function buildBulkUpdateOps(dept, courseNum, termCode, sectionData) {

}

export async function scrapeHowdy() {
    try {
        const termCodes = await requestTermCodes();
        for (let termCode of termCodes) {
            console.log(`TERM: ${termCode}`)
            const depts = await requestDepts(termCode);
            for (let dept of depts) {
                console.log(dept);
                const sectionData = await scrapeDeptSections(termCode, dept);
                console.log(JSON.stringify(sectionData, null, 3))
                let bulkOps = [];

            }
        }
    } catch (err) {
        throw err;
    }
}

const startTime = performance.now()
scrapeHowdy().then(function () {
    console.log(`Finished scraping Howdy in ${(performance.now() - startTime) / 1000}s`)
    process.exit()
})