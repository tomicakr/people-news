function insertPosts(db, posts, callback) {
    const collection = db.collection('posts');

    collection.insertMany(posts, function(err, result) {
        callback && callback(result);
        err && console.log(err);
    });
}

module.exports = {
    insertPosts
}
