import cheerio = require('cheerio');
import {downloadPDF, getCollegeAbbrevs} from './requestFunctions';

function*
    termCodeMaker(
        startYear: number, startSemester: number, endYear: number,
        endSemester: number) {
  while (startYear < endYear ||
         (startYear <= endYear && startSemester <= endSemester)) {
    yield Number(`${startYear}${startSemester++}`);
    if (startSemester === 4) {
      startSemester = 1;
      startYear++;
    }
  }
}

async function scrape(): Promise<void> {
  try {
    const abbrevs = await getCollegeAbbrevs();
    const currYear = new Date().getFullYear();
    for (const termCode of termCodeMaker(2011, 3, currYear, 3)) {
      for (const abbrev of abbrevs) {
        await downloadPDF(termCode, abbrev);
      }
    }
  } catch (err) {
    console.log('Error scraping grade distributions');
  }
}

scrape().then(() => {
  console.log('Finished scraping grade distribution data');
  process.exit();
});