import sys

with open(sys.argv[1], 'r', encoding='utf8') as lex_file:
    with open(sys.argv[2], 'w', encoding='utf8') as output:
        for line in lex_file:
            wordStat = line.split('\t')
            wordStat[6] = int(wordStat[6].strip())
            wordStat[3] = wordStat[3].split('|')

            if wordStat[4] == 'PROPN' and wordStat[3][2] == 'Number=singular' and wordStat[6] > 5:
                fin = wordStat[:3]
                fin.append(str(wordStat[len(wordStat) - 2]))
                outLine = '\t'.join(fin) + '\n'
                output.write(outLine)
