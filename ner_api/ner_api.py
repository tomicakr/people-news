import flask
from flask import request, jsonify
import classla
import sys

classla.download('hr')
nlp = classla.Pipeline('hr', processors='tokenize,ner,lemma')

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

lines = []
with open('./resources/names.txt', 'r', encoding='utf8') as file:
    lines = list(map(lambda x: [*x[:3], int(x[3])], map(lambda x: x.rstrip().split('\t'), file.readlines())))

called = {}
lastCalled = { 'link': '' }

@app.route('/health_check', methods=['GET'])
def health_check():
    return 'running'

@app.route('/nerText', methods=['POST'])
def get_this():
    data = request.get_json()
    doc = nlp(data['text'])
    link = data['link']
    check_for = data['checkFor']

    proc = []
    sentences = map(lambda x: x[0],doc.to_dict())
    for x in sentences:
        proc.extend(x)

    proc = list(map(lambda x: [x['text'], x['lemma'], x['ner']],filter(lambda x: 'B-PER' in x['ner'] or 'I-PER' in x['ner'], proc)))
    name_entities = []
    original_name_entities = []
    in_name = False
    new_ent = ''
    original_ent = ''

    for [original, lemma, decl] in proc:
        filtered_lines = list(sorted(filter(lambda x: x[0] == original, lines), key=lambda x: -x[-1]))
        real = ''
        if len(filtered_lines) != 0:
            real = filtered_lines[0][1]
        else: 
            real = lemma

        if decl == 'B-PER':
            if in_name:
                name_entities.append(new_ent)
                original_name_entities.append(original_ent)
                new_ent = ''
                original_ent = ''
                in_name = False
            in_name = True
            new_ent += real.strip().capitalize()
            original_ent += original.strip().capitalize()
        else:
            new_ent += ' ' + real.strip().capitalize()
            original_ent += ' ' + original.strip().capitalize()

    if new_ent != '':
        name_entities.append(new_ent)
    if original_ent != '':
        original_name_entities.append(original_ent)

    print('Request for {}'.format(link))
    print('Found:', name_entities)
    print('Original found:', original_name_entities)

    result = {}
    is_in = False
    for to_check in check_for:
        result[to_check] = False
        for i in range(len(name_entities)):
            name = name_entities[i]
            original = original_name_entities[i]
            if to_check == name or to_check == original:
                result[to_check] = True
                is_in = True
                break

    name_entities.extend(original_name_entities)
    res = {
        'anyNameInside': is_in,
        'checkedNamedEntities': result,
        'foundNamedEntities': name_entities
    }

    if link in called:
        called[link].update(name_entities)
    else:
        called[link] = set(name_entities)

        if lastCalled['link'] != '' and lastCalled['link'] != link:
            with open('./logs/apiLog.txt', 'a', encoding='utf8') as log:
                log.write(lastCalled['link'] + '\t' + str(called[lastCalled['link']])+'\n')

        lastCalled['link'] = link

    with open('./logs/detailedApiLog.txt', 'a', encoding='utf8') as log:
        s = link + '\t' + str(name_entities)
        log.write(s+'\n')

    return jsonify(res)

app.run()
