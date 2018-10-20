import cheerio = require('cheerio');
import rp = require('request-promise');
import fs = require('fs');
const pdfjs = require('pdfjs-dist');
import {sectionModel} from '../../server/models/courses/Section';

type UpdateOperation = {
    updateOne: {
        filter: {$and: 
            [
                {dept: string}, 
                {sectionNum: string}, 
                {courseNum: string}, 
                {termCode: TermCode}
            ] 
        },
        update: {$set: {
            gradeDistribution: GradeDistributionFields
        }},
        upsert: boolean
    }
}

function constructPDFURL(termCode: TermCode, collegeAbbrev: CollegeAbbrev): string {
    //return `http://web-as.tamu.edu/gradereport/PDFReports/${termCode}/grd${termCode}${collegeAbbrev}.pdf`
    return "http://web-as.tamu.edu/gradereport/PDFReports/20171/grd20171DN.pdf";
}

export async function getCollegeAbbrevs(): Promise<string[]>{
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

export async function downloadPDF(termCode: TermCode, collegeAbbrev: CollegeAbbrev): Promise<void>{
    try{
        const PDF_DIR = `./build/src/scraper/distributions/pdf/${termCode}${collegeAbbrev}.pdf`;
        const URL = constructPDFURL(termCode, collegeAbbrev);
        console.log(URL);
        let updateOps: UpdateOperation[] = [];
        const pdf = await pdfjs.getDocument(URL);
        const maxPages = pdf.pdfInfo.numPages;
        for (let i = 1; i < maxPages+1; i++){
            let page = await pdf.getPage(i);
            let txt = await page.getTextContent();
            const parsedText = txt.items.map((s:any) => { return s.str; }).join('');
            const newOps = parsePDF(termCode, parsedText);
            updateOps = [...updateOps, ...newOps];
        }
        sectionModel.bulkWrite(updateOps).then(() => {
            console.log("Finished writing to MongoDB");
        }).catch((err: Error) => {
            console.error(err);
        });
    }
    catch (err){
        console.log(err);
        console.error("Unable to load the resource at the URL")
    }
}

function parsePDF(termCode: TermCode, text: string): UpdateOperation[] {
    try{
        let updateOps: UpdateOperation[] = [];
        let re = /[' ']|[\n]|[-]{2,}/; //Searches for anything wth a space, newline, or more than 1 dash
        let parsed = text.split(re).filter((val: string) => val);
        for (let i = 0; i < parsed.length; i++){
            let part: string = parsed[i];
            console.log(part);
            if (part.match(/[A-Z]{4}-[A-Z0-9]{3,4}-[0-9]{3}/)){ //Searches specifically for lines with courses on them
                const courseInfo: RegExpMatchArray | null = part.match(/[A-Za-z]{4}-[0-9]{3,4}-[0-9]{3}/);
                const gpaMatch: RegExpMatchArray | null = part.match(/[0-9]{1}[.][0-9]{3}/);
                let dept: string;
                let courseNum: string;
                let sectionNum: string;
                let GPA: number = 0;
                let grades: number[] = [];
                if (courseInfo){
                    const courseInfoData: string[] = courseInfo[0].split("-");
                    dept = courseInfoData[0];
                    courseNum = courseInfoData[1];
                    sectionNum = courseInfoData[2];
                    const tamuTermCode: number = Number(String(termCode) + "1");

                    if (gpaMatch){
                        GPA = parseFloat(gpaMatch[0]);

                        ++i;
                        for (let j = 0; j < 5; j++) grades.push(Number(parsed[++i]));
                        ++i;
                        for (let j = 0; j < 5; j++) grades.push(Number(parsed[++i]));
                    }
                    else{
                        for (let j = 0; j < 5; j++){
                            grades.push(Number(parsed[++i]));
                            ++i;
                        }
                        const gpaMatch: RegExpMatchArray | null = parsed[++i].match(/[0-9]{1}[.][0-9]{3}/);
                        if (gpaMatch) GPA = Number(gpaMatch[0]);
                        for (let j = 0; j < 5; j++){
                            grades.push(Number(parsed[++i]));
                        }
                    }
                    updateOps.push({
                        updateOne: {
                            filter: {$and: 
                                [
                                    {dept: dept}, 
                                    {sectionNum: sectionNum},
                                    {courseNum: courseNum}, 
                                    {termCode: tamuTermCode}
                                ] 
                            },
                            update: {$set: {
                                gradeDistribution:{
                                    grades: grades,
                                    GPA: GPA
                                }
                            }},
                            upsert: false
                        }
                    });
                }
            }
        }
        return updateOps;
    }
    catch (err){
        console.log(err);
        return [];
    }
}