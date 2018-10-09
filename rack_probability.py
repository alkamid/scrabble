from typing import List, Union, Dict, Tuple
from pathlib import Path


def read_alphabet(filepath: Union[Path, str]) -> Dict[str, int]:
    letters_in_bag: Dict[str, int] = {}
    with open(filepath) as f:
        for line in f:
            lsp = line.split()
            if lsp[0] == 'blank':
                letters_in_bag.update({'?': int(lsp[2])})
            else:
                letters_in_bag.update({lsp[0].strip(): int(lsp[3])})
    return letters_in_bag


def calculate_rack_probability(rack: str) -> float:
    letters_in_bag = read_alphabet('polish.quackle_alphabet')
    num_letters_in_bag = 100
    prob = 1
    for let in rack.upper():
        prob *= letters_in_bag[let] / num_letters_in_bag
        letters_in_bag[let] -= 1
        num_letters_in_bag -= 1
    return prob


def order_words_by_probability(wordlist_path: Union[Path, str],
                               output_path: Union[Path, str],
                               word_len: int=7) -> List[Tuple[float, str]]:
    words_filtered = []
    with open(wordlist_path) as f:
        for line in f:
            word = line.split()[0].strip()
            if len(word) == word_len:
                words_filtered.append(word)

    words_with_prob = []
    for word in words_filtered:
        words_with_prob.append((calculate_rack_probability(word), word))

    words_sorted = sorted(words_with_prob, reverse=True)
    with open(output_path, 'w') as f:
        for prob, word in words_sorted:
            f.write(f'{word} {prob}\n')
            
    return words_sorted
