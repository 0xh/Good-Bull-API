import rp = require('request-promise');
import cheerio = require('cheerio');
import {CourseBlock} from './CourseBlock';

function deptAbbreviation(linkText: string) {
  return linkText.split(/\W+/g)[0];
}

export async function requestCatalogDepts(url: string): Promise<string[]> {
  try {
    const html = await rp(url);
    const $ = cheerio.load(html);
    const linkTexts: string[] = [];
    $('#atozindex > ul > li > a').each((_i, elem) => {
      const text = $(elem).text();
      linkTexts.push(deptAbbreviation(text));
    });
    return linkTexts;
  } catch (err) {
    console.error(
        'Failed to request term codes. Reason:', JSON.stringify(err, null, 3));
    return [];
  }
}

export async function requestCourses(
    url: string, dept: string): Promise<CourseBlock[]> {
  const courseBlocks: CourseBlock[] = [];
  try {
    const html = await rp(url + dept.toLowerCase());
    const $ = cheerio.load(html);
    $(html).find('.courseblock').each((_i, elem) => {
      courseBlocks.push(new CourseBlock($(elem)));
    });
  } catch (err) {
    console.error(
        `Failed to request courses for ${dept} because:`,
        JSON.stringify(err, null, 3));
  } finally {
    return courseBlocks;
  }
}
