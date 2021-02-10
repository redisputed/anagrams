import unittest
import builtins
import sys
from contextlib import contextmanager
from io import StringIO
import anagrams


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



class TestAnagrams(unittest.TestCase):

    def setUp(self):
        pass

    def test_getNameReturnsLowerString(self):
        expected = set(['Input name = NOTALLCAPS','','Using name = notallcaps'])
        with captured_output() as (out, err):
            with mockRawInput('NOTALLCAPS'):
                self.assertEqual(anagrams.get_name(), 'notallcaps')
        actual = set(out.getvalue().split('\n'))
        error = err.getvalue()
        self.assertSetEqual(actual, expected)
        self.assertFalse(error)

    def test_findAnagramReturnsAnAnagram(self):
        name = 'foster'
        expected = set(['fetors', 'forest', 'fortes', 'softer'])
        actual = set(anagrams.find_anagram(name))
        self.assertSetEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
