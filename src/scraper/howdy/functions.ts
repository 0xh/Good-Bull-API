import rp = require('request-promise');
import cheerio = require('cheerio');
import { request } from 'http';

export async function requestTermCodes(): Promise<number[]> {
    const TERM_CODE_URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched';
    const html = await rp(TERM_CODE_URL);
    const $ = cheerio.load(html);
    const options = $('select[name=p_term] > option');
    let values: number[] = []
    options.each((_, elem) => {
        const value = parseInt(elem.attribs['value'])
        values.push(value)
    })
    return values;
}

export async function requestDepts(termCode: number, retryDepth: number = 0): Promise<string[]> {
    try {
        const DEPT_LIST_URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckgens.p_proc_term_date'
        const FORM_DATA = {
            'p_calling_proc': 'bwckschd.p_disp_dyn_sched',
            'p_term': termCode
        }
        const html = await rp.post(DEPT_LIST_URL, { formData: FORM_DATA })
        const $ = cheerio.load(html)
        const options = $('select[name=sel_subj] > option')
        let values: string[] = []
        options.each((_, elem) => {
            values.push(elem.attribs['value'])
        })
        return values
    } catch (err) {
        console.error(err)
        if (retryDepth < 5) {
            return requestDepts(termCode, retryDepth + 1)
        }
        return [];
    }
}

function mergeTRs(trs: Cheerio): CheerioElement[] {
    let merged: CheerioElement[] = [];
    trs.each(function (i, elem) {
        const $ = cheerio.load(elem)
        if ($(elem).find('th.ddtitle').length > 0) {
            merged.push(elem);
        }
        else if ($(elem).find('td.dddefault').length > 0)
            $(elem).appendTo($(merged[merged.length - 1]));
    });
    return merged;
}

function parseTitle(titleText: string): [string, string, string, string, number, boolean, boolean] {
    const splitTitle = titleText.match(/\w+/g);
    if (!splitTitle) {
        console.error("No title.");
        throw Error(`Title is weird. ${titleText}`);
    }
    let [crnStr, dept, courseNum, sectionNum] = splitTitle.splice(-4);
    let honors = false;
    let sptp = false;
    const crn = parseInt(crnStr);

    let name = splitTitle;
    if (name[0].includes('HNR')) {
        honors = true;
        name = name.slice(1);
    }
    else if (name[0].includes('SPTP')) {
        sptp = true;
        name = name.slice(1);
    }
    const nameStr = name.join(' ');
    return [dept, courseNum, sectionNum, nameStr, crn, honors, sptp];
}

export async function scrapeDeptSections(termCode: number, dept: string, retryDepth: number = 0) {
    try {
        const URL = `https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in=${termCode}&sel_subj=${dept}&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=${dept}&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a`;
        const html = await rp(URL);
        const $ = cheerio.load(html);
        const trs = mergeTRs($('.pagebodydiv > .datadisplaytable > tbody > tr'));
        for (let tr of trs) {
            const titleText = $(tr).find('.ddtitle > a').text()
            const [dept, courseNum, sectionNum, name, crn, honors, sptp] = parseTitle(titleText)
            console.log([dept, courseNum, sectionNum, name, crn, honors, sptp])
        }
    } catch (err) {
        console.error(err)
    }
}

scrapeDeptSections(201831, 'CSCE')