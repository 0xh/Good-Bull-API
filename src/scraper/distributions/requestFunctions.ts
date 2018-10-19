import cheerio = require('cheerio');
import rp = require('request-promise');
import fs = require('fs');
const extract = require('pdf-text-extract');
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
    return `http://web-as.tamu.edu/gradereport/PDFReports/${termCode}/grd${termCode}${collegeAbbrev}.pdf`
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
        const options = {
            method: "GET",
            encoding: "binary",
            headers: {
                "Content-type": "applcation/pdf"
            }
        }
        const body = await rp(URL, options);
        let writeStream = fs.createWriteStream(PDF_DIR);
        writeStream.write(body, 'binary');
        writeStream.end(); 
    }
    catch (err){
        console.error("Unable to load the resource at the URL")
    }
}

export async function parsePDF(termCode: TermCode, collegeAbbrev: CollegeAbbrev): Promise<void> {
    try{
        let updateOps: UpdateOperation[] = [];
        const PDF_DIR = `./build/src/scraper/distributions/pdf/${termCode}${collegeAbbrev}.pdf`;
        extract(PDF_DIR, function (err: any, pages: any) {
            if (err) return;
            let re = /[' ']|[\n]|[-]{2,}/; //Searches for anything wth a space, newline, or more than 1 dash
            for (let page of pages){
                let parsed = page.split(re).filter((val: string) => val);
                for (let i = 0; i < parsed.length; i++){
                    let part = parsed[i];
                    if (part.match(/[A-Za-z]{4}-[0-9]{3}-[0-9]{3}/)){ //Searches specifically for lines with courses on them
                        const courseInfo = part.split("-");
                        const dept = courseInfo[0];
                        const courseNum = courseInfo[1];
                        const sectionNum = courseInfo[2];
                        const numA = parsed[++i];
                        const numB = parsed[++i];
                        const numC = parsed[++i];
                        const numD = parsed[++i];
                        const numF = parsed[++i];
                        ++i;
                        const GPA = parsed[++i];
                        const numI = parsed[++i];
                        const numS = parsed[++i];
                        const numU = parsed[++i];
                        const numQ = parsed[++i];
                        const numX = parsed[++i];
                        const gradeDistribution = {
                            A: numA,
                            B: numB,
                            C: numC,
                            D: numD,
                            F: numF,
                            GPA: GPA,
                            I: numI,
                            S: numS,
                            U: numU,
                            Q: numQ,
                            X: numX
                        };
                        const tamuTermCode = parseInt(termCode.toString() + "1");
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
                                    gradeDistribution: gradeDistribution
                                }},
                                upsert: false
                            }
                        });
                    }
                }
            }
            if (updateOps.length > 0)
                sectionModel.bulkWrite(updateOps).then(() => {
                    console.log("Finished writing to Mongo");
                }).catch((err: Error) => {
                    console.error(err);
                });
        })
    }
    catch (err){
        console.error("Unable to open the file at the given directory");
    }
}