import flask
from flask import request, jsonify
import classla
import sys

# classla.download('hr')
nlp = classla.Pipeline('hr', processors='tokenize,ner,lemma')

text = 'Damir Vrbanović, koji je u aferi Dinamo, pravomoćno osuđen na tri godine zatvora, danas se trebao javiti na izdržavanje kazne u Remetinec, no to se neće dogoditi. Jer je 13. svibnja zatražio odgodu zbog bolesti. ' 
checkFor = 'Zdravko Mamić'

lines = []
with open(sys.argv[1], 'r', encoding='utf8') as file:
    lines = list(map(lambda x: [*x[:3], int(x[3])], map(lambda x: x.rstrip().split('\t'), file.readlines())))

def get_this():
    doc = nlp(text)
    check_for = checkFor

    name_entities = []
    in_name = False
    new_ent = ''

    proc = list(map(lambda x: [x['text'], x['lemma'], x['ner']],filter(lambda x: 'PER' in x['ner'], doc.to_dict()[0][0])))

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

    print({
        'inside': is_in,
        'found_named_entities': name_entities
        })

    # return jsonify({
    #     'inside': is_in,
    #     'found_named_entities': name_entities
    #     })

get_this()
