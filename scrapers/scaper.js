const puppeteer = require('puppeteer');
const { portals } = require('./common.js');

async function scrape(portal) {
    let browser;
    try {
        browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto(portal.url);
    
        const hrefs = await Promise.all((await page.$x(portal.evalString))
                                    .map(async item => await (await item.getProperty('href'))
                                    .jsonValue()));
        
        let postLinks = hrefs;

        portal.filters.forEach(f => {
            postLinks = postLinks.filter(f);
        });

        console.log(postLinks);
        console.log(`Found ${postLinks.length} post links.`);

        if (portal.cleanup) {
            portal.cleanup(postLinks);
        }

        const postsScraped = [];

        for (let i = 0; i < postLinks.length; i++) {
            const postLink = postLinks[i];

            await page.goto(postLink);
            await page.addScriptTag({ content: portal });

            const eval1 = async titleString => document.querySelector(titleString).textContent;
            const eval2 = async contentString => document.querySelector(contentString).textContent;

            const title = await page.evaluate(eval1, portal.titleString);
            const text = await page.evaluate(eval2, portal.contentString);

            console.log(title);
            postsScraped.push({
                title,
                text
            });
        }
        console.log(postsScraped);
    } catch (e) {
        console.log(e);
    } finally {
        browser.close();
    }
}

Object.values(portals).forEach(portal => {
    console.log(portal.titleString);
    scrape(portal);
});
