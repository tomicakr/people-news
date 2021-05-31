const { containsRegex, removeDuplicates } = require('./filters.js');

const portals = {
    vecernji: {
        url: 'http://vecernji.hr/vijesti/',
        evalString: '//a[starts-with(@href, "/vijesti/")]',
        titleString: '.article__title',
        contentString: '.article__body--main_content',
        filters: [
            containsRegex(/-\d+$/),
            removeDuplicates
        ],
        async specificTextGetter(page) {
            const paragraphs = await page.$x('//div[@class="article__body--main_content"]//p');
            let content = [];
            for (let i = 0; i < paragraphs.length; i++) {
                const p = await paragraphs[i].getProperty('textContent');
                const text = p._remoteObject.value && p._remoteObject.value.trim();
                if (text) content.push(text);
            }
            
            return content;
        }
    },
    jutarnji: {
        url: 'http://jutarnji.hr/vijesti/',
        evalString: '//a[starts-with(@href, "/vijesti/")]',
        titleString: '.item__title',
        contentString: '.itemFullText',
        filters: [
            containsRegex(/-\d+$/),
            removeDuplicates
        ],
        cleanup(postLinks) {
            postLinks.shift();
        },
        async specificTextGetter(page) {
            const paragraphs = await page.$x('//div[@class="itemFullText"]//p');
            let content = [];
            for (let i = 0; i < paragraphs.length; i++) {
                const p = await paragraphs[i].getProperty('textContent');
                const text = p._remoteObject.value && p._remoteObject.value.trim();
                if (text) content.push(text);
            }
            
            return content;
        }
    },
    rep: {
        url: 'http://rep.hr/',
        evalString: '//a[starts-with(@href, "/vijesti/")]',
        titleString: '.post-title>h1',
        contentString: '.post-entry',
        filters: [
            containsRegex(/\/\d+\/$/),
            removeDuplicates
        ],
        async specificTextGetter(page) {
            const eval2 = async contentString => document.querySelector(contentString).textContent;
            let content = String(await page.evaluate(eval2,'.post-entry'));
            content = content.split('\n');
            return content.map((p) => p.trim()).filter((p) => p !== '');
        }
    },
    index: {
        url: 'https://index.hr/vijesti',
        evalString: '//a[starts-with(@href, "/vijesti/")]',
        titleString: '.title',
        contentString: '.text',
        filters: [
            containsRegex(/clanak/),
            removeDuplicates
        ],
        async specificTextGetter(page) {
            const paragraphs = await page.$x('//div[@class="text vijesti-link-underline"]//p');
            let content = [];
            for (let i = 0; i < paragraphs.length; i++) {
                const p = await paragraphs[i].getProperty('textContent');
                const text = p._remoteObject.value && p._remoteObject.value.trim();
                if (text) content.push(text);
            }
            
            return content;
        }
    },
    ictbusiness: {
        url: 'https://www.ictbusiness.info/vijesti/',
        evalString: '//a[starts-with(@href, "https://www.ictbusiness.info/vijesti/")]',
        titleString: '.main-article-block>h2',
        contentString: '#__phlinews',
        filters: [
            removeDuplicates
        ],
        async specificTextGetter(page) {
            const paragraphs = await page.$x('//div[@id="__phlinews"]//p');
            let content = [];
            for (let i = 0; i < paragraphs.length; i++) {
                const p = await paragraphs[i].getProperty('textContent');
                const text = p._remoteObject.value && p._remoteObject.value.trim();
                if (text) content.push(text);
            }
            
            return content;
        }
    }
}

module.exports = {
    portals
}
