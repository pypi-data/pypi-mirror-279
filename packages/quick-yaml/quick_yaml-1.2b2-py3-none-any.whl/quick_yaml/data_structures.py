__all__ = ['NestedDict', 'BYAML', 'RecordLockManager', 'RecordLock']

import logging
import threading
import time

import jmespath
import numpy as np
import pandas as pd
import yaml
import base64
from cryptography.fernet import Fernet


class NestedDict:
    """
    A class for managing nested dictionaries with dot notation access.

    Attributes:
        _data (dict): The underlying data structure for the nested dictionary.
    """

    def __init__(self, data=None):
        """
                Initializes the NestedDict with the provided data or an empty dictionary.

                Parameters:
                    data (dict, optional): The initial dictionary data. Defaults to None, resulting in an empty dictionary.
        """
        self._data = data if data is not None else {}

    def __getitem__(self, keys):
        """Retrieve an item using a dot-separated key string."""
        current = self._data
        key_split = keys.split('.')
        for key in key_split:
            current = current[key]
        return current

    def __setitem__(self, keys, value):
        """
             Retrieves an item using a dot-separated key string.

             Parameters:
                 keys (str): The dot-separated keys.

             Returns:
                 The value associated with the specified keys.

             Raises:
                 KeyError: If any of the keys do not exist.
        """
        current = self._data
        for key in keys.split('.')[:-1]:
            current = current.setdefault(key, {})
        current[keys.split('.')[-1]] = value

    def __delitem__(self, keys):
        """
               Deletes the item at the specified dot-separated keys.

               Parameters:
                   keys (str): The dot-separated keys of the item to delete.

               Raises:
                   KeyError: If any of the keys do not exist.
         """
        keys = keys.split('.')
        current = self._data
        for key in keys[:-1]:
            if key in current:
                current = current[key]
            else:
                raise ValueError('Key Path Invalid.')  # Key path is invalid, exit the method
        # Delete the final key if it exists
        if keys[-1] in current:
            del current[keys[-1]]

    def __iter__(self):
        """
          Returns an iterator over the nested dictionary's keys and values.

          Returns:
              An iterator that yields tuples of (dot-separated key string, value).
        """
        return NestedDictIterator(self._data)

    def __len__(self):
        return len(self._data)

    def get(self, keys, default=None):
        """
        Retrieves an item, returning a default value if the specified keys do not exist.

        Parameters:
            keys (str): The dot-separated keys.
            default (optional): The value to return if the keys do not exist. Defaults to None.

        Returns:
            The value associated with the specified keys, or the default value if the keys do not exist.
        """
        try:
            return self[keys]
        except KeyError:
            return default

    def set(self, keys, value):
        """
       Sets the value at the specified dot-separated keys. Equivalent to using the item assignment.

       Parameters:
           keys (str): The dot-separated keys where the value should be set.
           value: The value to set.
        """
        self[keys] = value

    def items(self):
        return self._data.items()

    def nested_items(self, level=None):
        """
        Returns a list of tuples (key, value) for items in the nested dictionary, optionally limited to a certain depth.

        Parameters:
            level (int, optional): The maximum depth to traverse. Defaults to None, indicating no limit.

        Returns:
            A list of tuples, where each tuple contains a dot-separated key string and its corresponding value.
        """

        return list(self._traverse(level=level))

    def keys(self):
        return self._data.keys()

    def nested_keys(self, level=None):
        """
        Returns a list of keys for the nested dictionary, optionally limited to a certain depth.

        Parameters:
            level (int, optional): The maximum depth to traverse. Defaults to None, indicating no limit.

        Returns:
            A list of dot-separated key strings.
        """
        return [key for key, _ in self._traverse(level=level)]

    def values(self):

        return self._data.values()

    def _traverse(self, current=None, path=(), level=None):
        """
        Pretty prints the nested dictionary to the console, with indentation to represent nesting.

        Parameters:
            current (dict, optional): The current level of the dictionary to print. Used for recursion. Defaults to None, indicating the top level.
            indent (int, optional): The current indentation level. Defaults to 0.
        """
        current = current if current is not None else self._data
        if level is not None and len(path) > level:
            return
        for key, value in current.items():
            new_path = path + (key,)
            if isinstance(value, dict):
                yield from self._traverse(value, new_path, level)
            else:
                yield '.'.join(new_path), value

    def pretty_print(self, current=None, indent=0):
        """Pretty print the nested dictionary."""
        current = current if current is not None else self._data
        for key, value in current.items():
            print('  ' * indent + str(key) + ':', end=' ')
            if isinstance(value, dict):
                print()
                self.pretty_print(value, indent + 1)
            else:
                print(value)

    def merge(self, other, overwrite=True):
        """
        Merges another dictionary or NestedDict into this one, optionally overwriting existing values.

        Parameters:
            other (NestedDict or dict): The other dictionary to merge into this one.
            overwrite (bool, optional): Whether to overwrite existing values. Defaults to True.
        """

        for key, value in other.nested_items(level=1):
            if key not in self or overwrite:
                self.set(key, value)

    def update(self, path, update_data):
        """
          Updates data at a specified path with update_data.

          Parameters:
              path (str): The dot-separated path to the target where the update should occur.
              update_data (dict): The data to update at the target location.

          Raises:
              ValueError: If the target specified by the path is not a dictionary.
        """
        target = self.get(path, {})
        if not isinstance(target, dict):
            raise ValueError(f"Target at path '{path}' is not a dictionary")
        target.update(update_data)
        self.set(path, target)

    def path_exists(self, keys):
        """
           Checks if a path exists in the NestedDict.

           Parameters:
               keys (str): The dot-separated keys to check.

           Returns:
               True if the path exists, False otherwise.
        """
        try:
            current = self._data
            for key in keys.split('.'):
                current = current[key]
            return True
        except KeyError:
            return False

    def sort_key(self, path=None):
        """
        Sorts the dictionary by keys at the specified path or at the top level if no path is provided.

        Parameters:
            path (str, optional): The dot-separated path to the target dictionary to sort. If not provided, the top-level dictionary is sorted.
        Returns:
            A new `NestedDict` instance with the dictionary sorted at the specified path.

        """
        sorted_dict = self._sort_recursive_by_key(self._data, path.split('.') if path else [])
        return NestedDict(sorted_dict)

    def _sort_recursive_by_key(self, current, keys):
        """
        Helper method to recursively sort the dictionary.
        """
        if not keys:
            # If no more keys, sort the current dict by keys
            return {k: (self._sort_recursive_by_key(v, None) if isinstance(v, dict) else v) for k, v in
                    sorted(current.items())}
        else:
            # If there are keys, navigate further
            key = keys.pop(0)
            if key in current and isinstance(current[key], dict):
                # Sort the next level if the key exists and its value is a dict
                current[key] = self._sort_recursive_by_key(current[key], keys)
            return current

    def find(self, query):
        """
        Use a JMESPath query string to find and return items from the nested dictionary.

        Parameters:
            query (str): A JMESPath query string.

        Returns:
            The result of the JMESPath query.
        """
        return jmespath.search(query, self._data)

    def get_dict(self):
        return self._data.copy()

    def to_dict(self):
        """
        Recursively convert NestedDict into a standard dictionary.

        Returns:
            dict: A dictionary representation of the NestedDict.
        """
        result = {}
        for key, value in self._data.items():
            if isinstance(value, NestedDict):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result

    @staticmethod
    def convert_nested(d):
        """
        Recursively converts a dictionary and all of its nested dictionaries
        into NestedDict instances for easier dot operator access.

        Parameters:
            d (dict): The original dictionary to convert.

        Returns:
            NestedDict: The converted dictionary where all nested dictionaries
            are also NestedDict instances.
        """
        for key, value in d.items():
            if isinstance(value, dict):
                d[key] = NestedDict.convert_nested(value)
            # Optionally handle lists/tuples of dictionaries
            elif isinstance(value, (list, tuple)):
                d[key] = [NestedDict.convert_nested(item) if isinstance(item, dict) else item for item in value]
        return NestedDict(d)

    def __str__(self):
        """
        Returns a string representation of NestedDict that looks like a Python dictionary,
        including handling nested NestedDict instances.
        """

        def dict_str(d, indent=0):
            indent_str = ' ' * indent
            items = []
            for key, value in d.items():
                if isinstance(value, NestedDict):
                    nested_str = dict_str(value, indent + 4)
                    item_str = f"'{key}': {nested_str}"
                elif isinstance(value, dict):  # Just in case there are dict instances
                    nested_str = dict_str(value, indent + 4)
                    item_str = f"'{key}': {nested_str}"
                else:
                    item_str = f"'{key}': {repr(value)}"
                items.append(indent_str + '    ' + item_str)
            return '{\n' + ',\n'.join(items) + '\n' + indent_str + '}'

        return dict_str(self._data)

    def flat_dict(self):
        """
        Converts the nested dictionary into a flattened dictionary.

        Returns:
            dict: A flattened dictionary representation of the nested dictionary.
        """
        flat_dict = {}

        def _flatten(obj, prefix=''):
            for k, v in obj.items():
                if isinstance(v, dict):
                    _flatten(v, prefix + k + '_')
                else:
                    flat_dict[prefix + k] = v

        _flatten(self._data)
        return flat_dict

    def to_pandas(self):
        """
        Converts the nested dictionary into a pandas DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame representation of the nested dictionary.
        """
        # Use the flat_dict method to get a flattened dictionary
        flat_data = self.flat_dict()
        # Convert lists to numpy arrays if needed
        for key, value in flat_data.items():
            if isinstance(value, list):
                flat_data[key] = np.array(value)
        # Create and return a pandas DataFrame
        return pd.DataFrame([flat_data])


