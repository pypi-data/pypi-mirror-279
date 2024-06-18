"""
:authors: KiryxaTech
:license Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2024 KiryxaTech
"""
import json
from pathlib import Path
from typing import Dict, Union, Any

from .Exceptions import *

class JsonFile:
    """
    A class for handling JSON file operations.

    Attributes:
        json_fp (Union[str, Path]): The path to the JSON file.
        encoding (str): The encoding of the JSON file.

    Methods:
        get() -> dict:
            Returns the content of the JSON file.
        
        set(data: dict):
            Writes the provided dictionary to the JSON file.
        
        update_key(key_path: str, value: Any):
            Updates the value of a specified key in the JSON file.
        
        add_key(key_path: str, value: Any):
            Adds a new key-value pair to the JSON file.
        
        remove_key(key_path: str):
            Removes a specified key from the JSON file.
    """
    
    def __init__(self, json_fp: Union[str, Path], encoding: str = 'utf-8'):
        if not Path(json_fp).is_file() or not str(json_fp).endswith('.json'):
            raise NotJsonFileError(json_fp)
        self.json_fp = json_fp
        self._encoding = encoding

    def _read(self) -> dict:
        with open(self.json_fp, encoding=self._encoding) as f:
            return json.load(f)

    def _write(self, data: dict):
        with open(self.json_fp, 'w', encoding=self._encoding) as f:
            json.dump(data, f, indent=4)

    def get(self) -> dict:
        """Returns the content of the JSON file."""
        return self._read()

    def set(self, data: dict):
        """Writes the provided dictionary to the JSON file."""
        self._write(data)

    def _update_dict(self, data: dict, keys: list, value: Any):
        for key in keys[:-1]:
            data = data.setdefault(key, {})
        data[keys[-1]] = value

    def _navigate_to_key(self, data: dict, keys: list) -> dict:
        for key in keys[:-1]:
            data = data[key]
        return data

    def update_key(self, key_path: str, value: Any):
        """
        Updates the value of a specified key in the JSON file.

        Args:
            key_path (str): The key path, separated by '/'.
            value (Any): The new value for the specified key.
        """
        data = self._read()
        keys = key_path.split('/')
        self._update_dict(data, keys, value)
        self._write(data)

    def add_key(self, key_path: str, value: Any):
        """
        Adds a new key-value pair to the JSON file.

        Args:
            key_path (str): The key path, separated by '/'.
            value (Any): The value for the new key.
        
        Raises:
            KeyError: If the key already exists.
        """
        data = self._read()
        keys = key_path.split('/')
        sub_data = self._navigate_to_key(data, keys)
        if keys[-1] in sub_data:
            raise KeyDuplicateError('/'.join(keys))
        sub_data[keys[-1]] = value
        self._write(data)

    def remove_key(self, key_path: str):
        """
        Removes a specified key from the JSON file.

        Args:
            key_path (str): The key path, separated by '/'.
        """
        data = self._read()
        keys = key_path.split('/')
        sub_data = self._navigate_to_key(data, keys)
        try:
            del sub_data[keys[-1]]
        except KeyError:
            raise KeyNotFoundError(key_path)
        self._write(data)


class JsonUnion(JsonFile):
    """
    A class for merging multiple JSON files or dictionaries into a single JSON file.

    Attributes:
        file_paths (Tuple[Union[str, Path,
                          Dict[Any, Any], JsonFile]]): The paths to the JSON files, dictionaries, or JsonFile objects to be merged.
        output_fp (Union[str, Path]): The file path for the output JSON file.
        replace_duplicates (bool): Determines whether duplicate keys should be replaced by the last one encountered. Defaults to False.
        _encoding (str): The encoding format used to read and write JSON files. Defaults to 'utf-8'.

    Methods:
        merge():
            Merges any number of JSON files or dictionaries and writes the result to the output
            file. If replace_duplicates is True, duplicate keys will be replaced by the last one
            encountered. Otherwise, a KeyError will be raised if duplicates are found.
    """
    
    def __init__(self, *file_paths: Union[str, Path, Dict[Any, Any], JsonFile], output_fp: Union[str, Path], replace_duplicates: bool = False, encoding: str = 'utf-8'):
        """
        Initializes the JsonUnion object with multiple JSON file paths or dictionaries.

        Args:
            *file_paths (Union[str, Path, Dict[Any, Any], JsonFile]): Variable number of arguments that can be file paths as strings or Path objects, dictionaries, or JsonFile objects.
            output_fp (Union[str, Path]): The file path for the output JSON file.
            replace_duplicates (bool): If set to True, duplicate keys will be replaced by the last one encountered. Defaults to False.
            encoding (str): The encoding format used to read and write JSON files. Defaults to 'utf-8'.
        """
        self.file_paths = file_paths
        self.json_fp = self.output_fp = output_fp
        self.replace_duplicates = replace_duplicates
        self._encoding = encoding

    def merge(self):
        """
        Merges any number of JSON files or dictionaries and writes the result to the output file.
        If replace_duplicates is True, duplicate keys will be replaced by the last one encountered.
        Otherwise, a KeyError will be raised if duplicates are found.

        Raises:
            KeyError: If replace_duplicates is False and duplicate keys are encountered.
        """
        merged_dict = {}
        for file_path in self.file_paths:
            current_dict = {}
            if isinstance(file_path, JsonFile):
                current_dict = file_path.get()
            elif isinstance(file_path, dict):
                current_dict = file_path
            elif isinstance(file_path, (str, Path)):
                with open(file_path, 'r', encoding=self._encoding) as f:
                    current_dict = json.load(f)
            
            for key in current_dict:
                if key in merged_dict and not self.replace_duplicates:
                    raise KeyDuplicateError(key)
                merged_dict[key] = current_dict[key]

        with open(self.output_fp, 'w', encoding=self._encoding) as f:
            json.dump(merged_dict, f, indent=4)