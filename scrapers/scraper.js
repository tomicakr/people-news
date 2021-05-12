const puppeteer = require('puppeteer');

const SLEEP_TIME_S = 5;

async function scrape(portal) {
    let browser;
    try {
        browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto(portal.url);
    
        const postLinks = await getFilteredPostLinks(page, portal);
        const postsScraped = [];

        for (let i = 0; i < postLinks.length; i++) {
            const postInfo = await getPostInfo(postLinks[i], page, portal);
            postsScraped.push(postInfo);
            console.log(postInfo.title);

            await page.waitForTimeout(SLEEP_TIME_S*1000);
        }
    } catch (e) {
        console.log(e);
    } finally {
        browser.close();
    }
}

async function getFilteredPostLinks(page, portal) {
    let postLinks = await Promise.all((await page.$x(portal.evalString))
        .map(async item => await (await item.getProperty('href'))
        .jsonValue())); 

    portal.filters.forEach(f => {
        postLinks = postLinks.filter(f);
    });

    if (portal.cleanup) {
        portal.cleanup(postLinks);
    }

    return postLinks;
}

async function getPostInfo(postLink, page, portal) {
    await page.goto(postLink);
    await page.addScriptTag({ content: portal });

    const eval1 = async titleString => document.querySelector(titleString).textContent;
    const eval2 = async contentString => document.querySelector(contentString).textContent;

    const title = await page.evaluate(eval1, portal.titleString);
    const text = await page.evaluate(eval2, portal.contentString);

    return {
        title,
        text,
    }
}

module.exports = {
    scrape
}
