"""
This is a utility to compare two word lists, formatted in the following way:
WORD	WORD_BASE_FORM
WORD2	WORD2_BASE_FORM
It can be used to describe an update of a word list for word games, e.g. Scrabble.
It will output four files: added.txt (added words), deleted.txt, added-existed.txt
(words whose "word-base form" combination was added but they existed in the list
already with a different base form), and deleted-remained.txt (words whose "word-base form"
combination was deleted but they remained in the list with a different base form) 
"""

import locale
locale.setlocale(locale.LC_ALL, "pl_PL.UTF-8")    

def completely_new(oldlist, newlist, added_desc, deleted_desc):
    """
    inputs:
        oldlist (string): filename of the old list
        newlist (string): filename of the new list
        added_desc (string): description of added words in the format "WORD	WORD_BASE_FORM	explanation"
        deleted_desc (string): description of deleted words in the format "WORD	WORD_BASE_FORM	explanation"
    """
    
    old = set()
    old_form = set()
    new = set()
    new_form = set()
    adesc = set()
    ddesc = set()
    with open(oldlist) as f:
        for line in f.readlines():
            lsp = line.split()
            old.add(line.strip())
            old_form.add(lsp[0])
            
    with open(newlist) as f:
        for line in f.readlines():
            lsp = line.split()
            new.add(line.strip())
            new_form.add(lsp[0])

    with open(added_desc) as f:
        for line in f.readlines():
            lsp = line.split('\t')
            adesc.add(('\t'.join([lsp[0].strip().upper(), lsp[1].strip()]), '\t'.join(lsp[2:]).lstrip()))

    with open(deleted_desc) as f:
        for line in f.readlines():
            lsp = line.split('\t')
            ddesc.add(('\t'.join([lsp[0].strip().upper(), lsp[1].strip()]), '\t'.join(lsp[2:]).lstrip()))
    
    added = [a for a in new if a.split()[0] not in old_form]
    deleted = [a for a in old if a.split()[0] not in new_form]

    added.sort(key=locale.strxfrm)
    deleted.sort(key=locale.strxfrm)

    with open('added.txt', 'w') as f:
        for a in added:
            for d in adesc:
                if d[0] == a:
                    f.write(d[0] + '\t' + d[1])

    with open('deleted.txt', 'w') as f:
        for d in deleted:
            for u in ddesc:
                if u[0] == d:
                    f.write(u[0] + '\t' + u[1])
    
    del_remained = []
    add_existed = []

    for o in old:
        if o not in new and o.split()[0] in new_form:
            del_remained.append(o)

    for n in new:
        if n.split()[0] in old_form and n not in old:
            add_existed.append(n)

    with open('deleted-remained.txt', 'w') as f, open('added-existed.txt', 'w') as g:
        del_remained.sort(key=locale.strxfrm)
        add_existed.sort(key=locale.strxfrm)
        for d in del_remained:
            for u in ddesc:
                if u[0].startswith(d):
                    f.write(u[0] + '\t' + u[1])
        for a in add_existed:
            for d in adesc:
                if d[0].startswith(a):
                    g.write(d[0] + '\t' + d[1])
            
def dwojki():
    with open('usuniete.txt') as f:
        for line in f.readlines():
            if len(line.split()[0]) == 2:
                print(line)

            
completely_new('osps34-new.txt', 'osps-new.txt', 'dodane35.txt', 'usuniete35.txt')
#dwojki()
