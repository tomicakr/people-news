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

@app.route('/nerText', methods=['POST'])
def get_this():
    data = request.get_json()
    doc = nlp(data['text'])
    check_for = data['checkFor']
    proc = list(map(lambda x: [x['text'], x['lemma'], x['ner']],filter(lambda x: 'PER' in x['ner'], doc.to_dict()[0][0])))

    name_entities = []
    in_name = False
    new_ent = ''

    for [original, lemma, decl] in proc:
        print(original, lemma, decl)
        filtered_lines = list(sorted(filter(lambda x: x[0] == original, lines), key=lambda x: -x[-1]))
        if len(filtered_lines) == 0:
            continue

        real = filtered_lines[0][1]
        if decl == 'B-PER':
            if in_name:
                name_entities.append(new_ent)
                new_ent = ''
                in_name = False
            in_name = True
            new_ent += real
        else:
            new_ent += ' ' + real
    name_entities.append(new_ent)

    print("Checking if the following name is in the text: ", check_for)
    print("Named entities found in the text: ", name_entities)

    is_in = False
    for name in name_entities:
        if check_for == name:
            is_in = True
            break

    return jsonify({'inside': is_in})

app.run()
