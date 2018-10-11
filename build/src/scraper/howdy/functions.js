"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const rp = require("request-promise");
const cheerio = require("cheerio");
const SectionPageParser_1 = require("./parser/SectionPageParser");
const TIMEOUT_DURATION = 30000;
const TERM_CODE_URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched';
const DEPT_LIST_URL = 'https://compass-ssb.tamu.edu/pls/PROD/bwckgens.p_proc_term_date';
function requestTermCodes(retryDepth = 0) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const html = yield rp(TERM_CODE_URL, { timeout: TIMEOUT_DURATION });
            const $ = cheerio.load(html);
            const options = $('select[name=p_term] > option');
            const values = [];
            options.each((i, elem) => {
                if (i === 0) {
                    return;
                }
                const value = Number(elem.attribs['value']);
                values.push(value);
            });
            return values;
        }
        catch (err) {
            if (retryDepth < 5) {
                console.error('requestTermCodes', err.message, retryDepth);
                return requestTermCodes(retryDepth + 1);
            }
            console.error(`Retry depth exceeded in requestTermCodes`);
            return [];
        }
    });
}
exports.requestTermCodes = requestTermCodes;
function requestDepts(termCode, retryDepth = 0) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const FORM_DATA = {
                'p_calling_proc': 'bwckschd.p_disp_dyn_sched',
                'p_term': termCode
            };
            const html = yield rp.post(DEPT_LIST_URL, { formData: FORM_DATA, timeout: TIMEOUT_DURATION });
            const $ = cheerio.load(html);
            const options = $('select[name=sel_subj] > option');
            const values = [];
            options.each((_, elem) => {
                values.push(elem.attribs['value']);
            });
            return values;
        }
        catch (err) {
            console.error(termCode, err.message, retryDepth);
            if (retryDepth < 5) {
                console.error('requestDepts', err.message, retryDepth);
                return requestDepts(termCode, retryDepth + 1);
            }
            console.error(`Retry depth exceeded in requestDepts for ${termCode}`);
            return [];
        }
    });
}
exports.requestDepts = requestDepts;
function scrapeDeptSections(termCode, dept, retryDepth = 0) {
    return __awaiter(this, void 0, void 0, function* () {
        const URL = `https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in=${termCode}&sel_subj=${dept}&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=${dept}&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a`;
        try {
            const html = yield rp(URL, { timeout: TIMEOUT_DURATION });
            const parser = new SectionPageParser_1.SectionPageParser(html);
            const courses = {};
            for (const row of parser) {
                const courseNum = row.asSection.courseNum;
                if (!(courseNum in courses)) {
                    courses[courseNum] = [row.asSection];
                }
                else {
                    courses[courseNum].push(row.asSection);
                }
            }
            return courses;
        }
        catch (err) {
            if (retryDepth < 5) {
                console.error('scrapeDeptSections', termCode, dept, err.message, retryDepth);
                return scrapeDeptSections(termCode, dept, retryDepth + 1);
            }
            console.error(`Retry depth exceeded in scrapeDeptSections for ${dept} - ${termCode}`);
            return {};
        }
    });
}
exports.scrapeDeptSections = scrapeDeptSections;
//# sourceMappingURL=functions.js.map