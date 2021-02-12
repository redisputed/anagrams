import unittest
import builtins
import sys
from unittest.mock import patch
from contextlib import contextmanager
from io import StringIO
import load_dictionary

import bruteforce_anagrams


@contextmanager
def mockRawInput(mock):
    original_raw_input = builtins.input
    builtins.input = lambda _: mock
    yield
    builtins.input = original_raw_input


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestBruteforceAnagrams(unittest.TestCase):

    def setUp(self):
        self.name = 'foster'
        self.word_list = ['FETORS', 'FOR', 'FOREST', 'FORTES', 'SOFTER']

    def test_prepWordsReturnsListofEqualLenghtWordsLower(self):
        expected = set(['fetors', 'forest', 'fortes', 'softer'])
        expected_len_list = f'length of new word_list = {len(expected)}'

        with captured_output() as (out, err):
            actual = set(bruteforce_anagrams.prep_words(
                self.name, self.word_list))
        len_list = out.getvalue().strip('\n')
        error = err.getvalue()
        self.assertSetEqual(actual, expected)
        self.assertEqual(len_list, expected_len_list)
        self.assertFalse(error)

    def test_cvMapWordsTakesListReturnsCVMap(self):
        words_lower = [word.lower()
                       for word in self.word_list if len(word) == len(self.name)]
        expected = set(['cvcvcc', 'cvccvc'])
        expected_len_list = f'length filtered_cv_map = {len(expected)}'

        with captured_output() as (out, err):
            actual = bruteforce_anagrams.cv_map_words(words_lower)
        len_list = out.getvalue().strip('\n')
        error = err.getvalue()
        self.assertSetEqual(actual, expected)
        self.assertEqual(len_list, expected_len_list)
        self.assertFalse(error)

    def test_cvMapFilterRemovesUnlikelyConVowelCombos(self):
        word = 'run'
        cv_map = set(['cvc', 'cvv'])
        expected = set(['run', 'nur'])
        expected_len_list = f'# choices after CV_map_filter = {len(expected)}'

        with captured_output() as (out, err):
            actual = bruteforce_anagrams.cv_map_filter(word, cv_map)
        len_list = out.getvalue().strip('\n')
        error = err.getvalue()
        self.assertSetEqual(actual, expected)
        self.assertEqual(len_list, expected_len_list)
        self.assertFalse(error)

    def test_cvMapConvertsWordToCv(self):
        word = 'test'
        expected = 'cvcc'
        actual = bruteforce_anagrams.cv_map(word)
        self.assertEqual(actual, expected)

    def test_trigramFilterRemovesPermsWithUnlikelyTrigrams(self):
        candidates = {'dosl', 'dlos', 'ldos', 'odsl', 'olds', 'slod', 'dlso', 'ldso', 'sldo', 'osdl', 'lsdo',
                      'sdol', 'dsol', 'dols', 'lods', 'osld', 'odls', 'sdlo', 'sodl', 'losd', 'sold', 'lsod', 'olsd', 'dslo'}
        trigrams = load_dictionary.load('least-likely_trigrams.txt')
        expected = set(['ldso', 'ldos', 'dslo', 'olsd', 'sldo', 'lsod', 'olds', 'osdl',
                        'sold', 'lsdo', 'dlso', 'losd', 'dosl', 'sdlo', 'dsol', 'osld', 'odsl', 'dlos'])
        expected_len_list = f'# choices after trigram_filter = {len(expected)}'

        with captured_output() as (out, err):
            actual = bruteforce_anagrams.trigram_filter(candidates, trigrams)
        len_list = out.getvalue().strip('\n')
        error = err.getvalue()
        self.assertSetEqual(actual, expected)
        self.assertEqual(len_list, expected_len_list)
        self.assertFalse(error)

    def test_digramFilterRemovesPermsWithUnlikelyDigrams(self):
        candidates = {'ldso', 'ldos', 'dslo', 'olsd', 'sldo', 'lsod', 'olds', 'osdl',
                      'sold', 'lsdo', 'dlso', 'losd', 'dosl', 'sdlo', 'dsol', 'osld', 'odsl', 'dlos'}
        expected = set(['dlso', 'osld', 'dosl', 'dlos', 'lsdo', 'dsol', 'odsl',
                        'sdlo', 'lsod', 'losd', 'sold', 'olds', 'osdl', 'sldo', 'olsd', 'dslo'])
        expected_len_list = f'# choices after digram_filter = {len(expected)}'

        with captured_output() as (out, err):
            actual = bruteforce_anagrams.digram_filter(candidates)
        len_list = out.getvalue().strip('\n')
        error = err.getvalue()
        self.assertSetEqual(actual, expected)
        self.assertEqual(len_list, expected_len_list)
        self.assertFalse(error)

    def test_viewByLetterDisplaysAnagramsStartingWithChoice(self):
        candidates = {'dlso', 'osld', 'dosl', 'dlos', 'lsdo', 'dsol', 'odsl',
                      'sdlo', 'lsod', 'losd', 'sold', 'olds', 'osdl', 'sldo', 'olsd', 'dslo'}
        expected = set(['', 'Number of choices starting with o = 5',
                        'osdl', 'olsd', 'osld', 'odsl', 'olds'])

        with mockRawInput('o'):
            with captured_output() as (out, err):
                bruteforce_anagrams.view_by_letter(candidates)
        actual = set(out.getvalue().split('\n'))
        error = err.getvalue()
        self.assertSetEqual(actual, expected)
        self.assertFalse(error)

    def test_getUserInputReturnsLowerCaseUserValue(self):
        expected = self.name
        with mockRawInput(self.name.upper()):
            actual = bruteforce_anagrams.get_user_input()
        self.assertEqual(actual, expected)

    def test_getUserInputRemovesSpaces(self):
        expected = 'phrasewithspacesremove'
        with mockRawInput('phrase with spaces remove'):
            actual = bruteforce_anagrams.get_user_input()
        self.assertEqual(actual, expected)

    @patch('bruteforce_anagrams.view_by_letter')
    def test_tryAgainCallsViewByLetter(self, mock):
        candidates = [word.lower() for word in self.word_list]
        with mockRawInput('y'):
            bruteforce_anagrams.try_again(candidates)
        self.assertTrue(mock.called)

    def test_tryAgainExits(self):
        candidates = [word.lower() for word in self.word_list]
        with self.assertRaises(SystemExit) as cm:
            with mockRawInput('#'):
                bruteforce_anagrams.try_again(candidates)
        self.assertEqual(cm.exception.code, 0)


if __name__ == '__main__':
    unittest.main()
