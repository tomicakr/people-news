
with open('apiLog.txt', 'r', encoding='utf8') as file:
    with open('links.txt', 'w', encoding='utf8') as out:
        lines = list(map(lambda x: x.split('\t')[0], file.readlines()))
        for line in lines:
            out.write(line+'\n')
