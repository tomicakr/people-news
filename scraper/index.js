const { portals } = require('./common.js');
const { scrape } = require('./scraper.js');
const { insertManyPosts, postPresentInDb } = require('./db.js');
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
var cron = require('node-cron');


const url = 'mongodb://localhost:27017';
const dbName = 'newsPosts';
const client = new MongoClient(url, {useNewUrlParser: true, useUnifiedTopology: true});
const cronSpec = '0 0 */4 * * *';

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
                safeToInsert.push({
                    ...post,
                    dateAdded: new Date()
                });
            }
        }
        if (safeToInsert.length) {
            console.log('Inserting bulk...');
            insertManyPosts(db, safeToInsert, callback);
        }
    }
}

client.connect(async function(err) {
    assert.equal(null, err);
    const db = client.db(dbName);
    console.log('<<<<<<<<<<<<SCRAPING>>>>>>>>>>>>>');
    await scrapePosts(db);
    cron.schedule(cronSpec, async () => {
        console.log('<<<<<<<<<<<<SCRAPING>>>>>>>>>>>>> ', cronSpec, ' expired');
        await scrapePosts(db);
    });
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
