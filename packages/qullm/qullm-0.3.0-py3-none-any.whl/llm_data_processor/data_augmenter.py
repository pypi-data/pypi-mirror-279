# qullm/llm_data_processor/data_augmenter.py

import random
from typing import List

class DataAugmenter:
    def __init__(self, data: List[str]):
        """
        Initialize the DataAugmenter class.

        Parameters:
        data (List[str]): The list of data to be augmented.
        """
        self.data = data

    def augment_data(self, augment_factor: int = 2) -> List[str]:
        """
        Augment data by duplicating and shuffling to increase the data volume.

        Parameters:
        augment_factor (int): The factor by which to augment the data.

        Returns:
        List[str]: The augmented list of data.
        """
        augmented_data = self.data * augment_factor
        random.shuffle(augmented_data)
        return augmented_data

    def synonym_replacement(self, word_map: dict) -> List[str]:
        """
        Replace words in the data using synonyms.

        Parameters:
        word_map (dict): A dictionary containing words and their synonyms.

        Returns:
        List[str]: The list of data with synonyms replaced.
        """
        augmented_data = []
        for line in self.data:
            words = line.split()
            new_words = [word_map.get(word, word) for word in words]
            augmented_data.append(' '.join(new_words))
        return augmented_data

    def random_insertion(self, insertion_words: List[str], insert_prob: float = 0.1) -> List[str]:
        """
        Randomly insert words into the data.

        Parameters:
        insertion_words (List[str]): The list of words to insert.
        insert_prob (float): The probability of inserting a word at each position.

        Returns:
        List[str]: The list of data with inserted words.
        """
        augmented_data = []
        for line in self.data:
            words = line.split()
            new_words = []
            for word in words:
                new_words.append(word)
                if random.random() < insert_prob:
                    new_words.append(random.choice(insertion_words))
            augmented_data.append(' '.join(new_words))
        return augmented_data

    def random_deletion(self, delete_prob: float = 0.1) -> List[str]:
        """
        Randomly delete words from the data.

        Parameters:
        delete_prob (float): The probability of deleting each word.

        Returns:
        List[str]: The list of data with words deleted.
        """
        augmented_data = []
        for line in self.data:
            words = line.split()
            new_words = [word for word in words if random.random() > delete_prob]
            augmented_data.append(' '.join(new_words))
        return augmented_data

    def random_swap(self, swap_prob: float = 0.1) -> List[str]:
        """
        Randomly swap the positions of words in the data.

        Parameters:
        swap_prob (float): The probability of swapping each pair of words.

        Returns:
        List[str]: The list of data with words' positions swapped.
        """
        augmented_data = []
        for line in self.data:
            words = line.split()
            for i in range(len(words)):
                if random.random() < swap_prob and i < len(words) - 1:
                    words[i], words[i + 1] = words[i + 1], words[i]
            augmented_data.append(' '.join(words))
        return augmented_data