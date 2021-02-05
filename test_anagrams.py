import unittest
import builtins
from contextlib import contextmanager

import anagrams


@contextmanager
def mockRawInput(mock):
    original_raw_input = builtins.input
    builtins.input = lambda _: mock
    yield
    builtins.input = original_raw_input


class TestAnagrams(unittest.TestCase):

    def setUp(self):
        pass

    def test_getNameReturnsLowerString(self):
        with mockRawInput('NOTALLCAPS'):
            self.assertEqual(anagrams.get_name(), 'notallcaps')

    def test_findAnagramReturnsAnAnagram(self):
        name = 'foster'
        expected = set(['fetors', 'forest', 'fortes', 'softer'])
        actual = set(anagrams.find_anagram(name))
        self.assertSetEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
