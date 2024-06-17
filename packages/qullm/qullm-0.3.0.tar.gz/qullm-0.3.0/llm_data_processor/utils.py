# qullm/llm_data_processor/utils.py

import json
from typing import List

def save_data(data: List[str], file_path: str):
    """
    Save data to a specified file path.

    Parameters:
    data (List[str]): List of data to be saved.
    file_path (str): Path to save the file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(data))
    print(f"Data saved to {file_path}")

def load_config(config_path: str) -> dict:
    """
    Load a configuration file from a specified path.

    Parameters:
    config_path (str): Path to the configuration file.

    Returns:
    dict: Contents of the configuration file.
    """
    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def save_config(config: dict, config_path: str):
    """
    Save a configuration file to a specified path.

    Parameters:
    config (dict): Configuration dictionary to be saved.
    config_path (str): Path to save the configuration file.
    """
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4)
    print(f"Config saved to {config_path}")

def split_data(data: List[str], train_ratio: float = 0.8) -> (List[str], List[str]):
    """
    Split data into training and testing sets.

    Parameters:
    data (List[str]): List of data to be split.
    train_ratio (float): Proportion of data to be used as the training set.

    Returns:
    (List[str], List[str]): Training and testing data lists.
    """
    split_index = int(len(data) * train_ratio)
    train_data = data[:split_index]
    test_data = data[split_index:]
    return train_data, test_data