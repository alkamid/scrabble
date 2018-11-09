# With this script you can compare two lists of words and their base forms
# and determine which base forms exist in one, but not the other list.
# It was written to compare OSPS (the official Polish Scrabble dictionary)
# and a free wordlist from sjp.pl

def remove_sjp_duplicates():
    """
    "duplicates" are words whose all inflections are contained in another
    word's inflection list. For example "sikh" and "sikhowie":
    sikh, sikha, sikhach, sikhami, sikhem, sikhom, sikhowi, sikhowie, sikhów, sikhu, sikhy
    sikhowie, sikhach, sikhami, sikhom, sikhów, sikhy
    """
    allwords = []

    with open('odm.txt', 'r') as f:
        for line in f:
            l = line.strip().split(',')
            if l[0][0].upper() != l[0][0]:
                allwords.append(l)

    baseforms = []

    for i, word in enumerate(allwords):
        baseform = word[0]
        inflexions = word[1:]

        found = 0
        for j in range(i-10, i+10):
            if j < 0 or j == i:
                continue
            elif j >= len(allwords):
                break
            else:
                if len(inflexions) and all(form in allwords[j] for form in inflexions):
                    found = 1
                    continue
        
        # this is a hack for comparing with OSPS only. Some gerunds are listed
        # as base forms on sjp.pl — below we're removing them as they are already
        # contained in the verb's inflections
        if not found or (baseform.endswith('nie') and len(inflexions) == 7):
            baseforms.append(baseform)

    with open('sjp-baseforms.txt', 'w') as g:
        for word in baseforms:
            g.write(word + '\n')


def strip_OSPS_of_gerunds():
    """
    This script takes in the OSPS list of inflections and their base forms
    in the following format:
    ABADAŃSKU	abadański
    ABADAŃSKĄ	abadański
    ABAK	abak
    ABAK	abaka
    ABAKA	abaka
    then it's detecting all gerunds (words ending with "nie" and having 7
    inflexions only, e.g. "łyżeczkowania, łyżeczkowaniem, łyżeczkowaniu,
    łyżeczkowaniach, łyżeczkowaniami, łyżeczkowaniom, łyżeczkowań" <- łyżeczkowanie
    Gerunds are removed and the output list is sorted.
    """
    import locale
    locale.setlocale(locale.LC_ALL, "pl_PL.UTF-8")

    words = {}
    with open('ospsutf.txt', 'r') as f:
        for line in f:
            l = line.strip().split()
            try: words[l[1]].append(l[0].lower())
            except KeyError:
                words[l[1]] = [l[0].lower()]

    final_wordlist = []
    with open('osps-nogerunds.txt', 'w') as f:
        for word in words:
            if word.endswith('nie') and len(words[word]) == 8:
                pass
            else:
                final_wordlist.append(word)
        
        final_wordlist.sort(key=locale.strxfrm)
        for word in final_wordlist:
            f.write(word + '\n')


def compare_OSPS_sjp():
    """
    Take the two preprocessed lists (OSPS and sjp.pl) and determine which
    base forms exist in OSPS but not in sjp.pl — they are potential errors in OSPS.
    There are two output lists, as words ending in "-ny" are filtered out.
    Most of them (but unfortunately not all) are passive adjectival participles
    (imiesłów przymiotnikowy bierny) which in OSPS are treated as base forms,
    but sjp.pl treats them as forms of verbs
    """
    sjpbases = set()
    osps_has_sjp_doesnt = []
    with open('osps-nogerunds.txt', 'r') as f, open('sjp-baseforms.txt', 'r') as g:
        for line in g:
            sjpbases.add(line.strip())
        for line in f:
            base_osps = line.strip()
            if base_osps not in sjpbases and base_osps not in osps_has_sjp_doesnt:
                osps_has_sjp_doesnt.append(base_osps)

    with open('diffs.txt', 'w') as f, open('diffs-ny.txt', 'w') as g:
        for word in osps_has_sjp_doesnt:
            if word.endswith('ny'):
                g.write(word + '\n')
            else:
                f.write(word + '\n')

remove_sjp_duplicates()
compare_OSPS_sjp()
#remove_gerunds_from_OSPS()
