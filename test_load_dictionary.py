import unittest
import load_dictionary

class TestLoadDictionary(unittest.TestCase):

    def setUp(self):
        temp_contents = ['Test', 'file', 'contents']
        self.file_name = 'temp_file.txt'
        self.bad_file_name = 'bad_file.txt'
        with open(self.file_name) as in_file:
            for item in temp_contents:
                in_file.write(item)

    def test_loadLoadsFileContentsAsLower(self):
        loaded_txt=load_dictionary.load(self.file_name)
        self.assertEqual(loaded_txt[0], 'test')
        self.assertEqual(loaded_txt[1], 'file')
        self.assertEqual(loaded_txt[2], 'contents')

    def test_loadBadFileRasiesIOException(self):
        with self.assertRaises(IOError):
            load_dictionary.load(self.bad_file_name)



if __name__ == '__main__':
    unittest.main()
