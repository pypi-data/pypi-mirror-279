# qullm/llm_data_processor/data_analyzer.py

from collections import Counter

class DataAnalyzer:
    def __init__(self, data):
        """
        Initialize the DataAnalyzer class.

        Parameters:
        data (list of str): List of data to be analyzed.
        """
        self.data = data

    def get_word_frequency(self):
        """
        Calculate the word frequency in the data.

        Returns:
        Counter: A Counter object containing word frequencies.
        """
        all_words = ' '.join(self.data).split()
        word_freq = Counter(all_words)
        return word_freq

    def get_data_statistics(self):
        """
        Get statistical information of the data, including the number of lines and words.

        Returns:
        dict: A dictionary containing the number of lines and words.
        """
        num_lines = len(self.data)
        num_words = sum(len(line.split()) for line in self.data)
        return {'num_lines': num_lines, 'num_words': num_words}

    def get_unique_words(self):
        """
        Get the unique words in the data.

        Returns:
        set: A set containing unique words.
        """
        all_words = set(' '.join(self.data).split())
        return all_words

    def get_average_line_length(self):
        """
        Calculate the average length of each line in the data (in terms of words).

        Returns:
        float: The average number of words per line.
        """
        total_words = sum(len(line.split()) for line in self.data)
        average_length = total_words / len(self.data) if self.data else 0
        return average_length

    def get_most_common_words(self, n=10):
        """
        Get the top n most common words in the data.

        Parameters:
        n (int): The number of most common words to return.

        Returns:
        list of tuple: A list containing the most common words and their frequencies.
        """
        word_freq = self.get_word_frequency()
        return word_freq.most_common(n)