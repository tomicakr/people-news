const { portals } = require('./common.js');
const { scrape } = require('./scaper.js');

Object.values(portals).forEach(portal => {
    scrape(portal);
});
