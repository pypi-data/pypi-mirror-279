# tests/test_data_preprocessor.py

import unittest
from qullm.llm_data_processor.data_preprocessor import DataPreprocessor

class TestDataPreprocessor(unittest.TestCase):
    def setUp(self):
        self.data = [
            " This  is a test. ",
            "This test is only a test.",
            "If this had been an actual emergency...",
        ]
        self.preprocessor = DataPreprocessor(self.data)

    def test_clean_data(self):
        cleaned_data = self.preprocessor.clean_data()
        self.assertEqual(cleaned_data[0], "This is a test.")

    def test_normalize_data(self):
        normalized_data = self.preprocessor.normalize_data()
        self.assertEqual(normalized_data[0], " this  is a test. ")

    def test_filter_data(self):
        filtered_data = self.preprocessor.filter_data(min_length=5)
        self.assertEqual(len(filtered_data), 2)

    def test_remove_special_characters(self):
        special_char_removed_data = self.preprocessor.remove_special_characters()
        self.assertEqual(special_char_removed_data[0], " This  is a test ")

    def test_remove_stopwords(self):
        stopwords = ["this", "is", "a"]
        stopwords_removed_data = self.preprocessor.remove_stopwords(stopwords)
        self.assertEqual(stopwords_removed_data[0], "is test.")
    
if __name__ == '__main__':
    unittest.main()