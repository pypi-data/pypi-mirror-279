# qullm/llm_data_processor/data_preprocessor.py

import re
from typing import List

class DataPreprocessor:
    def __init__(self, data: List[str]):
        """
        Initialize the DataPreprocessor class.

        Parameters:
        data (List[str]): A list of data that needs preprocessing.
        """
        self.data = data

    def clean_data(self) -> List[str]:
        """
        Clean the data by removing extra whitespace and newline characters.

        Returns:
        List[str]: A list of cleaned data.
        """
        cleaned_data = [re.sub(r'\s+', ' ', line).strip() for line in self.data]
        return cleaned_data

    def normalize_data(self) -> List[str]:
        """
        Normalize the data by converting all text to lowercase.

        Returns:
        List[str]: A list of normalized data.
        """
        normalized_data = [line.lower() for line in self.data]
        return normalized_data

    def filter_data(self, min_length: int = 5) -> List[str]:
        """
        Filter the data by removing lines with fewer words than the specified minimum length.

        Parameters:
        min_length (int): The minimum number of words to retain a line.

        Returns:
        List[str]: A list of filtered data.
        """
        filtered_data = [line for line in self.data if len(line.split()) >= min_length]
        return filtered_data

    def remove_special_characters(self) -> List[str]:
        """
        Remove special characters from the data, retaining only letters, numbers, and spaces.

        Returns:
        List[str]: A list of data with special characters removed.
        """
        cleaned_data = [re.sub(r'[^a-zA-Z0-9\s]', '', line) for line in self.data]
        return cleaned_data

    def remove_stopwords(self, stopwords: List[str]) -> List[str]:
        """
        Remove stopwords from the data.

        Parameters:
        stopwords (List[str]): A list of stopwords to remove.

        Returns:
        List[str]: A list of data with stopwords removed.
        """
        cleaned_data = []
        for line in self.data:
            words = line.split()
            new_words = [word for word in words if word.lower() not in stopwords]
            cleaned_data.append(' '.join(new_words))
        return cleaned_data