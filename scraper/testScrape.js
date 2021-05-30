const { portals } = require('./common.js');
const { getPostInfo } = require('./scraper.js');
const puppeteer = require('puppeteer');
const { containsName } = require('../services/nerService.js');

const postLink = 'https://www.vecernji.hr/vijesti/vrbanovic-nece-danas-u-remetinac-trazio-je-odgodu-zbog-bolesti-1495383';

async function scrape(portal) {
    let browser;
    try {
        browser = await puppeteer.launch();
        const page = await browser.newPage();
        const postInfo = await getPostInfo(postLink, page, portal);

        if (postInfo) {
            const res = await containsName(['some name', 'some other name'], postInfo.text);
            console.log(res);
        }
    } finally {
        browser.close();
    }
}

scrape(portals.vecernji);
