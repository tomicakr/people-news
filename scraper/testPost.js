const { containsName } = require('../services/nerService.js');
const { getDocument } = require('./db.js');
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

const url = 'mongodb://localhost:27017';
const dbName = 'newsPosts';
const client = new MongoClient(url, {useNewUrlParser: true, useUnifiedTopology: true});

const postUrl = 'https://www.vecernji.hr/vijesti/vrbanovic-nece-danas-u-remetinac-trazio-je-odgodu-zbog-bolesti-1495383';
async function testThis(db, callback) {
    const doc = await getDocument(db, postUrl);
    const res = await containsName('Lara Samošćanec', doc.title + ' ' + doc.text);
    console.log(res);
}

client.connect(async function(err) {
    assert.equal(null, err);
    const db = client.db(dbName);
    await testThis(db);
    console.log('Closing connection...');
    client.close();
});
