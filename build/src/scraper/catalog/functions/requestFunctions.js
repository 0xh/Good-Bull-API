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
const CourseBlock_1 = require("../CourseBlock");
function deptAbbreviation(linkText) {
    return linkText.split(/\W+/g)[0];
}
function requestCatalogDepts(url) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const html = yield rp(url);
            const $ = cheerio.load(html);
            const linkTexts = [];
            $('#atozindex > ul > li > a').each((_i, elem) => {
                const text = $(elem).text();
                linkTexts.push(deptAbbreviation(text));
            });
            return linkTexts;
        }
        catch (err) {
            console.error('Failed to request term codes. Reason:', JSON.stringify(err, null, 3));
            return [];
        }
    });
}
exports.requestCatalogDepts = requestCatalogDepts;
function requestCourses(url, dept) {
    return __awaiter(this, void 0, void 0, function* () {
        const courseBlocks = [];
        try {
            const html = yield rp(url + dept.toLowerCase());
            const $ = cheerio.load(html);
            $(html).find('.courseblock').each((_i, elem) => {
                courseBlocks.push(new CourseBlock_1.CourseBlock($(elem)));
            });
        }
        catch (err) {
            console.error(`Failed to request courses for ${dept} because:`, JSON.stringify(err, null, 3));
        }
        finally {
            return courseBlocks;
        }
    });
}
exports.requestCourses = requestCourses;
//# sourceMappingURL=requestFunctions.js.map