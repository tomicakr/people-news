const { portals } = require('./common.js');
const { scrape } = require('./scraper.js');
const { insertManyPosts, postPresentInDb } = require('./db.js');
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
var cron = require('node-cron');
const axios = require('axios');
const { log } = require('./logging');

const url = 'mongodb://localhost:27017';
const dbName = 'newsPosts';
const client = new MongoClient(url, {useNewUrlParser: true, useUnifiedTopology: true});
const cronSpec = '0 0 */5 * * *';
const cronSpec2 = '*/5 * * * * *';
let currentScraping = null;

async function scrapePosts(db, callback) {
    const ps = Object.values(portals);
    for (let i = 0; i < ps.length; i++) {
        const portal = ps[i];
        const portalPosts = await scrape(portal);
        const safeToInsert = [];
        for (let j = 0; j < portalPosts.length; j++) {
            const post = portalPosts[j];
            const inDb = await postPresentInDb(db, post);
            if (!inDb) {
                console.log(`Will insert: ${post.url}`);
                log(`Will insert: ${post.url}`, 'scraper');
                safeToInsert.push({
                    ...post,
                    dateAdded: new Date()
                });
            }
        }
        if (safeToInsert.length) {
            console.log('Inserting bulk...');
            log('Inserting bulk...', 'scraper');
            insertManyPosts(db, safeToInsert, callback);
        }
    }
}

client.connect(async function(err) {
    assert.equal(null, err);
    const db = client.db(dbName);
    // console.log('<<<<<<<<<<<<SCRAPING>>>>>>>>>>>>>');
    // log('<<<<<<<<<<<<SCRAPING>>>>>>>>>>>>>', 'scraper');
    currentScraping = cron.schedule(cronSpec, async () => {
        console.log('<<<<<<<<<<<<SCRAPING>>>>>>>>>>>>> ', cronSpec, ' expired');
        log('<<<<<<<<<<<<SCRAPING>>>>>>>>>>>>> ' + cronSpec + ' expired', 'scraper');
        await scrapePosts(db);
    });
    cron.schedule(cronSpec2, async () => {
        await axios.post('http://localhost:3000/health_check_report', { serviceName: 'scraper', status: 'running' });
    });
    await scrapePosts(db);
});

if (process.platform === "win32") {
  var rl = require("readline").createInterface({
    input: process.stdin,
    output: process.stdout
  });

  rl.on("SIGINT", function () {
    process.emit("SIGINT");
  });
}

process.on('SIGINT', async function() {
    console.log("Caught interrupt signal");
    console.log('Closing DB connection...');
    client.close(() => {
        console.log('Closed connection, exiting...');
        process.exit();
    });
});
