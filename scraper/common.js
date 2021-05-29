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
            let content = '';
            // for (let i = 0; i < paragraphs.length; i++) {
            //     if (i === 4) break;
            //     const p = await paragraphs[i].getProperty('textContent');
            //     const text = p._remoteObject.value;
            //     console.log(i, text)
            //     content += ' ' + text.trim();
            // }
            
            const p = await paragraphs[2].getProperty('textContent');
            content = p._remoteObject.value;
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
        ]
    },
    index: {
        url: 'https://index.hr/vijesti',
        evalString: '//a[starts-with(@href, "/vijesti/")]',
        titleString: '.title',
        contentString: '.text',
        filters: [
            containsRegex(/clanak/),
            removeDuplicates
        ]
    },
    ictbusiness: {
        url: 'https://www.ictbusiness.info/vijesti/',
        evalString: '//a[starts-with(@href, "https://www.ictbusiness.info/vijesti/")]',
        titleString: '.main-article-block>h2',
        contentString: '#__phlinews',
        filters: [
            removeDuplicates
        ]
    }
}

module.exports = {
    portals
}
