import cheerio = require('cheerio');
import rp = require('request-promise');
import fs = require('fs');
import {sectionModel} from '../../server/models/courses/Section';
import {courseModel} from '../../server/models/courses/Course';
const pdfjs = require('pdfjs-dist');

type SectionUpdateOperation = {
  updateOne: {
    filter: {
      $and:
          [
            {dept: string}, {sectionNum: string}, {courseNum: string},
            {termCode: TermCode}
          ]
    },
    update: {$set: {gradeDistribution: GradeDistributionFields}},
    upsert: boolean
  }
};

function constructPDFURL(
    termCode: TermCode, collegeAbbrev: CollegeAbbrev): string {
  return `http://web-as.tamu.edu/gradereport/PDFReports/${termCode}/grd${
      termCode}${collegeAbbrev}.pdf`;
}

export async function getCollegeAbbrevs(): Promise<string[]> {
  try {
    const GRADE_DISTRIBUTION_URL = 'http://web-as.tamu.edu/gradereport/';
    const html = await rp(GRADE_DISTRIBUTION_URL);
    const $ = cheerio.load(html);
    const abbrevs: string[] = [];
    $('#ctl00_plcMain_lstGradCollege > option').each((_i, element) => {
      const text = $(element).val();
      abbrevs.push(text);
    });
    return abbrevs;
  } catch (err) {
    console.error(
        'Failed to get the college abbreviations. Reason: ',
        JSON.stringify(err, null, 3));
    return [];
  }
}

export async function downloadPDF(
    termCode: TermCode, collegeAbbrev: CollegeAbbrev): Promise<void> {
  try {
    const PDF_DIR =
        `./build/src/scraper/distributions/pdf/${termCode}${collegeAbbrev}.pdf`;
    const URL = constructPDFURL(termCode, collegeAbbrev);
    let sectionUpdateOps: SectionUpdateOperation[] = [];
    let coureseUpdateOps: Array<{}> = [];

    const pdf = await pdfjs.getDocument(URL);
    const maxPages = pdf.pdfInfo.numPages;
    for (let i = 1; i < maxPages + 1; i++) {
      const page = await pdf.getPage(i);
      const txt = await page.getTextContent();
      // tslint:disable-next-line:no-any
      const parsedText = txt.items.map((s: any) => s.str).join('');
      const {newSectionUpdateOps, newCourseUpdateOps} =
          await parsePDF(termCode, parsedText);
      sectionUpdateOps = [...sectionUpdateOps, ...newSectionUpdateOps];
      coureseUpdateOps = [...coureseUpdateOps, ...newCourseUpdateOps];
    }
    sectionModel.bulkWrite(sectionUpdateOps)
        .then(() => {
          console.log('Finished writing the section distributions to MongoDB');
        })
        .catch((err: Error) => {
          console.error(err);
        });

    courseModel.bulkWrite(coureseUpdateOps)
        .then(() => {
          console.log('Finished writing the course distributions to MongoDB');
        })
        .catch((err: Error) => {
          console.error('There were no operations specified for this document');
        });
  } catch (err) {
    console.error('Unable to load the resource at the URL');
  }
}

async function parsePDF(termCode: TermCode, text: string): Promise<{
  newSectionUpdateOps: SectionUpdateOperation[],
  newCourseUpdateOps: Array<{}>
}> {
  try {
    let sectionUpdateOps: SectionUpdateOperation[] = [];
    let courseUpdateOps: Array<{}> = [];
    const re = /[' ']|[\n]|[-]{2,}/;  // Searches for anything wth a space,
    // newline, or more than 1 dash
    const parsed = text.split(re).filter((val: string) => val);
    for (let i = 0; i < parsed.length; i++) {
      const part: string = parsed[i];
      const courseInfo: RegExpMatchArray|null =
          part.match(/[A-Za-z]{4}-[0-9]{3,4}-[0-9]{3}/);
      const gpaMatch: RegExpMatchArray|null = part.match(/[0-9]{1}[.][0-9]{3}/);
      let dept: string;
      let courseNum: string;
      let sectionNum: string;
      let GPA = 0;
      const grades: number[] = [];
      const tamuTermCode: number = Number(String(termCode) + '1');

      if (part.match(
              /[A-Z]{4}-[A-Z0-9]{3,4}-[0-9]{3}/)) {  // Searches specifically
        // for lines with courses on
        // them
        if (courseInfo) {
          const courseInfoData: string[] = courseInfo[0].split('-');
          dept = courseInfoData[0];
          courseNum = courseInfoData[1];
          sectionNum = courseInfoData[2];

          if (gpaMatch) {
            GPA = Number(gpaMatch[0]);

            ++i;
            if (isNaN(Number(parsed[i+1]))) i++;
            for (let j = 0; j < 5; j++) {
              grades.push(Number(parsed[++i]));
            }
            ++i;
            for (let j = 0; j < 5; j++) {
              grades.push(Number(parsed[++i]));
            }
          } else {
            for (let j = 0; j < 5; j++) {
              grades.push(Number(parsed[++i]));
              ++i;
            }
            const gpaMatch: RegExpMatchArray|null =
                parsed[++i].match(/[0-9]{1}[.][0-9]{3}/);
            if (gpaMatch) GPA = Number(gpaMatch[0]);
            for (let j = 0; j < 5; j++) {
              grades.push(Number(parsed[++i]));
            }
          }
          const updates = await updateOps(
              grades, GPA, tamuTermCode, dept, sectionNum, courseNum,
              sectionUpdateOps, courseUpdateOps);
          sectionUpdateOps = updates['sectionUpdateOps'];
          courseUpdateOps = updates['courseUpdateOps'];
        }
      }
    }
    return {
      newSectionUpdateOps: sectionUpdateOps,
      newCourseUpdateOps: courseUpdateOps
    };
  } catch (err) {
    console.log(err);
    return {newSectionUpdateOps: [], newCourseUpdateOps: []};
  }
}

async function updateOps(
    grades: number[], GPA: number, tamuTermCode: number, dept: string,
    sectionNum: string, courseNum: string,
    sectionUpdateOps: SectionUpdateOperation[], courseUpdateOps: Array<{}>) {
  // tslint:disable-next-line:no-any
  const courseSetObject: any = {};
  courseSetObject['terms.' + tamuTermCode + '.$[element].gradeDistribution'] = {
    grades,
    GPA
  };
  sectionUpdateOps.push({
    updateOne: {
      filter:
          {$and: [{dept}, {sectionNum}, {courseNum}, {termCode: tamuTermCode}]},
      update: {$set: {gradeDistribution: {grades, GPA}}},
      upsert: false
    }
  });
  const termCodeExists =
      await checkTermCodeExists(dept, courseNum, tamuTermCode);
  if (termCodeExists) {
    courseUpdateOps.push({
      updateOne: {
        filter: {
          $and: [
            {dept},
            {courseNum},
          ]
        },
        update: {$set: courseSetObject},
        arrayFilters: [{'element.sectionNum': sectionNum}]
      }
    });
  }
  return {courseUpdateOps, sectionUpdateOps};
}

async function checkTermCodeExists(
    dept: string, courseNum: string, tamuTermCode: number): Promise<boolean> {
  // tslint:disable-next-line:no-any
  const termsObject: any = {};
  termsObject['terms.' + tamuTermCode] = {'$exists': true};
  return courseModel
      .find(
          {$and: [{dept}, {courseNum}, termsObject]},
          )
      .then((result) => {
        if (result.length === 0) return false;
        return true;
      });
}