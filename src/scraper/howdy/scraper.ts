import {Building, buildingModel} from '../../server/models/Building';
import {courseModel} from '../../server/models/courses/Course';
import {sectionModel} from '../../server/models/courses/Section';

import {SectionPageParser} from './parsers/SectionPageParser';
import {requestDepts, requestSectionHtml, requestTermCodes} from './requestFunctions';

type UpdateOperation = {
  updateOne: {filter: object; update: object; upsert: boolean;};
};

type CourseUpdateOperation = {
  updateOne: {
    filter: {dept: string; courseNum: string;};
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
    updateOne: {filter: {dept, courseNum}, update: {$set: {}}, upsert: true},
  };
  updateOp.updateOne.update.$set[fieldName] = sectionData;
  return updateOp;
}

function sectionUpdateBulkOp(
    dept: string, courseNum: string, termCode: TermCode, crn: number,
    section: SectionFields,
    locations: Array<Document|string|null>): UpdateOperation {
  for (let i = 0; i < section.meetings.length; i++) {
    section.meetings[i].location = locations[i];
  }
  return buildBulkUpdateOp({dept, courseNum, termCode, crn}, section, true);
}

function assembleCourses(sectionData: SectionFields[]):
    {[courseNum: string]: SectionFields[]} {
  const courses: {[courseNum: string]: SectionFields[]} = {};
  for (const row of sectionData) {
    if (!(row.courseNum in courses)) {
      courses[row.courseNum] = [row];
    } else {
      courses[row.courseNum].push(row);
    }
  }
  return courses;
}

async function lookupBuilding(location: Document|
                              null): Promise<Document|string|null> {
  if (!location) {
    return null;
  }
  const searchQuery = {$text: {$search: location}};
  const scoring = {score: {$meta: 'textScore'}};

  const buildingMatches =
      await buildingModel.find(searchQuery, scoring).sort(scoring);
  if (buildingMatches) {
    return buildingMatches[0];
  }
  return null;
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
          // Look up building and use that if possible
          const locations: Array<Document|string|null> = [];
          for (const {location} of section.meetings) {
            const buildingMatch = await lookupBuilding(location);
            locations.push(buildingMatch);
          }
          sectionBulkOps.push(sectionUpdateBulkOp(
              dept, courseNum, termCode, section.crn, section, locations));
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