class NestedDictIterator:
    """
               An iterator class for NestedDict, allowing iteration over all key-value pairs in the nested dictionary.

               Attributes:
                   stack (list of tuples): A stack used for depth-first traversal of the dictionary. Each tuple contains a path (as a tuple of keys) and the current dictionary or value to process.
           """

    def __init__(self, data):

        self.stack = [((), data)]  # Initialize with a tuple of path and data

    def __iter__(self):
        """
            Initializes the NestedDictIterator with the nested dictionary data.

            Parameters:
                data (dict): The nested dictionary data to iterate over.
        """

        return self

    def __next__(self):
        """
              Returns the next key-value pair in the nested dictionary as a dot-separated key string and its value.

              Returns:
                  A tuple containing a dot-separated key string and its corresponding value.

              Raises:
                  StopIteration: If there are no more items to iterate over.
            """
        while self.stack:
            path, current = self.stack.pop()
            if isinstance(current, dict):
                for key, value in current.items():
                    new_path = path + (key,)
                    self.stack.append((new_path, value))
            else:
                return '.'.join(path), current
        raise StopIteration


class BYAML:
    """
      A class for handling the encoding and decoding of nested dictionaries into/from an encrypted or plain binary YAML format.

      Attributes:
          encryption_enabled (bool): Flag indicating whether encryption is enabled.
          key_file (str): Path to the file containing the encryption key.
          file_path (str): Path to the binary YAML file.
          cipher_suite (Fernet): A Fernet instance initialized with the encryption key, used for encrypting and decrypting data.
      """

    def __init__(self, filepath, encryption_enabled=False, key_file='key.file'):
        """
          Initializes the BYAML instance.

          Parameters:
              filepath (str): The file path for the binary YAML data.
              encryption_enabled (bool, optional): Whether to enable encryption. Defaults to False.
              key_file (str, optional): The file path for the encryption key. Defaults to 'key.file'.
        """

        self.encryption_enabled = encryption_enabled
        self.key_file = key_file
        self.file_path = filepath
        if encryption_enabled:
            self.key = self.load_key() or self.generate_and_save_key()
            self.cipher_suite = Fernet(self.key)

    def generate_and_save_key(self):
        """
          Generates a new encryption key and saves it to the key file.

          Returns:
              The generated encryption key.
        """
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as file:
            file.write(key)
        return key

    def load_key(self):
        """
           Loads the encryption key from the key file.

           Returns:
               The encryption key. None if the encryption key cannot be loaded.
        """
        try:
            with open(self.key_file, 'rb') as file:
                return file.read()
        except FileNotFoundError:
            return None  # Returning None to allow for key generation if not found

    def encode_to_binary_yaml(self, data):
        """
           Encodes the given data into binary YAML format, optionally encrypting it, and writes it to the file path.

           Parameters:
               data (NestedDict or dict): The data to encode and save.

           Raises:
               Exception: If an error occurs during the encoding or file writing process.
        """
        try:
            if type(data) is NestedDict:
                yaml_str = yaml.dump(data.to_dict())
            else:
                yaml_str = yaml.dump(data)
            binary_yaml = base64.b64encode(yaml_str.encode('utf-8'))
            if self.encryption_enabled:
                binary_yaml = self.cipher_suite.encrypt(binary_yaml)
            with open(self.file_path, 'wb+') as file:
                file.write(binary_yaml)
        except Exception as e:
            raise Exception('Exception occurred during encode to binary yaml operation.') from e

    def decode_from_binary_yaml(self, type_dict: str = 'NestedDict'):
        """
           Reads the binary YAML data from the file path, optionally decrypting it, and decodes it into a NestedDict.
           Parameters:
               type_dict: The type of dictionary either 'dictionary' or 'NestedDict'. If not specified, it defaults to 'NestedDict'.
           Returns:
               A NestedDict/Dict instance containing the decoded data.
        """
        with open(self.file_path, 'rb') as file:
            binary_yaml = file.read()
        if self.encryption_enabled:
            binary_yaml = self.cipher_suite.decrypt(binary_yaml)
        yaml_str = base64.b64decode(binary_yaml).decode('utf-8')
        data = yaml.safe_load(yaml_str)
        if type_dict == 'dict':
            return data
        return NestedDict(data)

    @staticmethod
    def convert_yaml_to_byaml(filename, encrypted=False):
        """
            Converts a YAML file to binary YAML format, optionally encrypting it.

            Parameters:
                filename (str): The path to the YAML file to convert.
                encrypted (bool, optional): Whether to encrypt the binary YAML data. Defaults to False.

            Returns:
                A tuple containing the paths to the generated binary YAML file and the key file (if encryption is enabled).
        """

        with open(filename, 'r') as f:
            x = yaml.safe_load(f)
        b = BYAML(f'{filename[:-5]}.ezdb', encrypted, f'{filename[:-5]}.key')
        b.encode_to_binary_yaml(x)
        return f'   {filename[:-5]}.ezdb', f'{filename[:-5]}.key'

    @staticmethod
    def convert_dict_to_byaml(data: dict, filename, encrypted=False):
        """Converts the dictionary to BYAML format, optionally encrypting
        Parameters:
            data (dict): The dictionary data
            filename (str): The file path as string
            encrypted (bool): Whether to encrypt the binary YAML data. Defaults to False.
        Returns:
            A string of path of the generated binary YAML file and the key file (if encrypted)
            """
        b = BYAML(f'{filename}.ezdb', encrypted, f'{filename}.key')
        b.encode_to_binary_yaml(data)
        return f'{filename}.ezdb', f'{filename}.key'


