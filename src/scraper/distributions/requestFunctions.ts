import cheerio = require('cheerio');
import rp = require('request-promise');

function constructPDFURL(termCode: TermCode, collegeAbbrev: CollegeAbbrev): string {
    return `http://web-as.tamu.edu/gradereport/PDFReports/${termCode}/grd${termCode}${collegeAbbrev}.pdf`
}

async function getCollegeAbbrevs(): Promise<string[]>{
    try{
        const GRADE_DISTRIBUTION_URL = "http://web-as.tamu.edu/gradereport/";
        const html = await rp(GRADE_DISTRIBUTION_URL);
        const $ = cheerio.load(html);
        const abbrevs: string[] = [];
        $('#ctl00_plcMain_lstGradCollege > option').each((_i, element) => {
            const text = $(element).val();
            abbrevs.push(text);
        });
        return abbrevs;
    }
    catch (err){
        console.error("Failed to get the college abbreviations. Reason: ", JSON.stringify(err, null, 3));
        return [];
    }
}

async function downloadPDF(termCode: TermCode, collegeAbbrev: CollegeAbbrev){
    const URL = constructPDFURL(termCode, collegeAbbrev);
}
