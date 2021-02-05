import unittest
import os
import load_dictionary


class TestLoadDictionary(unittest.TestCase):

    def setUp(self):
        temp_contents = ['Test', 'file', 'contents', 'LOWERCASE']
        self.file_name = 'temp_file.txt'
        try:
            with open(self.file_name, 'a') as out_file:
                for item in temp_contents:
                    out_file.write(item)
                    out_file.write('\n')
        except IOError as e:
            print(f'{e}\nError opening {self.file_name}.\n')

    def test_loadLoadsFileContentsAsLower(self):
        loaded_txt = load_dictionary.load(self.file_name)
        self.assertEqual(loaded_txt[0], 'test')
        self.assertEqual(loaded_txt[1], 'file')
        self.assertEqual(loaded_txt[2], 'contents')
        self.assertEqual(loaded_txt[3], 'lowercase')

    def tearDown(self):
        if os.path.isfile(self.file_name):
            try:
                os.remove(self.file_name)
            except OSError as e:
                print(f'Error: {e.filename} - {e.strerror}.')


if __name__ == '__main__':
    unittest.main()
