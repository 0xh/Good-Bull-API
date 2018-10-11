import {courseModel} from '../../server/models/courses/Course';

import {CourseBlock} from './CourseBlock';
import {requestCatalogDepts, requestCourses} from './requestFunctions';

const UNDERGRADUATE_URL =
    'http://catalog.tamu.edu/undergraduate/course-descriptions/';
const GRADUATE_URL = 'http://catalog.tamu.edu/graduate/course-descriptions/';
const URLS = [UNDERGRADUATE_URL, GRADUATE_URL];

type CourseUpdateOperation = {
  updateOne: {
    filter: {dept: string; courseNum: string}; update: {
      dept: string; courseNum: string; distributionOfHours: string | null;
      description: string | null;
      prereqs: string | null;
      coreqs: string | null;
      crossListings: string | null;
      minCredits: number | null;
      maxCredits: number | null;
      name: string | null;
      searchableName: string;
      $setOnInsert: {terms: {};};
    };
    upsert: boolean;
  };
};

const buildBulkUpdateCourseOp = (updateFields: CourseFields) => {
  return {
    updateOne: {
      filter: {dept: updateFields.dept, courseNum: updateFields.courseNum},
      update: {...updateFields, $setOnInsert: {terms: {}}},
      upsert: true
    }
  };
};

async function scrape(): Promise<void> {
  try {
    for (const url of URLS) {
      const depts = await requestCatalogDepts(url);
      for (const dept of depts) {
        console.log(dept);
        const courseBlocks: CourseBlock[] = await requestCourses(url, dept);
        const bulkOps: CourseUpdateOperation[] = [];
        for (const block of courseBlocks) {
          bulkOps.push(buildBulkUpdateCourseOp(block.fields));
        }
        courseModel.bulkWrite(bulkOps);
      }
    }
  } catch (err) {
    console.error(`Error scraping course catalog.`);
  }
}

scrape().then(() => {
  console.log('Finished scraping courses.');
  process.exit();
})
