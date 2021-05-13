
import classla
classla.download('hr')
nlp = classla.Pipeline('hr', processors='tokenize,ner,lemma')
doc = nlp("Tomislavu Kravaršćanu Igorom Mekterovićem Josipu Miličeviću")
proc = list(map(lambda x: (x['text'], x['lemma'], x['ner']),filter(lambda x: 'PER' in x['ner'], doc.to_dict()[0][0])))

for (x, y, z) in proc:
    print('{} {} {}'.format(x, y, z))
