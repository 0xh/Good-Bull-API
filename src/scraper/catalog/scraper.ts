import { getDepartmentNames, scrapeCatalogPage } from "./functions";
import { performance } from "perf_hooks";

export async function scrapeCatalog() {
    const UNDERGRADUATE_URL = 'http://catalog.tamu.edu/undergraduate/course-descriptions/';
    const GRADUATE_URL = 'http://catalog.tamu.edu/graduate/course-descriptions/';

    for (let levelUrl of [UNDERGRADUATE_URL, GRADUATE_URL]) {
        const deptAbbrs = await getDepartmentNames(levelUrl);
        for (let dept of deptAbbrs) {
            await scrapeCatalogPage(levelUrl, dept)
            console.log(dept)
        }
    }
}

const startTime = performance.now()
scrapeCatalog().then(function () {
    console.log(`Finished scraping in ${(performance.now() - startTime) / 1000}s`)
    process.exit()
})