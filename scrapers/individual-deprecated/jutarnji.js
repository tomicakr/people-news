const puppeteer = require('puppeteer');

const url = 'http://jutarnji.hr/vijesti/';

(async () => {
    let browser;
    try {
        browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto(url);
    
        const hrefs = await Promise.all((await page.$x('//a[starts-with(@href, "/vijesti/")]'))
                                    .map(async item => await (await item.getProperty('href'))
                                    .jsonValue()));

        const postLinks = hrefs.filter(href => {
                                    return /-\d+$/.test(href);
                                }).filter((value, index, self) => {
                                    return self.indexOf(value) === index;
                                });

        postLinks.shift();

        console.log(postLinks);
        console.log(`Found ${postLinks.length} post links.`);

        const postsScraped = [];

        for (let i = 0; i < postLinks.length; i++) {
            const postLink = postLinks[i];

            await page.goto(postLink);
            const title = await page.evaluate(() => document.querySelector('.item__title').textContent);
            const text = await page.evaluate(() => document.querySelector('.itemFullText').textContent);

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
})();
