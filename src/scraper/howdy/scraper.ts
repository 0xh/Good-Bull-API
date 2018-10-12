import {courseModel} from '../../server/models/courses/Course';
import {sectionModel} from '../../server/models/courses/Section';

import {SectionPageParser} from './parsers/SectionPageParser';
import {requestDepts, requestSectionHtml, requestTermCodes} from './requestFunctions';

type UpdateOperation = {
  updateOne: {filter: object; update: object; upsert: boolean;};
};

type CourseUpdateOperation = {
  updateOne: {
    filter: {dept: string; termCode: number};
    update: {$set: {[key: string]: SectionFields[];};};
    upsert: boolean;
  };
};

function buildBulkUpdateOp(
    filter: object, update: object, upsert: boolean): UpdateOperation {
  return {updateOne: {filter, update, upsert}};
}

function courseUpdateBulkOp(
    termCode: TermCode, dept: string, courseNum: string,
    sectionData: SectionFields[]): CourseUpdateOperation {
  const fieldName = `terms.${termCode}`;
  const updateOp: CourseUpdateOperation = {
    updateOne: {filter: {dept, termCode}, update: {$set: {}}, upsert: true},
  };
  updateOp.updateOne.update.$set[fieldName] = sectionData;
  return updateOp;
}

function sectionUpdateBulkOp(
    termCode: TermCode, crn: number, section: SectionFields): UpdateOperation {
  return buildBulkUpdateOp({termCode, crn}, section, true);
}

async function scrape(shallow = false) {
  const termCodes = await requestTermCodes(shallow);
  for (const termCode of termCodes) {
    console.log(termCode);
    const depts = await requestDepts(termCode);
    for (const dept of depts) {
      console.log(dept);
      const courseBulkOps: UpdateOperation[] = [];
      const sectionBulkOps: UpdateOperation[] = [];
      const sectionPageHtml = await requestSectionHtml(termCode, dept);
      if (!sectionPageHtml) {
        continue;
      }
      const sectionPageParser = new SectionPageParser(sectionPageHtml);
      const courses = sectionPageParser.courses;
      for (const courseNum of Object.keys(courses)) {
        for (const section of courses[courseNum]) {
          sectionBulkOps.push(
              sectionUpdateBulkOp(termCode, section.crn, section));
        }
        courseBulkOps.push(
            courseUpdateBulkOp(termCode, dept, courseNum, courses[courseNum]));
      }
      courseModel.bulkWrite(courseBulkOps);
      sectionModel.bulkWrite(sectionBulkOps);
    }
  }
}

scrape().then(() => {
  console.log('Scraped successfully.');
  process.exit();
});
