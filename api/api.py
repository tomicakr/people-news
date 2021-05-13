import flask
from flask import request, jsonify
import classla

classla.download('hr')
nlp = classla.Pipeline('hr', processors='tokenize,ner,lemma')

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

lines = []
with open('../lex/out1.txt', 'r', encoding='utf8') as file:
    lines = list(map(lambda x: [*x[:3], int(x[3])], map(lambda x: x.rstrip().split('\t'), file.readlines())))

@app.route('/nerText', methods=['POST'])
def get_this():
    data = request.get_json()
    doc = nlp(data['text'])
    proc = list(map(lambda x: [x['text'], x['lemma'], x['ner']],filter(lambda x: 'PER' in x['ner'], doc.to_dict()[0][0])))

    return jsonify(proc)

app.run()
