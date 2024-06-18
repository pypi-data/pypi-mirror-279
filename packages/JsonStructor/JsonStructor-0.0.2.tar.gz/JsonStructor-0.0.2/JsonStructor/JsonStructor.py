"""
:authors: KiryxaTech
:license Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2024 KiryxaTech
"""
import json
from pathlib import Path
from typing import Union, Any


class JsonFile:
    """
    A class to handle reading and writing JSON files.
    
    Attributes:
        __json_fp (Union[str, Path]): The file path to the JSON file.
        __encoding (str): The encoding format used to read/write the file.
        
    Methods:
        get: Reads and returns the content of the JSON file.
        set: Writes a dictionary to the JSON file.
        add_new_key: Adds a new key-value pair to the JSON file.
        remove_key: Removes a key-value pair from the JSON file.
        replace_value: Replaces the value of an existing key in the JSON file.
    """
    def __init__(self, json_fp: Union[str, Path], encoding: str = 'utf-8'):
        """
        Initializes the JsonFile object with a file path and encoding.
        
        Parameters:
            json_fp (Union[str, Path]): The file path to the JSON file.
            encoding (str): The encoding format used to read/write the file.
            
        Raises:
            ValueError: If the provided file path does not point to a .json file.
        """
        if not Path(json_fp).is_file() or not str(json_fp).endswith('.json'):
            raise ValueError("The file path must point to a .json file.")
        self.__json_fp = json_fp
        self.__encoding = encoding

    def get(self) -> dict:    
        """
        Reads and returns the content of the JSON file as a dictionary.
        
        Returns:
            dict: The content of the JSON file.
            
        Raises:
            FileNotFoundError: If the JSON file does not exist.
            json.JSONDecodeError: If the JSON file cannot be decoded.
        """
        try:
            with open(self.__json_fp, encoding=self.__encoding) as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {self.__json_fp} does not exist.")
        except json.JSONDecodeError:
            raise json.JSONDecodeError("Failed to decode JSON.")

    def set(self, data: dict):
        """
        Writes a dictionary to the JSON file.
        
        Parameters:
            data (dict): The data to write to the JSON file.
            
        Raises:
            Exception: If there is an error writing to the file.
        """
        try:
            with open(self.__json_fp, 'w', encoding=self.__encoding) as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            raise e
        
    def update_key(self, key: str, value: Any):
        """
        Updates the value of an existing key in the JSON file.

        If the key does not exist, it will be added to the file.

        Parameters:
            key (str): The key to update in the JSON file.
            value (Any): The new value to associate with the key.

        Raises:
            Exception: If there is an error reading or writing to the file.
        """
        file_data = self.get()
        file_data[key] = value
        self.set(file_data)


    def add_key(self, new_key: str, value: Any):
        """
        Adds a new key-value pair to the JSON file if it does not already exist.
        
        Parameters:
            new_key (str): The key to add to the JSON file.
            value (Any): The value associated with the key in the JSON file.
            
        Raises:
            KeyError: If the key already exists in the JSON file.
        """
        file_data = self.get()
        if new_key in file_data:
            raise KeyError(f"The key {new_key} already exists.")
        file_data[new_key] = value
        self.set(file_data)

    def remove_key(self, key_to_remove: str):
        """
        Removes a key-value pair from the JSON file if it exists.

        Parameters:
            key_to_remove (str): The key to remove from the JSON file.

        Raises:
            KeyError: If the key does not exist in the JSON file.
        """
        file_data = self.get()
        if key_to_remove not in file_data:
            raise KeyError(f"The key {key_to_remove} does not exist.")
        del file_data[key_to_remove]
        self.set(file_data)