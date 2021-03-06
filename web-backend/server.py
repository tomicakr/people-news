from flask import request, jsonify, Flask
from pymongo import MongoClient, DESCENDING
from db_models import to_post
from flask_cors import CORS
import requests
import time
import datetime

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://localhost:27017/')
db = client.newsPosts
posts = db.posts
groups = db.groups
scraper_working = { 'status': True, 'time': time.time() }
logs = {}

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

@app.route('/analytics', methods=['GET'])
def analytics():
    group_name = request.args.get('group')
    days = request.args.get('days')
    from_date = datetime.datetime.now() - datetime.timedelta(days=int(days))
    to_date = datetime.datetime.now()
    group = groups.find_one({ 'groupName': group_name })
    people = group['people']
    print(from_date)
    print(to_date)
    relevant_posts = posts.find({"names": {"$in": people}, "dateAdded": {'$lte': to_date, '$gte': from_date}})
    posts_res = []
    for p in relevant_posts:
        posts_res.append({'names': p['names'], 'dateAdded': p['dateAdded']})
    
    from_group_count = 0
    for post in posts_res:
        names_in_post = post['names']
        post['in_from_group'] = []
        for name_in_post in names_in_post:
            if name_in_post in people:
                post['in_from_group'].append(name_in_post)
            
        from_group_count += len(post['in_from_group'])
    return jsonify({'posts': posts_res, 'fromGroupCount': from_group_count, 'groupName': group['groupFullName']})

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
    database = { 'serviceName': 'Baza', 'status': True }

    if time.time() - scraper_working['time'] > 15:
        scraper['status'] = False

    try:
        ner_api_health = requests.get('http://localhost:5000/health_check').text
    except:     
        ner_api['status'] = False

    try:
        client.server_info()
    except:
        database['status'] = False
    return jsonify([ner_api, scraper, database])

@app.route('/health_check_report', methods=['POST'])
def health_check_report():
    obj = request.get_json() # not needed
    scraper_working['time'] = time.time()
    return 'success'

@app.route('/log', methods=['POST'])
def log():
    obj = request.get_json()
    source = obj['source']
    if source in logs:
        logs[source].append(obj['text'])
    else:
        logs[source] = [obj['text']]
    return 'success'

@app.route('/get_logs', methods=['GET'])
def get_logs():
    source = request.args.get('source')
    if source not in logs:
        return jsonify(['jo?? nema logova za ' + source])
    return jsonify(logs[source])

app.run(port=3000)
