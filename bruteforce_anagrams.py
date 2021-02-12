import sys
from itertools import permutations
from collections import Counter

import load_dictionary


def cv_map(word):
    """convert a word to a consonant-vowel map
        refactored out of first version of cv_map functions

    Args:
        word (string): value to convert

    Returns:
        string: contstructed cv_map
    """
    vowels = 'aeiouy'
    cv_map = ''
    for letter in word:
        if letter in vowels:
            cv_map += 'v'
        else:
            cv_map += 'c'
    return cv_map


def prep_words(name, word_list_ini):
    """Prep word list for finding anagrams. Create a new list from words in
        word_list_ini that have same length as name. convert words to lower.

    Args:
        name (string): the name to compare against.
        word_list_ini (list): list of words to compare.

    Returns:
        (list): words with same length as name converted to lowercase.
    """
    len_name = len(name)
    word_list = [word.lower() for word in word_list_ini
                 if len(word) == len_name]
    print(f'length of new word_list = {len(word_list)}')
    return word_list


def cv_map_words(word_list):
    """Map letters in words to consonants & vowels.

    Args:
        word_list (list): list of words

    Returns:
        (set): unique consonant vowel maps - 'cvcvcc', 'cvccvc'
    """
    cv_mapped_words = set()
    for word in word_list:
        cv_mapped_words.add(cv_map(word))
    total = len(cv_mapped_words)
    target = 0.05
    n = int(total*target)
    count_pruned = Counter(cv_mapped_words).most_common(total-n)
    filtered_cv_map = set()
    for pattern, _ in count_pruned:
        filtered_cv_map.add(pattern)
    print(f'length filtered_cv_map = {len(filtered_cv_map)}')
    return filtered_cv_map


def cv_map_filter(name, filtered_cv_map):
    """Remove permutations of words based on unlikely cons-vowel combos.

    Args:
        name (string): value for each permutation
        filtered_cv_map ([type]): cv_maps to match

    Returns:
        (set): permutations of name that match the cv_map
    """
    perms = {''.join(i) for i in permutations(name)}
    filtered_set = set()
    for candidate in perms:
        if cv_map(candidate) in filtered_cv_map:
            filtered_set.add(candidate)
    print(f'# choices after CV_map_filter = {len(filtered_set)}')
    return filtered_set


def trigram_filter(candidates, trigrams):
    """Remove unlikely trigrams from permutations

    Args:
        candidates (set): perms in cv map
        trigrams (list): least likely trigrams

    Returns:
        (set): permutations without trigrams
    """
    filtered_set = set()
    for candidate in candidates:
        for trigram in trigrams:
            if trigram.lower() in candidate:
                filtered_set.add(candidate)
    trigrams_filtered = candidates - filtered_set
    print(f'# choices after trigram_filter = {len(trigrams_filtered)}')
    return trigrams_filtered


def digram_filter(candidates):
    """Remove unlikely letter pairs from permutations

    Args:
        candidates (set): permutations

    Returns:
        (set): permutations without digrams
    """
    filter_set = set()
    rejects = ['dt', 'lr', 'md', 'ml', 'mr', 'mt',
               'mv', 'td', 'tv', 'vd', 'vl', 'vm', 'vr', 'vt']
    first_pair_rejects = ['ld', 'lm', 'lt', 'lv',
                          'rd', 'rl', 'rm', 'rt', 'rv', 'tl', 'tm']
    for candidate in candidates:
        for r in rejects:
            if r in candidate:
                filter_set.add(candidate)
        for fp in first_pair_rejects:
            if candidate.startswith(fp):
                filter_set.add(candidate)
    digram_filtered = candidates - filter_set
    print(f'# choices after digram_filter = {len(digram_filtered)}')
    return digram_filtered


def view_by_letter(candidates):
    """Filter to anagrams starting with input letters.

    Args:
        candidates (set): anagrams
    """
    first = input('Select a starting letter or press enter to see all: ')
    subset = []
    for candidate in candidates:
        if candidate.startswith(first):
            subset.append(candidate)
    print(*sorted(subset), sep='\n')
    print(f'Number of choices starting with {first} = {len(subset)}')
    return


def get_user_input():
    """get user input

    Returns:
        string: lowercase with all spaces removed
    """
    return input('Enter a name or phrase to proceed: ').lower().replace(' ', '')


def try_again(candidates):
    """Ask the user to try again or exit.

    Args:
        candidates (set): anagrams
    """
    try_again = input(
        'Try again? Press y to continue. Press any other key to exit.')
    if try_again.lower() == 'y':
        view_by_letter(candidates)
    else:
        sys.exit(0)
    return


def main():
    word_list = load_dictionary.load('words.txt')
    trigrams = load_dictionary.load('least-likely_trigrams.txt')
    name = get_user_input()
    words = prep_words(name, word_list)
    cv_mapped = cv_map_words(words)
    filtered = cv_map_filter(name, cv_mapped)
    candidates = trigram_filter(filtered, trigrams)
    candidates = digram_filter(candidates)
    view_by_letter(candidates)
    try_again(candidates)


if __name__ == '__main__':
    main()
