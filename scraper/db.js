function insertOnePost(db, post, callback) {
    const collection = db.collection('posts');
    collection.insertOne(post, function(err, result) {
        callback && callback(result);
        err && console.log(err);
    });
}

function insertManyPosts(db, posts, callback) {
    const collection = db.collection('posts');
    collection.insertMany(posts, function(err, result) {
        callback && callback(result);
        err && console.log(err);
    });
}

async function postPresentInDb(db, post) {
    return await db.collection('posts').countDocuments({ hash: post.hash }, { limit: 1 }) === 1;
}

async function getPostWithUrl(db, url) {
    return await db.collection('posts').findOne({ url: url });
}

module.exports = {
    insertOnePost,
    insertManyPosts,
    postPresentInDb,
    getPostWithUrl
}
