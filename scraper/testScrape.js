const puppeteer = require('puppeteer');
const { portals } = require('./common.js');
const { getPostInfo } = require('./scraper.js');
const { containsName } = require('../services/nerService.js');

const portalToScrape = 'ictbusiness';
const postLink = 'https://www.ictbusiness.info/vijesti/etf-airways-predstavio-prvi-svoj-putnicki-zrakoplov-u-puli-a-najavljen-skori-dolazak-jos-jednog';
const namesList = ['Andrej Plenković', 'Tomislav Tomašević'];

async function scrape(portal) {
    let browser;
    try {
        browser = await puppeteer.launch();
        const page = await browser.newPage();
        const postInfo = await getPostInfo(postLink, page, portal);

        if (postInfo) {
            const res = await containsName(namesList, postInfo.text, postLink);
            console.log(res);
        }
    } finally {
        browser.close();
    }
}

scrape(portals[portalToScrape]);
