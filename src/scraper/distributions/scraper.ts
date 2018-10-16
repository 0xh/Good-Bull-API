import cheerio = require('cheerio');
import {get_college_abbrevs} from './requestFunctions';

async function scrape(): Promise<void> {
    try{
        const abbrevs = await get_college_abbrevs();
    }
    catch (err) {
        console.log("Error scraping grade distributions");
    }
} 

scrape().then(() => {
    console.log("Finished scraping grade distribution data");
    process.exit();
})