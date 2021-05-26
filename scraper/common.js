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
        ]
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
