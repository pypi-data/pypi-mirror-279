# tests/test_data_loader.py

import unittest
from qullm.llm_data_processor.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def test_load_data(self):
        data_loader = DataLoader('tests/test_data.txt')
        data = data_loader.load_data()
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], 'This is a test.\n')

    def test_load_data_as_string(self):
        data_loader = DataLoader('tests/test_data.txt')
        data = data_loader.load_data_as_string()
        self.assertTrue(data.startswith('This is a test.'))

    def test_load_data_as_lines(self):
        data_loader = DataLoader('tests/test_data.txt')
        data = data_loader.load_data_as_lines()
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], 'This is a test.')

if __name__ == '__main__':
    unittest.main()