class RecordLock:
    def __init__(self):
        self.writer_lock = threading.Semaphore(1)
        self.mutex = threading.Lock()
        self.readers = 0
        self.writers = 0


class RecordLock:
    """
    A class that represents a record lock.
    Attributes:
        writer_lock (threading.Semaphore): A semaphore that controls access to the writer lock.
        mutex (threading.Lock): A lock that controls access to the readers count.
        readers (int): The number of active readers.
        writers (int): The number of active writers.
        writers_waiting (bool): A flag indicating if there are waiting writers.
    """
    def __init__(self):

        self.writer_lock = threading.Semaphore(1)  # Ensure only one writer at a time
        self.mutex = threading.Lock()  # Mutex for managing readers count
        self.readers = 0  # Counter for active readers
        self.writers = 0  # A count for writer.
        self.writers_waiting = False  # To denote waiting of writer

class RecordLockManager:
    """
    A class that manages record locks for a given database
    Attributes:
        records (dict): A dictionary of record locks by table name and record ID.
        mutex (threading.Lock): A lock that controls access to the records dictionary.
        logger (logging.Logger): A logger instance for logging purposes.


    """
    def __init__(self, logger=None, create_logger=False):

        self.records = {}  # Dictionary for storing locks by table name and record ID
        self.mutex = threading.Lock()  # Global mutex for synchronizing lock creation
        self.logger = logger or self._setup_default_logger(create_logger)

    def _setup_default_logger(self, create_logger):
        if create_logger:
            logger = logging.getLogger("RecordLockManager")
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
            return logger
        return None

    def make_record_lock(self, table_name, record_id):
        """
        Creates a new record lock for the given table and record ID.
        Parameters:
            table_name (str): The name of the table.
            record_id (str): The ID of the record.
        """

        if table_name not in self.records:
            self.records[table_name] = {}
        if record_id not in self.records[table_name]:
            self.records[table_name][record_id] = RecordLock()
            self.logger.debug(f"Record lock created for {table_name} ID: {record_id}")

    def acquire_writer_lock(self, table_name, record_id):
        """
        Acquires a writer lock for the given table and record ID.
        Parameters:
            table_name (str): The name of the table.
            record_id (str): The ID of the record.
        Returns:
            None
        """
        with self.mutex:
            self.make_record_lock(table_name, record_id)
        lock = self.records[table_name][record_id]
        lock.writers_waiting = True
        self.logger.debug(f"Writer waiting to acquire lock for {table_name} record {record_id}")    
        lock.writer_lock.acquire()
        lock.writers_waiting = False
        lock.writers += 1
        self.logger.debug(
            f"Writer acquired lock for {table_name} record {record_id}. Active writers: {lock.writers}")

    def release_writer_lock(self, table_name, record_id):
        """
        Releases a writer lock for the given table and record ID.

        Parameters:
            table_name (str): The name of the table.
            record_id (str): The ID of the record.

        Returns:
             None
        """
        lock = self.records[table_name][record_id]
        with lock.mutex:
            lock.writers -= 1
        lock.writer_lock.release()
        self.logger.debug(
            f"Writer released lock for {table_name} record {record_id}. Remaining writers: {lock.writers}")

    def acquire_reader_lock(self, table_name, record_id):
        """
        Acquires a reader lock for the given table and record ID.
        Parameters:
            table_name (str): The name of the table.
            record_id (str): The ID of the record.
        Returns:
            None

        """
        lock = self.records[table_name][record_id]
        with lock.mutex:
            while lock.writers_waiting:
                lock.mutex.release()
                time.sleep(0.1)
                lock.mutex.acquire()
            lock.readers += 1
            if lock.readers == 1:
                lock.writer_lock.acquire()
        self.logger.debug(f"Reader acquired lock for {table_name} record {record_id}, total readers: {lock.readers}")

    def release_reader_lock(self, table_name, record_id):
        """
        Releases a reader lock for the given table and record ID.
        Parameters:
            table_name (str): The name of the table.
            record_id (str): The ID of the record.
        Returns:
            None
        """
        lock = self.records[table_name][record_id]
        with lock.mutex:
            lock.readers -= 1
            if lock.readers == 0:
                lock.writer_lock.release()
        self.logger.debug(
            f"Reader released lock for {table_name} record {record_id}, remaining readers: {lock.readers}")

    def delete_lock_id(self, table_name, record_id):
        """
        Deletes the record lock for the given table and record ID.

        Parameters:
            table_name (str): The name of the table.
            record_id (str): The ID of the record.

        Returns:
            None
        """
        if table_name in self.records and record_id in self.records[table_name]:
            del self.records[table_name][record_id]
            self.logger.debug(f"Record lock deleted for {table_name} ID: {record_id}")

    def delete_lock_table(self, table_name):
        """
        Deletes all record locks for the given table.
        Parameters:
            table_name (str): The name of the table.
        Returns:
            None
        """
        with self.mutex:
            if table_name in self.records:
                for record_id in list(self.records[table_name].keys()):
                    self.release_reader_lock(table_name, record_id)
                    self.release_writer_lock(table_name, record_id)
                del self.records[table_name]
                self.logger.debug(f"All record locks deleted for {table_name}")
