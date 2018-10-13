import { courseModel } from '../../server/models/courses/Course';
import { sectionModel } from '../../server/models/courses/Section';

import { SectionPageParser } from './parsers/SectionPageParser';
import { requestDepts, requestSectionHtml, requestTermCodes } from './requestFunctions';

type UpdateOperation = {
  updateOne: { filter: object; update: object; upsert: boolean; };
};

type CourseUpdateOperation = {
  updateOne: {
    filter: { dept: string; courseNum: string; };
    update: { $set: { [key: string]: SectionFields[]; }; };
    upsert: boolean;
  };
};

function buildBulkUpdateOp(
  filter: object, update: object, upsert: boolean): UpdateOperation {
  return { updateOne: { filter, update, upsert } };
}

function courseUpdateBulkOp(
  termCode: TermCode, dept: string, courseNum: string,
  sectionData: SectionFields[]): CourseUpdateOperation {
  const fieldName = `terms.${termCode}`;
  const updateOp: CourseUpdateOperation = {
    updateOne: { filter: { dept, courseNum }, update: { $set: {} }, upsert: true },
  };
  updateOp.updateOne.update.$set[fieldName] = sectionData;
  return updateOp;
}

function sectionUpdateBulkOp(dept: string, courseNum: string,
  termCode: TermCode, crn: number, section: SectionFields): UpdateOperation {
  return buildBulkUpdateOp({ dept, courseNum, termCode, crn }, section, true);
}

function assembleCourses(sectionData: SectionFields[]): { [courseNum: string]: SectionFields[] } {
  const courses: { [courseNum: string]: SectionFields[] } = {};
  for (const row of sectionData) {
    if (!(row.courseNum in courses)) {
      courses[row.courseNum] = [row];
    } else {
      courses[row.courseNum].push(row);
    }
  }
  return courses;
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
      const courses = assembleCourses(sectionPageParser.sections);
      for (const courseNum of Object.keys(courses)) {
        for (const section of courses[courseNum]) {
          sectionBulkOps.push(
            sectionUpdateBulkOp(dept, courseNum, termCode, section.crn, section));
        }
        courseBulkOps.push(
          courseUpdateBulkOp(termCode, dept, courseNum, courses[courseNum]));
      }
      if (courseBulkOps.length > 0) {
        await courseModel.bulkWrite(courseBulkOps);
      }
      if (sectionBulkOps.length > 0) {
        await sectionModel.bulkWrite(sectionBulkOps);
      }
    }
  }
}

scrape().then(() => {
  console.log('Scraped successfully.');
  process.exit();
});
