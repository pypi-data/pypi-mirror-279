# tests/test_data_analyzer.py

import unittest
from collections import Counter
from qullm.llm_data_processor.data_analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):
    def setUp(self):
        self.data = [
            "This is a test.",
            "This test is only a test.",
            "If this had been an actual emergency...",
        ]
        self.analyzer = DataAnalyzer(self.data)

    def test_get_word_frequency(self):
        word_freq = self.analyzer.get_word_frequency()
        self.assertIsInstance(word_freq, Counter)
        self.assertGreater(word_freq["test"], 1)

    def test_get_data_statistics(self):
        stats = self.analyzer.get_data_statistics()
        self.assertEqual(stats['num_lines'], len(self.data))
        self.assertGreater(stats['num_words'], 5)

    def test_get_unique_words(self):
        unique_words = self.analyzer.get_unique_words()
        self.assertIn("test", unique_words)

    def test_get_average_line_length(self):
        average_length = self.analyzer.get_average_line_length()
        self.assertGreater(average_length, 3)

    def test_get_most_common_words(self):
        most_common_words = self.analyzer.get_most_common_words(n=2)
        self.assertEqual(len(most_common_words), 2)

if __name__ == '__main__':
    unittest.main()