import re
import locale
from typing import List, Set, Tuple, Dict

locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')


def get_words_from_playability_list(playability: str, num_words: int) -> List:
    words = []
    i = 0
    with open(playability) as f:
        for line in f:
            if i > num_words:
                break
            base = line.split('(')[1].split(')')[0]
            if len(base) > 2:
                words.append(base)
                i += 1
    return list(dict.fromkeys(words))


def get_words_shorter_than(wordlist: str, word_len: int) -> Set:
    words = set()
    with open(wordlist) as f:
        for line in f:
            word = line.strip().split()[0]
            if len(word) < word_len:
                words.add(word)
    return words


def hooks_dict(word_set: Set, max_word_len: int) -> Tuple[Dict, Dict]:
    left_hdict = {}
    right_hdict = {}
    for word in word_set:
        if len(word) > max_word_len + 1:
            continue
        lhook, rword = word[0], word[1:]
        lword, rhook = word[:-1], word[-1]
        if rword in word_set:
            left_hdict[rword] = left_hdict.get(rword, '') + lhook
        if lword in word_set:
            right_hdict[lword] = right_hdict.get(lword, '') + rhook
    return left_hdict, right_hdict


def create_anki_set(playability_list, playability_limit, wordlist):
    inputs = get_words_from_playability_list(playability_list, playability_limit)

    max_word_len = len(max(inputs, key=locale.strxfrm))
    print(max(inputs))
    print(max_word_len)

    words = get_words_shorter_than(wordlist, max_word_len + 2)

    l_hooks, r_hooks = hooks_dict(words, max_word_len)

    i = 1
    inputs = list(inputs)
    while i*100 < len(inputs):

        anki = ''
        for word in inputs[(i-1)*100:i*100]:
            line = f'{word}; ; ;'
            for hook in sorted(l_hooks.get(word, ''), key=locale.strxfrm):
                line += f' <br><hook>{hook}</hook>{word}'
            else:
                line += ' ;'
            for hook in sorted(r_hooks.get(word, ''), key=locale.strxfrm):
                line += f' <br>{word}<hook>{hook}</hook>'
            else:
                line += ' ;'
            line += ' przedłużki\n'
            anki += line

        with open(f'/tmp/{i}ankiprzed.txt', 'w') as f:
            f.write(anki)
        i += 1


create_anki_set('/home/adam/code/scrabble/io/playability-pl-hooks-nobase-osps38.txt',
                1000,
                '/home/adam/code/scrabble/io/osps38utf.txt')


def pos(inp, tag=True):
    if tag:
        return {
            'n': 'nouns',
            'v': 'verbs',
            'interj': 'interjections',
            'adj': 'adjectives',
            'adv': 'adverbs',
            'pron': 'pronouns',
            'prep': 'prepositions', }[inp]
    else:
        return {
            'n': 'noun',
            'v': 'verb',
            'interj': 'interjection',
            'adj': 'adjective',
            'adv': 'adverb',
            'pron': 'pronoun',
            'prep': 'preposition', }[inp]


def extras(inp, tag=True):
    output = [set(), []]
    for elem in inp:
        elem = elem.strip('[')
        elem = elem.strip(']')
        if elem.find(' ') != -1:
            output[0].add(pos(elem[:elem.find(' ')], tag))
        else:
            output[0].add(pos(elem, tag))
            output[1].append(None)
            continue
        rest = elem[elem.find(' ') + 1:]
        output[1].append(rest)

    for (i, elem) in enumerate(output[1]):
        if output[1][i]:
            output[1][i] = u'%d. ' % (i + 1) + output[1][i]

    output[1] = filter(None, output[1])
    if len(output[1]) == 1:
        output[1][0] = output[1][0].replace(u'1. ', u'')

    return output


def hooks_pos(word, hooks, front=True):
    re_square_brackets = re.compile(r'(\[.*?\])')
    hooks_definitions = open('fours_qjxz.txt', 'r')
    defs = hooks_definitions.read()
    hooks = hooks.upper()
    output = u''
    for elem in hooks:
        if front:
            re_elem = re.compile(u'\n(%s%s.*)' % (elem, word))
            output_word_hooked = '<hook>%s</hook>%s' % (elem, word)
        else:
            re_elem = re.compile(u'\n(%s%s.*)' % (word, elem))
            output_word_hooked = '%s<hook>%s</hook>' % (word, elem)

        s_elem = re.search(re_elem, defs)
        if s_elem:
            list = s_elem.group(1).split('\t')
            if list[1][:3] == word:
                origin = u'<small>← %s</small>' % word
            else:
                additional = re.findall(re_square_brackets, list[1])
                extra = extras(additional, False)
                origin = u'<small>' + ', '.join(extra[0]) + '</small>'

            output = output + '<br>' + output_word_hooked + ' ' + origin
    return output


def main():
    custom_tags = ' threes-with-hooks'
    order = ['word', 'definition', 'front hooks', 'back hooks']

    input_filename = 'threes_qjxz.txt'
    output_filename = 'anki_output_3.txt'
    file = open(input_filename, 'r')
    lines = [line.rstrip(u'\n') for line in file]
    re_square_brackets = re.compile(r'(\[.*?\])')

    output = u''

    for line in lines:
        list = line.split('\t')
        output_line = list[0] + u';'
        additional = re.findall(re_square_brackets, list[1])
        if additional:
            for each in additional:
                list[1] = list[1].replace(each, '')
        list[1] = list[1].replace('/', '<br>')
        output_line += u' ' + list[1] + u';'
        extra = extras(additional)
        if extra[1]:
            output_line += u' ' + u'<br>'.join(extra[1])
        output_line += u'; ' + hooks_pos(list[0], list[2]) + u';'
        output_line += u' ' + hooks_pos(list[0], list[3], False) + u';'
        output_line += ' '.join(extra[0])
        output_line += custom_tags
        output += output_line + u'\n'

    file.close
    file = open(output_filename, 'w')
    file.write(output.encode('utf-8'))
    file.close


# main()
