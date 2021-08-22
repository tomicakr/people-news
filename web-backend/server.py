from flask import request, jsonify, Flask
from pymongo import MongoClient, DESCENDING
from db_models import to_post
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://localhost:27017/')
db = client.newsPosts
posts = db.posts
groups = db.groups
scraper_working = { 'status': True, 'time': time.time() }

@app.route('/post/<title_hash>', methods=['GET'])
def get_post(title_hash):
    db_post = posts.find_one({ 'titleHash': title_hash })
    return jsonify(to_post(db_post))

@app.route('/posts', methods=['GET'])
def get_recent_by_group():
    count = request.args.get('count')
    start = request.args.get('start')
    group_name = request.args.get('group')
    print(group_name)
    if count is None:
        count = 10
    if start is None:
        start = 0
    if group_name is None:
        group_name = 'all'
    count = int(count)
    start = int(start)

    relevant_posts = []

    if group_name == 'all':
        relevant_posts = posts.find().sort('dateAdded', DESCENDING)
    else: 
        group = groups.find_one({ 'groupName': group_name })
        people = group['people']
        relevant_posts = posts.find({"names": {"$in": people}}).sort('dateAdded', DESCENDING)

    relevant_posts = relevant_posts[start:start+count]
    posts_res = []
    for p in relevant_posts:
        posts_res.append(to_post(p))
    return jsonify(posts_res)

@app.route('/groupnames', methods=['GET'])
def get_all_group_names():
    groups_db = groups.find({}, { 'groupName': 1, 'groupFullName': 1 })
    names_return = []
    for g in groups_db:
        names_return.append({'groupName': g['groupName'], 'groupFullName': g['groupFullName']})
    return jsonify(names_return)

@app.route('/add_group', methods=['POST'])
def add_group():
    obj = request.get_json()
    db.groups.insert_one(obj)
    return "success"

@app.route('/health_check', methods=['GET'])
def health_check():
    ner_api = { 'serviceName': 'Ner api', 'status': True }
    scraper = { 'serviceName': 'Scraper', 'status': True }

    if time.time() - scraper_working['time'] > 15:
        scraper['status'] = False

    try:
        ner_api_health = requests.get('http://localhost:5000/health_check').text
    except:     
        ner_api['status'] = False

    return jsonify([ner_api, scraper])

@app.route('/health_check_report', methods=['POST'])
def health_check_report():
    obj = request.get_json() # not needed
    scraper_working['time'] = time.time()
    return 'success'

app.run(port=3000)
