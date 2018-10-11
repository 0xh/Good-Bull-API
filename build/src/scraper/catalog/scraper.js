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
const perf_hooks_1 = require("perf_hooks");
const functions_1 = require("./functions");
function scrapeCatalog() {
    return __awaiter(this, void 0, void 0, function* () {
        const UNDERGRADUATE_URL = 'http://catalog.tamu.edu/undergraduate/course-descriptions/';
        const GRADUATE_URL = 'http://catalog.tamu.edu/graduate/course-descriptions/';
        for (const levelUrl of [UNDERGRADUATE_URL, GRADUATE_URL]) {
            const deptAbbrs = yield functions_1.getDepartmentNames(levelUrl);
            for (const dept of deptAbbrs) {
                yield functions_1.scrapeCatalogPage(levelUrl, dept);
                console.log(dept);
            }
        }
    });
}
exports.scrapeCatalog = scrapeCatalog;
const startTime = perf_hooks_1.performance.now();
scrapeCatalog().then(() => {
    console.log(`Finished scraping in ${(perf_hooks_1.performance.now() - startTime) / 1000}s`);
    process.exit();
});
//# sourceMappingURL=scraper.js.map