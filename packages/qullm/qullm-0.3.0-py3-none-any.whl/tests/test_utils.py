# tests/test_utils.py

import unittest
import os
import json
from qullm.llm_data_processor.utils import save_data, load_config, save_config, split_data

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.data = [
            "This is a test.",
            "This test is only a test.",
            "If this had been an actual emergency...",
        ]
        self.config = {
            "param1": "value1",
            "param2": "value2"
        }
        self.data_file_path = 'tests/processed_data.txt'
        self.config_file_path = 'tests/config.json'

    def test_save_data(self):
        save_data(self.data, self.data_file_path)
        self.assertTrue(os.path.exists(self.data_file_path))
        with open(self.data_file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
        self.assertEqual(len(content), len(self.data))

    def test_load_config(self):
        with open(self.config_file_path, 'w', encoding='utf-8') as file:
            json.dump(self.config, file)
        loaded_config = load_config(self.config_file_path)
        self.assertEqual(loaded_config, self.config)

    def test_save_config(self):
        save_config(self.config, self.config_file_path)
        self.assertTrue(os.path.exists(self.config_file_path))
        with open(self.config_file_path, 'r', encoding='utf-8') as file:
            loaded_config = json.load(file)
        self.assertEqual(loaded_config, self.config)

    def test_split_data(self):
        train_data, test_data = split_data(self.data, train_ratio=0.8)
        self.assertEqual(len(train_data), 2)
        self.assertEqual(len(test_data), 1)

if __name__ == '__main__':
    unittest.main()