import flask
from flask import request, jsonify
import classla
import sys

classla.download('hr')
nlp = classla.Pipeline('hr', processors='tokenize,ner,lemma')

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

lines = []
with open(sys.argv[1], 'r', encoding='utf8') as file:
    lines = list(map(lambda x: [*x[:3], int(x[3])], map(lambda x: x.rstrip().split('\t'), file.readlines())))

called = {}
lastCalled = { 'link': '' }

@app.route('/nerText', methods=['POST'])
def get_this():
    data = request.get_json()
    doc = nlp(data['text'])
    link = data['link']
    check_for = data['checkFor']
    proc = list(map(lambda x: [x['text'], x['lemma'], x['ner']],filter(lambda x: 'B-PER' in x['ner'] or 'I-PER' in x['ner'], doc.to_dict()[0][0])))
    name_entities = []
    in_name = False
    new_ent = ''

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
                new_ent = ''
                in_name = False
            in_name = True
            new_ent += real.strip().capitalize()
        else:
            new_ent += ' ' + real.strip().capitalize()

    if new_ent != '':
        name_entities.append(new_ent)

    print('Request for {}'.format(link))
    print('Found:', name_entities)

    result = {}
    is_in = False
    for to_check in check_for:
        result[to_check] = False
        for name in name_entities:
            if to_check == name:
                result[to_check] = True
                is_in = True
                break

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
            with open('./apiLog.txt', 'a', encoding='utf8') as log:
                log.write(lastCalled['link'] + '\t' + str(called[lastCalled['link']])+'\n')

        lastCalled['link'] = link

    with open('./detailedApiLog.txt', 'a', encoding='utf8') as log:
        s = link + '\t' + str(name_entities)
        log.write(s+'\n')

    return jsonify(res)

app.run()
