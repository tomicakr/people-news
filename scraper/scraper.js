const puppeteer = require('puppeteer');
const crypto = require('crypto');
const { containsName } = require('../services/nerService.js');
const { resolveSoa } = require('dns');

const SLEEP_TIME_S = 3;
const checkNames = ['Andrej Plenković'];

async function scrape(portal) {
    let browser;
    try {
        browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto(portal.url);

        const postLinks = await getFilteredPostLinks(page, portal);
        const postsScraped = [];

        for (let i = 0; i < postLinks.length; i++) {
            console.log(`${i+1} of ${postLinks.length} from ${postLinks[i]}`);
            const postInfo = await getPostInfo(postLinks[i], page, portal);
            if (postInfo) {
                const res = await containsName(checkNames, postInfo.text);
                console.log(res);
                for (let i = 0; i < res.length; i++) {
                    const ent = res[i];
                    if (ent.anyNameInside) {
                        console.log('Found, moving to db');
                        postsScraped.push(postInfo);
                        break;
                    }
                }

            }
            await page.waitForTimeout(SLEEP_TIME_S*1000);
        }

        return postsScraped;
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
    try {
        await page.goto(postLink);
        await page.addScriptTag({ content: portal });
    
        const eval1 = async titleString => document.querySelector(titleString).textContent;
        const eval2 = async contentString => document.querySelector(contentString).textContent;
    
        const title = String(await page.evaluate(eval1, portal.titleString));

        let text;
        if (portal.specificTextGetter) {
            text = await portal.specificTextGetter(page);
        } else {
            text = [String(await page.evaluate(eval2, portal.contentString))];
        }
        console.log(text)

        text = text.map((paragraph) => paragraph.replace(/\s+/gm, ' ')); // clean from unnecessary \n and spaces
        return {
            title,
            text,
            url: postLink,
            titleHash: crypto.createHash('md5').update(title).digest('hex'),
            textHash: crypto.createHash('md5').update(text.join()).digest('hex'),
            urlHash: crypto.createHash('md5').update(postLink).digest('hex'),
        }
    } catch(err) {
        console.error(`Error: ${postLink}, ${err}`);
    }

    return null;
}

module.exports = {
    scrape,
    getPostInfo
}
