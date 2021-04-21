const portals = {
    vecernji: {
        url: 'http://vecernji.hr/vijesti/',
        evalString: '//a[starts-with(@href, "/vijesti/")]',
        titleString: '.article__title',
        contentString: '.article__body--main_content',
        filters: [
            function(href) {
                return /-\d+$/.test(href);
            },
            function uniquifier(value, index, self){
                return self.indexOf(value) === index;
            }
        ]
    }
}

module.exports = {
    portals
}
