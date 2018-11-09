sevens = set()
with open('/home/adam/code/scrabble/io/osps38utf.txt') as f:
    for line in f:
        lsp = line.split()[0]
        if len(lsp) == 7:
            sevens.add(lsp)

with open('/home/adam/Resources/scrabble/scrabble_anki.txt') as f:
    for line in f:
        lsp = line.split('\t')
        if 'sevens' in lsp[-1]:
            sols = line[8:].split('
