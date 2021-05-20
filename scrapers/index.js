const { portals } = require('./common.js');
const { scrape } = require('./scraper.js');
const { insertPosts, presentInDb } = require('./db.js');
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

const url = 'mongodb://localhost:27017';
const dbName = 'newsPosts';
const client = new MongoClient(url, {useNewUrlParser: true, useUnifiedTopology: true});

async function scrapePosts(db, callback) {
    const ps = Object.values(portals);
    for (let i = 0; i < ps.length; i++) {
        const portal = ps[i];
        const portalPosts = await scrape(portal);
        let safeToInsert = [];
        for (let j = 0; j < portalPosts.length; j++) {
            const post = portalPosts[j];
            const inDb = await presentInDb(db, post);
            if (!inDb) {
                safeToInsert.push(post);
            }
        }
        if (safeToInsert.length) {
            insertPosts(db, safeToInsert, callback);
        }
    }
}

client.connect(async function(err) {
    assert.equal(null, err);
    const db = client.db(dbName);
    await scrapePosts(db);
    console.log('Closing connection...');
    client.close();
});
