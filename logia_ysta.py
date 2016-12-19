'''
Check for words ending with -LOGIA which don't have -LOG counterparts
Check for words ending with -ISTA/-YSTA which don't have -ISTKA/-YSTKA counterparts
'''

logia = set()
logg = set()
ysta = set()
ystka = set()
ista = set()
istka = set()

with open('update35/osps-final.txt') as f:
    for line in f.readlines():
        lsp = line.split()
        if lsp[0][-5:] == 'LOGIA' and lsp[1].strip()[-5:] == 'logia':
            logia.add(lsp[0])
        elif lsp[0][-3:] == 'LOG' and lsp[1].strip()[-3:] == 'log':
            logg.add(lsp[0])
        elif lsp[0][-4:] == 'YSTA' and lsp[1].strip()[-4:] == 'ysta':
            ysta.add(lsp[0])
        elif lsp[0][-5:] == 'YSTKA' and lsp[1].strip()[-5:] == 'ystka':
            ystka.add(lsp[0])
        elif lsp[0][-4:] == 'ISTA' and lsp[1].strip()[-4:] == 'ista':
            ista.add(lsp[0])
        elif lsp[0][-5:] == 'ISTKA' and lsp[1].strip()[-5:] == 'istka':
            istka.add(lsp[0])

with open('brak_log.txt', 'w') as f:
    for log in logia:
        if log[:-2] not in logg:
            f.write(log + '\n')

with open('brak_ystka.txt', 'w') as f:
    for y in ysta:
        if y[:-4] + 'YSTKA' not in ystka:
            f.write(y + '\n')

with open('brak_istka.txt', 'w') as f:
    for y in ista:
        if y[:-4] + 'ISTKA' not in istka:
            f.write(y + '\n')
