from flask import request, jsonify, Flask
from pymongo import MongoClient, DESCENDING
from db_models import to_post
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://localhost:27017/')
db = client.newsPosts
posts = db.posts
groups = db.groups

# get one post
@app.route('/post/<title_hash>', methods=['GET'])
def get_post(title_hash):
    db_post = posts.find_one({ 'titleHash': title_hash })
    print(db_post)
    return jsonify(to_post(db_post))

@app.route('/posts', methods=['GET'])
def get_recent_posts():
    count = request.args.get('count')
    start = request.args.get('start')
    if count is None:
        count = 10
    if start is None:
        start = 0
    count = int(count)
    start = int(start)

    all_posts = posts.find().sort('dateAdded', DESCENDING)
    all_posts = all_posts[start:start+count]
    posts_res = []
    for p in all_posts:
        posts_res.append(to_post(p))
    return jsonify(posts_res)

@app.route('/postsgrouped/<group_name>', methods=['GET'])
def get_recent_by_group(group_name):
    count = request.args.get('count')
    start = request.args.get('start')
    if count is None:
        count = 10
    if start is None:
        start = 0
    count = int(count)
    start = int(start)

    group = groups.find_one({ 'groupName': group_name })
    people = group['people']
    relevantPosts = posts.find({"names": {"$in": people}}).sort('dateAdded', DESCENDING)
    relevantPosts = relevantPosts[start:start+count]
    posts_res = []
    for p in relevantPosts:
        posts_res.append(to_post(p))
    return jsonify(posts_res)

@app.route('/add_group', methods=['POST'])
def add_group():
    obj = request.get_json()
    db.groups.insert_one(obj)
    return "success"

app.run(port=3000)
