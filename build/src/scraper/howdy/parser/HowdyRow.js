"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const HowdyRowBody_1 = require("./HowdyRowBody");
const HowdyRowTitle_1 = require("./HowdyRowTitle");
const cheerio = require("cheerio");
class HowdyRow {
    constructor(tr) {
        const $ = cheerio.load(tr);
        const titleText = $('.ddtitle > a').text();
        this.title = new HowdyRowTitle_1.HowdyRowTitle(titleText);
        const dddefault = $('.dddefault');
        this.body = new HowdyRowBody_1.HowdyRowBody(dddefault);
    }
    get titleFields() {
        return this.title.fields;
    }
    get bodyFields() {
        return this.body.fields;
    }
    get asSection() {
        return Object.assign({}, this.titleFields, this.bodyFields);
    }
}
exports.HowdyRow = HowdyRow;
//# sourceMappingURL=HowdyRow.js.map