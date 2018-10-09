import { requestDepts, requestTermCodes, scrapeDeptSections } from "./functions";
import { performance } from "perf_hooks";

import { SectionModel, Section } from '../../server/models/courses/Section';
import { MeetingModel } from '../../server/models/courses/Meeting';
import { CourseModel, Course } from '../../server/models/courses/Course';

type UpdateOperation = {
    updateOne: {
        filter: { dept: string, courseNum: string },
        update: {
            $set: { [key: string]: any }
        }
        upsert: boolean
    }
}

function buildBulkOps(termCode: TermCode, dept: string, courseNum: string, sectionData: SectionFields[]) {
    const fieldName = `terms.${termCode}`;
    let updateOp: UpdateOperation = {
        updateOne: {
            filter: { dept, courseNum },
            update: {
                $set: {}
            },
            upsert: true
        }
    }
    updateOp.updateOne.update.$set[fieldName] = sectionData;
    return updateOp;
}
export async function scrapeHowdy() {
    try {
        const termCodes: TermCode[] = await requestTermCodes();
        for (let termCode of termCodes) {
            console.log(`TERM: ${termCode}`)
            const depts = await requestDepts(termCode);
            for (let dept of depts) {
                console.log(dept);
                const sectionData = await scrapeDeptSections(termCode, dept);
                let bulkOps = [];
                for (let courseNum in sectionData) {
                    bulkOps.push(buildBulkOps(termCode, dept, courseNum, sectionData[courseNum]));
                }
                CourseModel.bulkWrite(bulkOps);
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