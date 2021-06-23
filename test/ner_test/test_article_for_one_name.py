import flask
from flask import request, jsonify
import classla
import sys

# Tests CLASSLA Ner for a given text

# classla.download('hr')
nlp = classla.Pipeline('hr', processors='tokenize,ner,lemma')

text = 'Te argumentirane osnove za rano pokretanje nautičkog turizma objavili smo 7. travnja u Jutarnjem listu. Bilo je to tjedan dana prije Uskrsa, kada u normalnim okolnostima počinje nautička sezona. Odmah smo dobili široku potporu predstavnika marina i čartera, a povrh svega i odlučujućih faktora - Ministarstva turizma i Hrvatske turističke zajednice. U stvaranju konkretnih uvjeta ključnu ulogu odigralo je Udruženje marina HGK i njezin predsjednik Sean Lisjak, te direktorica Marine Punat Renata Marević, na čiju je inicijativu analitički članak u Jutarnjem o pokretanju nautičkog turizma u uvjetima zaraze koronom preveden na engleski i poslan svim važnim dionicima europskog nautičkog biznisa te Svjetskom nautičkom udruženju ICOMIA. Članak je upućen i Svjetskoj turističkoj organizaciji (UNWTO), koja je gotovo istodobno slične preporuke uputila svim svojim članicama.'
checkFor = 'Zdravko Mamić'

lines = []
with open('./resources/names.txt', 'r', encoding='utf8') as file:
    lines = list(map(lambda x: [*x[:3], int(x[3])], map(lambda x: x.rstrip().split('\t'), file.readlines())))

def get_this():
    doc = nlp(text)
    check_for = checkFor

    name_entities = []
    in_name = False
    new_ent = ''

    print(text)

    proc = []
    sentences = map(lambda x: x[0],doc.to_dict())
    for x in sentences:
        proc.extend(x)
    print(proc)

    proc = list(map(lambda x: [x['text'], x['lemma'], x['ner']],filter(lambda x: 'B-PER' in x['ner'] or 'I-PER' in x['ner'], proc)))
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

get_this()
