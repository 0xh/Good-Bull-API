import { requestDepts, requestTermCodes, scrapeDeptSections } from "./functions";
import { performance } from "perf_hooks";

import { SectionModel, Section } from '../../server/models/courses/Section';
import { CourseModel, Course } from '../../server/models/courses/Course';

type UpdateOperation = {
    updateOne: {
        filter: object,
        update: { [key: string]: any },
        upsert: boolean
    }
}

function buildBulkUpdateOp(filter: object, update: object, upsert: boolean): UpdateOperation {
    return {
        updateOne: {
            filter, update, upsert
        }
    }
}

function courseUpdateBulkOp(termCode: TermCode, dept: string, courseNum: string, sectionData: SectionFields[]): UpdateOperation {
    const fieldName = `terms.${termCode}`;
    let updateOp: UpdateOperation = buildBulkUpdateOp({ dept, courseNum }, { $set: {} }, true);
    updateOp.updateOne.update['$set'][fieldName] = sectionData;
    return updateOp;
}

function sectionUpdateBulkOp(termCode: TermCode, crn: CRN, section: SectionFields): UpdateOperation {
    return buildBulkUpdateOp({ termCode, crn }, section, true);
}


export async function scrapeHowdy(fullScrape = false) {
    try {
        let termCodes: TermCode[] = await requestTermCodes();
        if (fullScrape) {
            termCodes = termCodes.slice(0, 8);
        }
        for (let termCode of termCodes) {
            console.log(`TERM: ${termCode}`)
            const depts = await requestDepts(termCode);
            for (let dept of depts) {
                console.log(dept);
                const sectionData = await scrapeDeptSections(termCode, dept);
                let courseBulkOps: UpdateOperation[] = [];
                let sectionBulkOps: UpdateOperation[] = [];
                for (let courseNum in sectionData) {
                    for (let section of sectionData[courseNum]) {
                        sectionBulkOps.push(sectionUpdateBulkOp(termCode, section.crn, section));
                    }
                    courseBulkOps.push(courseUpdateBulkOp(termCode, dept, courseNum, sectionData[courseNum]));
                }
                if (courseBulkOps.length > 0) {
                    CourseModel.bulkWrite(courseBulkOps);
                }
                if (sectionBulkOps.length > 0) {
                    SectionModel.bulkWrite(sectionBulkOps);
                }
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