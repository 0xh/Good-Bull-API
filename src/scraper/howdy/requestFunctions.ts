import rp = require('request-promise');
import cheerio = require('cheerio');

const TERM_CODE_URL =
    'https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched';
const DEPT_LIST_URL =
    'https://compass-ssb.tamu.edu/pls/PROD/bwckgens.p_proc_term_date';

const TIMEOUT_VALUE = 60 * 1000;  // In millis

export async function requestTermCodes(
    shallow = false, retryDepth = 0): Promise<TermCode[]> {
  const SHALLOW_CUTOFF = 6;
  try {
    const html = await rp(TERM_CODE_URL, {timeout: TIMEOUT_VALUE});
    const $ = cheerio.load(html);
    const options: string[] = [];
    $('.dedefault > select > option').each((i, elem) => {
      options.push(elem.attribs['value']);
    });
    const numericOptions = options.map(value => Number(value));
    if (shallow) {
      return numericOptions.slice(1, SHALLOW_CUTOFF);
    }
    return numericOptions.slice(1);
  } catch (err) {
    console.error(`Error requesting term codes after ${
        retryDepth + 1} attempts because of: ${err.message}`);
    if (retryDepth < 5) {
      return await requestTermCodes(shallow, retryDepth + 1);
    }
    return [];
  }
}

export async function requestDepts(
    termCode: TermCode, retryDepth = 0): Promise<string[]> {
  const FORM_DATA = {
    p_calling_proc: 'bwckschd.p_disp_dyn_sched',
    p_term: termCode
  };
  try {
    const html = await rp.post(
        DEPT_LIST_URL, {formData: FORM_DATA, timeout: TIMEOUT_VALUE});
    const $ = cheerio.load(html);
    const options = $('select[name=sel_subj] > option');
    const values: string[] = [];
    options.each((_, elem) => {
      values.push(elem.attribs['value']);
    });
    return values;
  } catch (err) {
    console.error(`Error requesting departments for term ${termCode} after ${
        retryDepth + 1} attempts because of: ${err.message}`);
    if (retryDepth < 5) {
      return await requestDepts(termCode, retryDepth + 1);
    }
    return [];
  }
}

export async function requestSectionHtml(
    termCode: TermCode, dept: string,
    retryDepth = 0): Promise<string|undefined> {
  const SECTIONS_FOR_DEPT_URL =
      `https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in=${
          termCode}&sel_subj=${
          dept}&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=${
          dept}&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a`;
  try {
    return await rp(SECTIONS_FOR_DEPT_URL, {timeout: TIMEOUT_VALUE});
  } catch (err) {
    console.error(`Error requesting sections for ${dept}-${termCode} after ${
        retryDepth + 1} attempts because of: ${err.message}`);
    if (retryDepth < 5) {
      return await requestSectionHtml(termCode, dept, retryDepth + 1);
    }
    return;
  }
}
