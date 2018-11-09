#!/usr/bin/python
#-*- coding: utf-8 -*-

import io
import importsjp
import re

def anagram(letters, wordlist):
    alphagram = sorted(letters)
    result = set()
    for elem in wordlist:
        if alphagram == sorted(elem):
            result.add(elem)

    return result

def listWords(start, stop, num_letters=7):
    #odmOlafa = importsjp.OdmianaOlafa()
    
    inputFilename = 'io/playability-sevens.txt'
    #inputFilename = 'sevens-playable-short.txt'
    wordlist_filename = 'io/osps38_under9.txt'

    list_anagrams = []
    list_hooks = []
    list_all_words = []

    with open(wordlist_filename, encoding='utf-8', mode='r') as f:
        for word in f:
            if len(word) == num_letters+1:
                list_anagrams.append(word.strip().upper())
            elif len(word) == num_letters+2:
                list_hooks.append(word.strip().upper())

            list_all_words.append(word.strip().upper())

    with open(inputFilename, encoding='utf-8', mode='r') as f:
        inputList = set(line.strip().upper() for line in f.readlines()[start:stop])
        #inputList = set(''.join(sorted(a.upper().strip())) for a in f.readlines()[start:stop])

    with open('io/anki_existing_words_osps38.txt') as f:
        inputList_old = set(line.strip() for line in f)

    inputList = set(a for a in inputList if a not in inputList_old)
    print(inputList)

    baseforms = {}
    with open('io/osps38utf.txt') as f:
        for line in f.readlines():
            lsp = line.split('\t')
            baseforms[lsp[0]] = baseforms.get(lsp[0], []) + [lsp[1].strip().upper()]


    with open('output.txt', encoding='utf-8', mode='w') as f:

        for seven in inputList:
            i = 1
            ankiLine = u'%s; ' % u''.join(sorted(seven)).upper()
            for word in anagram(seven, list_anagrams):
                ankiLine += u'%s; ' % word.upper()
                frontHooks = set()
                backHooks = set()
                listMean = []
                addedWords = []
                for baseform in baseforms[word]:
                    base = baseform.split()[0]
                    ndm = ''
                    if '(NDM)' in baseform:
                        ndm = '(ndm) '
                    wordInfo = importsjp.HasloSJP(base.lower(), grabExisting=True, noWiki = True)
                    for each in wordInfo.words:
                        if (each.title.upper() in list_all_words) and (each.title not in addedWords) and (each.title.lower() == each.title) and each.notRoot == False:
                            for e in each.meanings:
                                try: defn = e.definition
                                except AttributeError:
                                    print(each.title, ' - no definition')
                                    listMean.append(ndm + '()')
                                else:
                                    if base == word:
                                        listMean.append(ndm + defn)
                                    else:
                                        listMean.append('← {0} ({1})'.format(each.title.upper(), defn))
                            addedWords.append(each.title)
                ankiLine += u', '.join(listMean).replace(u';', u',').replace(u'<br />', u',')                       

                ankiLine += u';'
                for hook in list_hooks:
                    if word == hook[1:]:
                        frontHooks.add(hook[0])
                    elif word == hook[:-1]:
                        backHooks.add(hook[-1])

                ankiLine += u'%s; %s;' % (''.join(frontHooks).upper(), ''.join(backHooks).upper())
                i+=1
            while i<10:
                ankiLine += u';;;;'
                i+=1
            print(ankiLine)

            ankiLine += u'sevens-osps38\n'
            f.write(ankiLine)


listWords(0,500, 7)
