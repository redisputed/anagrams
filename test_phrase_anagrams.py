import unittest
import builtins
import sys
from unittest.mock import patch
from contextlib import contextmanager
from io import StringIO

import phrase_anagrams


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


class TestPhraseAnagrams(unittest.TestCase):

    def setUp(self):
        self.name = 'foster'

    def test_findAnagramFindsAnAnagramWithNoError(self):
        word_list = ['fetors', 'for', 'forest', 'fortes', 'softer']
        expected = set([*word_list,
                        '',
                        'Remaining letters = foster',
                        'Number of remaining letters = 6',
                        f'Number of remaining (real word) anagrams = {len(word_list)}'])
        with captured_output() as (out, err):
            phrase_anagrams.find_anagrams(self.name, word_list)
        actual = set(out.getvalue().split('\n'))
        error = err.getvalue()
        self.assertSetEqual(actual, expected)
        self.assertFalse(error)

    @patch('phrase_anagrams.main')
    def test_processUserChoiceRestartsIfEmptyString(self, mock):
        with mockRawInput(''):
            phrase_anagrams.process_choice(self.name)
            self.assertTrue(mock.called)

    def test_processUserChoiceExitsIfOctothorpe(self):
        with self.assertRaises(SystemExit) as cm:
            with mockRawInput('#'):
                phrase_anagrams.process_choice(self.name)

        self.assertEqual(cm.exception.code, 0)

    def test_processUserChoiceReturnsChoiceAndRemaining(self):
        with mockRawInput('for'):
            choice,remaining = phrase_anagrams.process_choice(self.name)
            self.assertEqual(choice,'for')
            self.assertEqual(remaining,'ste')


    def test_processUserChoiceWontWorkonBadChoice(self):
        expected = set(['', "Won't work! Make another choice!"])
        with mockRawInput('bad'):
            with captured_output() as (out, err):
                choice,remaining = phrase_anagrams.process_choice(self.name)
                self.assertEqual(choice,'bad')
                self.assertEqual(remaining,'foster')
        actual = out.getvalue()
        error = set(err.getvalue().split('\n'))
        self.assertSetEqual(error, expected)
        self.assertFalse(actual)



if __name__ == '__main__':
    unittest.main()
