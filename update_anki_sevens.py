import re

def anagram(letters, wordlist):
    alphagram = sorted(letters)
    result = set()
    for elem in wordlist:
        if alphagram == sorted(elem):
            result.add(elem)

    return result

def existing_anagrams(filename):
    result = {}
    rc = re.compile(r'<td id=ana>(\w*)?<', re.UNICODE)
    with open(filename) as f:
        for line in f:
            if 'trojki' not in line:
                result[line[:7]] = set(re.findall(rc, line))

    return result

def load_wordlist(filename):
    words = set()
    with open(filename) as f:
        for line in f:
            words.add(line.strip())
    return words

existing = existing_anagrams('/home/adam/Resources/scrabble/scrabble_anki.txt')
words = load_wordlist('/home/adam/code/scrabble/io/osps38_under9.txt')
for key in existing:
    new_anagrams = anagram(key, words)
    if existing[key] != new_anagrams:
        print(key, existing[key], new_anagrams)
