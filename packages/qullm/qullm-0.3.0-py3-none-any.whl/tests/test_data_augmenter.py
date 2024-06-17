# tests/test_data_augmenter.py

import unittest
from qullm.llm_data_processor.data_augmenter import DataAugmenter

class TestDataAugmenter(unittest.TestCase):
    def setUp(self):
        self.data = [
            "This is a test.",
            "This test is only a test.",
            "If this had been an actual emergency...",
        ]
        self.augmenter = DataAugmenter(self.data)

    def test_augment_data(self):
        augmented_data = self.augmenter.augment_data(augment_factor=2)
        self.assertEqual(len(augmented_data), len(self.data) * 2)

    def test_synonym_replacement(self):
        word_map = {"test": "exam", "emergency": "crisis"}
        synonym_replaced_data = self.augmenter.synonym_replacement(word_map)
        self.assertIn("exam", synonym_replaced_data[0])

    def test_random_insertion(self):
        insertion_words = ["random", "insert"]
        random_insertion_data = self.augmenter.random_insertion(insertion_words, insert_prob=0.5)
        self.assertTrue(any(word in random_insertion_data[0] for word in insertion_words))

    def test_random_deletion(self):
        random_deletion_data = self.augmenter.random_deletion(delete_prob=0.5)
        self.assertLessEqual(len(random_deletion_data[0].split()), len(self.data[0].split()))

    def test_random_swap(self):
        random_swap_data = self.augmenter.random_swap(swap_prob=0.5)
        self.assertNotEqual(random_swap_data, self.data)

if __name__ == '__main__':
    unittest.main()