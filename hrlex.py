
lines = []

with open("small-hrlex.txt") as lex_file:
    for line in lex_file:
        wordStat = line.split('\t')
        wordStat[6] = int(wordStat[6].strip())

        if wordStat[4] == 'PROPN' and wordStat[6] > 5000:
            lines.append(wordStat)
            
            
    lines = sorted(lines, key=lambda x: -x[6])
    for l in lines:
        print(l)