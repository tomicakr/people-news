const puppeteer = require('puppeteer');

const url = 'https://index.hr/vijesti';

(async () => {
    let browser;
    try {
        browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto(url);
    
        const hrefs = await Promise.all((await page.$x('//a[@class="vijesti-text-hover"]'))
                                    .map(async item => await (await item.getProperty('href'))
                                    .jsonValue()));
        const postLinks = hrefs.filter(href => href.includes('clanak'))
                                .filter((value, index, self) => {
                                    return self.indexOf(value) === index;
                                });

        console.log(`Found ${hrefs.length} post links.`);

        const postsScraped = [];

        for (let i = 0; i < postLinks.length; i++) {
            const postLink = postLinks[i];

            await page.goto(postLink);
            const title = await page.evaluate(() => document.querySelector('.title').textContent);
            const text = await page.evaluate(() => document.querySelector('.text').textContent);

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
