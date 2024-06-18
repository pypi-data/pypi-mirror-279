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
        
    def update_key(self, key_path: str, value: Any):
        """
        Updates the value of an existing key or nested key in the JSON file.

        If the key does not exist at any level, it will be added.

        Parameters:
            key_path (str): The path to the key or nested key to update in the JSON file.
                            Use dots to separate keys for nested objects.
            value (Any): The new value to associate with the key.

        Raises:
            Exception: If there is an error reading or writing to the file.
        """
        file_data = self.get()
        keys = key_path.split('/')
        data = file_data
        for key in keys[:-1]:  # Go through all keys except the last one
            data = data.setdefault(key, {})  # Set default if key does not exist
        data[keys[-1]] = value  # Set the value for the last key
        self.set(file_data)


    def add_key(self, key_path: str, value: Any):
        """
        Adds a new key-value pair to the JSON file if it does not already exist.
        Supports adding nested key-value pairs using '/' as a separator.

        Parameters:
            key_path (str): The path to the key or nested key to add to the JSON file.
                            Use '/' to separate keys for nested objects.
            value (Any): The value associated with the key in the JSON file.

        Raises:
            KeyError: If the key already exists in the JSON file at any level.
        """
        file_data = self.get()
        keys = key_path.split('/')
        data = file_data
        for key in keys[:-1]:  # Go through all keys except the last one
            if key not in data:
                data[key] = {}  # Create a new dict if key does not exist
            else:
                if not isinstance(data[key], dict):
                    raise KeyError(f"Key path {'/'.join(keys[:keys.index(key)])} is not a nested object.")
            data = data[key]
        if keys[-1] in data:
            raise KeyError(f"The key {'/'.join(keys)} already exists.")
        data[keys[-1]] = value  # Set the value for the last key
        self.set(file_data)


    def remove_key(self, key_path: str):
        """
        Removes a key-value pair or a nested key-value pair from the JSON file if it exists.
        Supports removing nested keys using '/' as a separator.

        Parameters:
            key_path (str): The path to the key or nested key to remove from the JSON file.
                            Use '/' to separate keys for nested objects.

        Raises:
            KeyError: If the key path does not exist in the JSON file at any level.
        """
        file_data = self.get()
        keys = key_path.split('/')
        data = file_data
        for key in keys[:-1]:  # Go through all keys except the last one
            if key not in data or not isinstance(data[key], dict):
                raise KeyError(f"Key path {'/'.join(keys[:keys.index(key) + 1])} does not exist.")
            data = data[key]
        if keys[-1] not in data:
            raise KeyError(f"The key {'/'.join(keys)} does not exist.")
        del data[keys[-1]]  # Remove the value for the last key
        self.set(file_data)