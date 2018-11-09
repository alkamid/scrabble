import words_with_hooks_to_anki as anki
import locale

locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')


def test_getting_words_from_playability_list():
    words = anki.get_words_from_playability_list(
        '/home/adam/Resources/scrabble/quackle/test/output/playability-pl-hooks-nobase-osps38.txt',
        10)

    assert all(w in words for w in ['ŹGA', 'ŹLE', 'JAŹ'])


def test_wordlist_shorter_than():
    words = anki.get_words_shorter_than('/home/adam/Resources/scrabble/quackle/test/input/osps38utf.txt', 5)

    assert all(w in words for w in ['ŹGA', 'ŹLE', 'JAŹ', 'ŹGNĄ'])


def test_hooks_dict():
    words = anki.get_words_shorter_than('/home/adam/Resources/scrabble/quackle/test/input/osps38utf.txt', 5)

    l_hooks, r_hooks = anki.hooks_dict(words, 3)
    print(l_hooks['ŹGA'], sorted(r_hooks['ŹGA'], key=locale.strxfrm))
