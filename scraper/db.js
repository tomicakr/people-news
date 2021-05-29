function insertPosts(db, posts, callback) {
    const collection = db.collection('posts');

    collection.insertMany(posts, function(err, result) {
        callback && callback(result);
        err && console.log(err);
    });
}

async function presentInDb(db, post) {
    return await db.collection('posts').countDocuments({ titleHash: post.titleHash }, { limit: 1 }) === 1;
}

async function getDocument(db, url) {
    return await db.collection('posts').findOne({ url: url });
}

module.exports = {
    insertPosts,
    presentInDb,
    getDocument
}
