const puppeteer = require('puppeteer');
const { portals } = require('../../scraper/common.js');
const { getPostInfo } = require('../../scraper/scraper.js');
const { containsName } = require('../../services/nerService.js');
const fs = require('fs');

function getPortalForLink(link) {
    if(link.startsWith('https://www.vecernji.hr')) {
        return 'vecernji';
    } else if (link.startsWith('https://www.jutarnji.hr')) {
        return 'jutarnji';
    } else if (link.startsWith('https://www.jutarnji.hr')) {
        return 'jutarnji';
    } else if (link.startsWith('https://rep.hr')) {
        return 'rep';
    } else if (link.startsWith('https://www.index.hr')) {
        return 'index';
    } else if (link.startsWith('https://www.ictbusiness')) {
        return 'ictbusiness';
    }
}

const SLEEP_TIME_S = 3;


// Tests scraping from a set of links
// Tests NER for those links - nerAPI has to be running
async function scrapeTest(portal) {
    const data = fs.readFileSync('linksForTest.txt', 'utf8');
    const lines = data.split('\n');
    const links = lines.map(line => line.trim());

    let browser;
    try {
        browser = await puppeteer.launch();
        const page = await browser.newPage();

        for (let i = 0; i < links.length; i++) {
            const link = links[i];
            const postInfo = await getPostInfo(link, page, portals[getPortalForLink(link)]);

            if (postInfo) {
                const res = await containsName([], postInfo.text, link);
                console.log(res);
            }

            await page.waitForTimeout(SLEEP_TIME_S*1000);
        }
    } finally {
        browser.close();
    }
}

scrapeTest();
