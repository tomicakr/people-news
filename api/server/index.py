from flask import request, jsonify, Flask
from pymongo import MongoClient
from db_models import to_post
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://localhost:27017/')
db = client.newsPosts
posts = db.posts

# get one post
@app.route('/post/<titlehash>', methods=['GET'])
def get_post(titlehash):
    db_post = posts.find_one({ 'titleHash': titlehash })
    print(db_post)
    return jsonify(to_post(db_post))

@app.route('/posts', methods=['GET'])
def get_recent_posts():
    count = request.args.get('count')
    if count is None:
        count = 10
    count = int(count)

    all_posts = posts.find()
    all_posts = all_posts[:count]
    posts_res = []
    for p in all_posts:
        posts_res.append(to_post(p))
    return jsonify(posts_res)

app.run(port=3000)
