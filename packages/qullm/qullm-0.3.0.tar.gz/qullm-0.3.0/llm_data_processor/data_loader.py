# qullm/llm_data_processor/data_loader.py

import os

class DataLoader:
    def __init__(self, file_path: str):
        """
        Initialize the DataLoader class.

        Parameters:
        file_path (str): The path to the data file.
        """
        self.file_path = file_path

    def load_data(self) -> list:
        """
        Load data from the specified file path.

        Returns:
        list: A list containing each line of data.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} does not exist.")
        
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = file.readlines()
        
        return data

    def load_data_as_string(self) -> str:
        """
        Load data from the specified file path and return it as a string.

        Returns:
        str: A string containing the entire file content.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} does not exist.")
        
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        
        return data

    def load_data_as_lines(self) -> list:
        """
        Load data from the specified file path and return a list of strings, each representing a line of data.

        Returns:
        list: A list of strings, each containing a line of data.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} does not exist.")
        
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = file.read().splitlines()
        
        return data