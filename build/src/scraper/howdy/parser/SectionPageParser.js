"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cheerio = require("cheerio");
const HowdyRow_1 = require("./HowdyRow");
class SectionPageParser {
    constructor(html) {
        this.i = 0;
        const $ = cheerio.load(html);
        const trs = $('.pagebodydiv > .datadisplaytable > tbody > tr');
        this.rows = this.mergeTRs(trs);
    }
    mergeTRs(trs) {
        const merged = [];
        trs.each((i, elem) => {
            const $ = cheerio.load(elem);
            if ($(elem).find('th.ddtitle').length > 0) {
                merged.push(elem);
            }
            else if ($(elem).find('td.dddefault').length > 0)
                $(elem).appendTo($(merged[merged.length - 1]));
        });
        return merged.map(elem => new HowdyRow_1.HowdyRow(elem));
    }
    next() {
        if (this.i < this.rows.length) {
            return { done: false, value: this.rows[this.i++] };
        }
        return { done: true, value: this.rows[this.i++] };
    }
    [Symbol.iterator]() {
        return this;
    }
}
exports.SectionPageParser = SectionPageParser;
//# sourceMappingURL=SectionPageParser.js.map