const { portals } = require('./common.js');
const { scrape } = require('./scaper.js');

(async () => {
    Object.values(portals).forEach(async portal => {
        await scrape(portal);
    });
})();
