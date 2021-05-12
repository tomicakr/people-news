const { portals } = require('./common.js');
const { scrape } = require('./scraper.js');

(async () => {
    Object.values(portals).forEach(async portal => {
        await scrape(portal);
    });
})();
