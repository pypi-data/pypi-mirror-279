__all__ = ['QYAMLDB', 'QYAMLDBCoarse', 'MetaData', 'QYAMLDBFine']

import logging
import time
from threading import Semaphore, Lock

import jmespath
import sys

from .data_structures import BYAML, NestedDict, RecordLockManager
from .parser import QueryProcessor
import pandas as pd
import copy
import matplotlib.pyplot as plt

class MetaData:
    """
    A class for storing table metadata

    Attributes:
        - version (float): The version of the metadata.
        - unique_columns (list): A list of unique columns for the table.
        - indexes (list): A list of indexes for the table.
    """

    def __init__(self):
        """
        Initialize the object with an empty dictionary for storing tables.
        """
        self.tables = {}  # A dictionary to hold table-specific metadata
        self._lock = Lock()  # Internal Semaphore for synchronizing access to the metadata.

    def add_table(self, table_name, default_values=None, unique_columns=None, indexes=None):
        """
        Add a new table to the metadata.
        Parameters:
            table_name (str): The name of the table.
            default_values: A dictionary of default values for the table.
            unique_columns (list): A list of unique columns for the table.
            indexes (list): A list of indexes for the table.
        Returns:
            None

        """

        with self._lock:
            self.tables[table_name] = {
                'version': 1.1,
                'unique_columns': unique_columns or [],
                'default_values': default_values or {},
                'indexes': indexes or []
            }

    def to_dict(self):
        """
        Return a dictionary representation of the object.
        """

        return self.tables

    def get_unique_columns(self, table_name):
        """Returns the unique columns for the given table."""
        with self._lock:
            data = self.tables[table_name]['unique_columns']
        return data

    def get_indexes(self, table_name):
        """Returns the indexes for the given table."""
        with self._lock:
            data = self.tables[table_name]['indexes']

        return data

    def __deepcopy__(self, memo):
        # Create a new instance of the same class
        new_obj = type(self)()
        # Explicitly copy the dictionary to the new instance
        new_obj.tables = copy.deepcopy(self.tables, memo)
        # Do not copy the lock, just create a new lock
        new_obj._lock = Lock()
        return new_obj

    def add_default_values(self, table_name, default_values):
        """Adds default key and value to the table
        Parameters:
            table_name (str): The name of the table.
            default_values: A dictionary of default values for the table to be added.
        Returns:
            None
         """
        # Get table MetaDATA'
        with self._lock:
            meta = self.tables[table_name]
            # check if default Values is declared if not add it
            if 'default_values' not in self.tables[table_name]:
                self.tables[table_name]['default_values'] = {}

            # Now for each key in default_values check if the key is in unique_columns
            for k, v in default_values.items():
                if k in meta['unique_columns']:
                    raise ValueError(f"Default value for {k} is not allowed as it is a unique column")

            self.tables[table_name]['default_values'].update(default_values)

    def add_unique_column(self, table_name, unique_columns):
        """Adds unique column to the table
        Parameters:
            table_name (str): The name of the table.
            unique_columns: A list of unique columns for the table to be added.
        Returns:
            None
         """

        with self._lock:
            # check if default Values is declared if not add it
            if 'unique_columns' not in self.tables[table_name]:
                self.tables[table_name]['unique_columns'] = []

            self.tables[table_name]['unique_columns'].extend(unique_columns)


class QYAMLDB:
    """
    A simple and easy-to-use database manager without thread safety

    Attributes:
        - path (str) : path of database
        - key_file (str): path of key file
        - encrypted (bool): flag indicating if encryption is enabled
        - byaml (BYAML): BYAML instance
        - log_file (str): path of log file
        - enable_logging (bool): flag indicating if logging is enabled
        - log_level (int): level of logging
        - silent (bool): flag indicating if logging is silent

    Methods:
        - __init__: Initialize the database.
        - add_table: Add a table to the database.
        - insert_data: Insert data into a specified table.
        - execute_query: Query data from a specified table.
        - delete_data: Delete data from a specified table.
    """

    def __init__(self, path, key_file='key.file', encrypted=False, byaml=None, log_file='qyaml.log',
                 enable_logging=True,
                 log_level=logging.DEBUG, silent=False):
        """
          Initializes the quick_yaml instance.
          Parameters:
              path (str): The file path for the database.
              key_file (str): The file path for the encryption key. Defaults to 'key.file'.
              encrypted (bool): Flag indicating whether encryption is enabled. Defaults to False.
              byaml (BYAML): An existing BYAML instance. If not provided, a new BYAML instance is created.
          Raises:
              ValueError: If the file format is invalid.
          Returns:
              None
          """

        if not path.endswith('.ezdb'):
            raise ValueError('Invalid file format. Must use ".ezdb" extension.')
        self.path = path
        self.key_file = key_file
        self.encrypted = encrypted
        self.logger_enabled = enable_logging
        self._backup_table = None
        self.byaml = byaml or BYAML(self.path, encryption_enabled=self.encrypted, key_file=self.key_file)
        self.tables: dict = {}  # Use a dict to manage multiple tables, each with its data and metadata4
        # Logging Operations
        if enable_logging:
            self._setup_logger(log_file, log_level, not silent)
        else:
            self._logger = logging.getLogger('QYAMLDB')
            self._logger.addHandler(logging.NullHandler())

    def _setup_logger(self, log_file, log_level, print_to_console):
        self._logger = logging.getLogger('QYAMLDB')
        self._logger.setLevel(log_level)
        # Include milliseconds in the formatter
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        fh = logging.FileHandler(log_file)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        self._logger.addHandler(fh)
        if print_to_console:
            ch = logging.StreamHandler()
            ch.setLevel(log_level)
            ch.setFormatter(formatter)
            self._logger.addHandler(ch)

    def _log(self, message, level='debug'):
        if self.logger_enabled:
            getattr(self._logger, level)(message)

    def save_db(self):
        """Saves the current state of the database to a file."""

        self._log(f"Saving database to {self.path}", 'info')

        try:
            to_save = {table_name: {'metadata': table_info['metadata'].to_dict(),
                                    'data': table_info['data'].to_dict()} for table_name, table_info in
                       self.tables.items()}

            self.byaml.encode_to_binary_yaml(to_save)

            self._log(f"Saved database to {self.path}", 'info')
        except Exception as e:
            self._log(f"Failed to save database: {e}", 'error')

    def create_table(self, table_name, unique_columns=None, indexes=None):
        """
        Creates a new table in the database.

        Parameters:
            table_name (str): The name of the table to create.
            unique_columns (list, optional): List of column names that should be unique. Defaults to None.
            indexes (list, optional): List of column names to index. Defaults to None.
        Returns:
            str: "done." if the table is created successfully.
        Raises:
            ValueError: If the table already exists.
        """
        if table_name in self.tables:
            self._log(f"Table '{table_name}' already exists.", 'error')
            raise ValueError(f"Table '{table_name}' already exists.")
        metadata = MetaData()
        metadata.add_table(table_name, unique_columns, indexes)  # MetaData is adjusted to handle this
        self.tables[table_name] = {
            'metadata': metadata,
            'data': NestedDict()
        }
        self.save_db()
        self._log(f"Created table '{table_name}'.", 'info')
        return "done."

    def load_db(self):
        """
        Load the database by decoding the contents from binary YAML and populating the tables dictionary with metadata
         and data.

        Returns:
            None
        """
        contents = self.byaml.decode_from_binary_yaml(type_dict='dict')

        try:
            for table_name, table_info in contents.items():
                metadata = MetaData()
                metadata.tables[table_name] = table_info['metadata']  # Properly load metadata
                self.tables[table_name] = {
                    'metadata': metadata,
                    'data': NestedDict(table_info['data'])
                }
        except Exception:
            print("WARNING CANNOT LOAD META DATA")

    def generate_new_id(self, table_name):
        """
        Generates new ID for records
        """
        # Get existing IDs as integers
        existing_ids = [int(key) for key in self.tables[table_name]['data'].get_dict().keys()]

        # Find missing IDs if there are any gaps
        missing_ids = [i for i in range(1, max(existing_ids) + 1) if i not in existing_ids] if existing_ids else []

        # Use the first missing ID if available; otherwise, use the next highest ID
        entry_id = str(missing_ids[0]) if missing_ids else str(max(existing_ids) + 1 if existing_ids else 1)

        return entry_id

    def insert_new_data(self, table_name, data):
        """
        Insert new data into the specified table.

        Parameters:
            table_name (str): Name of the table to insert data into.
            data (dict): Data to be inserted into the table.

        Returns:
            str: A message indicating the insertion operation is done.

        Raises:
            ValueError: If the table does not exist or if a unique constraint is violated.
        """
        # TODO: Work using Default meta data
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        # Check for unique constraints
        unique_columns = self.tables[table_name]['metadata'].get_unique_columns(table_name)
        for column in unique_columns:
            if column in data and any(
                    data[column] == row.get(column) for row in self.tables[table_name]['data'].get_dict().values()):
                raise ValueError(f"Unique constraint violated for column: {column}")

        entry_id = self.generate_new_id(table_name)
        # Insert the data with the new entry_id
        self.tables[table_name]['data'][entry_id] = data
        self.save_db()
        return 'done'

    def insert_many(self, table_name, list_of_values):
        """
        Insert multiple values into the specified table.
        Parameters:
            table_name (str): Name of the table to insert data into.
            list_of_values (list): List of values to be inserted into the table.
        Returns:
            str: A message indicating the insertion operation is done.
        """
        try:
            for i in list_of_values:
                if type(i) is dict or isinstance(i, NestedDict):
                    self.insert_new_data(table_name, i)

            return 'done'
        except Exception:
            print("Error inserting values")

    def get_data_by_id(self, table_name, entry_id):
        """
        A function that retrieves data by ID from a specific table.

        Parameters:
            table_name (str): The name of the table to retrieve data from.
            entry_id (int): The ID of the entry to retrieve.

        Returns:
            contents: The data associated with the provided entry ID in the specified table.
        """
        if table_name not in self.tables:
            raise ValueError(f"Table Not found.")
        contents = self.tables[table_name]['data'].get(str(entry_id), None)
        return contents

    def update_entry(self, table_name, entry_id, updated_data):
        """Updates the data by given ID.
        Parameters:
            table_name (str): Name of the table
            entry_id (str): ID of the entry
            updated_data (NestedDict/Dict): Data to be updated.
        """
        if table_name not in self.tables or entry_id not in self.tables[table_name]['data'].get_dict():
            raise ValueError("Table or entry does not exist.")
        print(
            f"DEBUG Table {self.tables[table_name]['data'][entry_id]} type{type(self.tables[table_name]['data'][entry_id])}")
        if entry_id not in self.tables[table_name]['data'].keys():
            return KeyError("Entry does not exist.")
        self.tables[table_name]['data'][entry_id].update(updated_data)
        self.save_db()
        return 'done'

    def update_many(self, table_name, condition, update_data, flags=None):
        """ Updates data based on given condition
        Parameters:
            condition (dict): Filtering Conditions.
            update_data (dict): Data to be updated
            flags: Additional flags (Supported: { add_missing_values : 'True'/False})
            table_name: name of table """
        if flags is None:
            flags = {'add_missing_values': True}
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        # Retrieve the metadata to check for unique constraints
        unique_columns = self.tables[table_name]['metadata'].get_unique_columns(table_name)
        qp = QueryProcessor(self.tables[table_name]['data'])
        qp.filter_id(condition)
        matching_ids = qp.results

        if not matching_ids:
            return None  # No data matching the condition

        for entry_id in matching_ids:
            current_entry = self.tables[table_name]['data'].get(entry_id)

            for key, value in update_data.items():
                # Check if the key exists in the entry or if missing keys should be added
                if key in current_entry or flags.get('add_missing_keys', False):
                    # Check for unique constraints
                    if key in unique_columns and any(
                            value == row.get(key) for row in self.tables[table_name]['data'].get_dict().values()
                            if row.get(key) is not None and str(row.get('id')) != entry_id):
                        raise ValueError(f"Unique constraint violated for column: {key}")

                    # Update or add the key-value pair
                    if isinstance(value, dict) and isinstance(current_entry.get(key, None), dict):
                        # For nested dicts, update sub-keys
                        current_entry[key].update(value)
                    else:
                        current_entry[key] = value

            # Update the entry in the dataset
            self.tables[table_name]['data'][entry_id] = current_entry

        self.save_db()
        return 'done'

    def delete_entry(self, table_name, entry_id):
        """
        Delete an entry from a specified table.
        Parameters:
            table_name (str): The name of the table to delete the entry from.
            entry_id (str): The unique identifier of the entry to be deleted.

        Raises:
            ValueError: If the table or entry does not exist.
            KeyError: If the entry does not exist.

        Returns:
            str: "done" if the deletion is successful.
        """
        if table_name not in self.tables or entry_id not in self.tables[table_name]['data'].get_dict().keys():
            raise ValueError("Table or entry does not exist.")
        if entry_id not in self.tables[table_name]['data']:
            return KeyError("Entry does not exist.")
        del self.tables[table_name]['data'][entry_id]
        self.save_db()
        return "done"

    def delete_many(self, table_name, condition):
        """
           Delete multiple records from a table based on a given condition.
           Parameters:
               table_name (str): The name of the table to delete records from.
               condition (dict): The condition to filter the records to be deleted.
           Raises:
               ValueError: If the table does not exist in the database.
           Returns:
               str: A message confirming the deletion process is done.
           """
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        # Retrieve the metadata to check for unique constraints
        qp = QueryProcessor(self.tables[table_name]['data'])
        qp.filter_id(condition)
        matching_ids = qp.results
        # for each matching records, delete the record
        for entry_id in matching_ids:
            del self.tables[table_name]['data'][entry_id]
        self.save_db()
        return "done"

    def find_jmes(self, table_name, query: str):
        """
        Finds data in the specified table based on a query.
        This uses Jmespath query to find the data in the dictionary
        Parameters:
            table_name (str): The name of the table to search in.
            query (dict): The query to filter the data.
        Returns:
            list: The results of the query execution.
        Raises:
            ValueError: If the table does not exist in the database.
        """
        # Placeholder for query processing logic
        if table_name not in self.tables:
            raise ValueError("Table or entry does not exist.")

        data_list = list(self.tables[table_name]['data'].get_dict().values())

        return jmespath.search(query, data_list)

    def execute_query(self, table_name, query):
        """
           Executes a query on a specific table and returns the results.

           Parameters:
               table_name (str): The name of the table to execute the query on.
               query (dict): The query to be executed.

           Returns:
               dict: The results of the query execution.
           """
        # check if table exists
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")
        data = self.tables[table_name]['data'].to_dict()
        executor = QueryProcessor(data)
        executor.process_query(query)

        return executor.results

    def find(self, table_name, query):
        """
           Finds and filters data in the specified table based on a query.
           Parameters:
               table_name (str): The name of the table to search in.
               query (dict): The query to filter the data.
           Returns:
               dict: The filtered results based on the query.
           """
        data = self.tables[table_name].to_dict()
        executor = QueryProcessor(data)
        executor.filter(query)
        return executor.results

    def find_all(self, table_name):
        """
        Returns all the data in the specified table.
        Parameters:
            table_name (str): The name of the table to search in.
        Returns:
            list: The results of the query execution.
        """
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")
        return self.tables[table_name]['data'].values()

    def to_pandas(self, table_name):
        """
        Converts the specified table data into a pandas DataFrame.

        Parameters:
            table_name (str): The name of the table to convert.

        Returns:
            pandas.DataFrame: The converted DataFrame.

        Raises:
            ValueError: If the table does not exist in the database.
        """
        if table_name not in self.tables:
            self._log(f"Executed method to_pandas. Table '{table_name}' does not exist.", 'error')
            raise ValueError(f"Table '{table_name}' does not exist.")

        # Extract data from the specified table
        data = self.tables[table_name]['data'].to_dict()

        # Flatten the data and convert it into a format suitable for DataFrame creation
        flattened_data = []
        for entry_id, entry_data in data.items():
            entry_data_flat = {'obj_id': entry_id}
            for key, value in entry_data.items():
                if isinstance(value, list):
                    entry_data_flat[key] = ', '.join(map(str, value))  # Convert lists to comma-separated strings
                else:
                    entry_data_flat[key] = value
            flattened_data.append(entry_data_flat)

        # Create and return the DataFrame
        df = pd.DataFrame(flattened_data)
        self._log(f'Result {df}')
        return df

    # MetaData Methods
    def get_metadata(self, table_name):
        return copy.deepcopy(self.tables[table_name]['metadata'])

    def update_meta_data(self, table_name, data):
        # Update Metadata
        self.tables[table_name]['metadata'].update(data)

    def begin_transaction(self, data):
        """
        Emulates a transaction processing system.

        Parameters:
            data (dict): Dictionary data to be processed

        Raises:
            ValueError: If the error strategy is not one of the valid values.

        Returns:
            dict: A dictionary containing the status, error message, and transaction details.
        """

        # Create a backup copy of the tables
        self._backup_table = copy.deepcopy(self.tables)

        # Initialize transaction report
        transaction_report = {
            'successful_operations': 0,
            'failed_operation': 0,
            'results': [],  # To store the results
            'list_of_failed_operations_id': []  # The operation id is jus the index of data
        }
        # TODO Improve transaction function.

        # Get the transactional data and error strategy from input data
        transactional_data = data.get('$operations', [])
        error_strategy = data.get('$error_strategy', 'rollback')
        on_invalid_command = data.get('$on_invalid_command', 'rollback')

        # Ensure error_strategy is valid
        if error_strategy not in ('rollback', 'continue', 'break'):
            error_strategy = 'rollback'

        transaction_id = 0
        for i in transactional_data:

            transaction_id += 1
            try:

                status = self.execute_command(i)
                print(status)
                transaction_report['results'].append(status)
                if status == 'Invalid command':
                    if on_invalid_command == 'rollback':
                        self.tables = self._backup_table
                        transaction_report['failed_operation'] += len(transactional_data) - transaction_report[
                            'successful_operations']
                        return {'status': 'Failure', 'error_message': 'Invalid command', 'details': transaction_report}
                    elif on_invalid_command == 'break':
                        transaction_report['failed_operation'] += len(transactional_data) - transaction_report[
                            'successful_operations']
                        return {'status': 'Failure', 'error_message': 'Invalid command', 'details': transaction_report}
                    elif on_invalid_command == 'continue':
                        transaction_report['list_of_failed_operations_id'].append(transaction_id)
                        continue
                transaction_report['successful_operations'] += 1
            except Exception as e:
                if error_strategy == 'rollback':
                    self.tables = self._backup_table
                    self.save_db()  # Save roll-backed DB.
                    del self._backup_table
                    transaction_report['failed_operation'] += len(transactional_data) - transaction_report[
                        'successful_operations']
                    # Print Stack Trace
                    import traceback
                    traceback.print_exc()
                    return {'status': 'Failure', 'error_message': str(e), 'details': transaction_report}
                elif error_strategy == 'break':
                    transaction_report['failed_operation'] += len(transactional_data) - transaction_report[
                        'successful_operations']
                    return {'status': 'Failure', 'error_message': str(e), 'details': transaction_report}
                elif error_strategy == 'continue':
                    transaction_report['list_of_failed_operations_id'].append(transaction_id)
                    continue

        # Determine final status based on failed operations
        stat = "Success" if len(transaction_report['list_of_failed_operations_id']) == 0 else "Finished with errors"
        print(transaction_report)
        return {'status': stat, 'error_message': None, 'details': transaction_report}

    def execute_command(self, i):
        """
        Execute a command based on the given input type.
        Parameters:
            i (dict): The input command to be executed.
        Returns:
            str: The result of the executed command.
        """
        translation_operations = ['$insert', '$insert_many', '$update', '$update_many', '$delete'
            , '$delete_many', '$del_many', '$del', '$get_by_id', '$upate_meta_data', '$find', '$create_table',
                                  '$insert_meta_data', '$query']
        op_type = i['type']
        if op_type not in translation_operations:
            return "Invalid operation detected."
        if op_type == '$insert':
            return self.insert_new_data(i['$table_name'], i['$data'])
        elif op_type == '$insert_many':
            return self.insert_many(i['$table_name'], i['data'])
        elif op_type == '$find':
            return self.find(i['$table_name'], i['$query_data'])
        elif op_type == '$get_by_id':
            return self.get_data_by_id(i['$table_name'], i['$obj_id'])
        elif op_type == '$update':
            return self.update_entry(i['$table_name'], i['$obj_id'], i['$data'])

        elif op_type == '$update':
            return self.update_many(i['$table_name'], i['$obj_id'], i['$data'])
        elif op_type == '$update_many':
            return self.update_many(i['$table_name'], i['$condition'], i['$data'], i.get('$flags',
                                                                                         {'add_missing_values': True}))
        elif op_type == '$delete' or op_type == '$del':
            return self.delete_entry(i['$table_name'], i['$obj_id'])
        elif op_type == '$delete_many' or op_type == '$del_many':
            return self.delete_many(i['$table_name'], i['$condition'])
        elif op_type == '$create_table':

            return self.create_table(i['$table_name'], i.get('$unique_columns', None), i.get('$default_values', None))
        elif op_type == '$query':
            return self.execute_query(i['$table_name'], i['$query_data'])


class QYAMLDBCoarse(QYAMLDB):
    """
   QYAMLDBCoarse is a subclass designed to handle locks in a coarse-grained manner. This is ideal for environments
    where simplicity and preventing race conditions are prioritized over operation throughput. This consist of

    Inherits from:
        QYAMLDB: The base class for database operations.


    Attributes:
        - _mutex (threading.Semaphore): A semaphore used to synchronize access to the database.
        - _writers_lock (threading.Semaphore): A semaphore used to synchronize access to the writers.
        - _readers (int): The number of _readers currently accessing the database.

    """

    # include all the arguments from base class
    def __init__(self, path, key_file='key.file', encrypted=False, byaml=None, log_file='qyaml.log',
                 enable_logging=True,
                 log_level=logging.DEBUG, silent=False):
        super().__init__(path, key_file, encrypted, byaml, log_file, enable_logging, log_level, silent)

        self._mutex = Semaphore(1)
        self._writers_lock = Semaphore(1)
        self._readers = 0
        self._writers_waiting = False
        self._data_lock = Lock()
        self.logger_enabled = enable_logging

    def _start_write(self, agent='Writer'):
        """
        Function to acquire the writer lock.
        """
        self._log(f'{agent} Waiting to acquire writer lock. With {self._readers} _readers', 'debug')
        with self._mutex:
            self._writers_waiting = True

        self._log(f'{agent} Acquired writer lock. With {self._readers} _readers', 'debug')
        self._writers_lock.acquire()

    def _end_write(self, agent='Writer'):
        """
        Function to release the writer lock.
        """
        self._log(f'Releasing writer lock. With {self._readers} _readers', 'debug')
        self._writers_lock.release()

        with self._mutex:
            self._writers_waiting = False

        self._log(f'Released writer lock.With {self._readers} _readers', 'debug')

    def _start_read(self):
        """
        Function to acquire the reader lock.
        """
        self._log('Waiting to acquire reader lock', 'debug')
        self._mutex.acquire()  # Acquire mutex lock to synchronize readers attaining lock
        while self._writers_waiting:
            # Release all the readers until writers are finished.
            self._log(f'Lock Released due to waiting of writers. No of _readers {self._readers}')
            self._mutex.release()  # Release mutex in favor of writers
            time.sleep(0.1)  # Sleep to prevent busy waiting
            self._mutex.acquire()  # Again Try to acquire locks.

        self._log('Acquired reader lock', 'debug')
        self._readers += 1

        if self._readers == 1:
            self._log('Waiting for writers lock by _readers', 'debug')
            self._writers_lock.acquire()
            self._log('Writers Lock acquired by _readers.', 'debug')
        self._mutex.release()
        self._log(f'No of _readers {self._readers}', 'debug')

    def _end_read(self):
        """Function to release reader lock."""
        self._log('Releasing reader lock', 'debug')
        self._mutex.acquire()

        self._readers -= 1
        self._log(f'Released reader lock. No of Readers {self._readers}', 'debug')
        if self._readers == 0:
            self._writers_lock.release()
        self._mutex.release()

    def create_table(self, table_name, unique_columns=None, indexes=None):
        """
        Thread-safe version of create_table.
        Parameters:
            table_name (str): The name of the table to create.
            unique_columns (list, optional): List of column names that should be unique. Defaults to None.
            indexes (list, optional): List of column names to index. Defaults to None.

        Returns:
            str: "done." if the table is created successfully.

        Raises:
            Exception: If the table already exists.
        """
        self._start_write()
        result = None
        try:
            result = super().create_table(table_name, unique_columns, indexes)
        except Exception as e:
            result = e
        finally:
            self._end_write()  # Ensure that lock is released despite exceptions
        if isinstance(result, Exception):
            raise result

        return result

    def insert_new_data(self, table_name, data):
        """
        Thread-safe version of insert_data.
        Parameters:
            table_name (str): The name of the table to insert into.
            data (dict): The data to insert.

        Returns:
            str: "done." if the data is inserted successfully.

        Raises:
            Exception: If the table is not found.
        """
        self._start_write()
        result = None
        try:
            result = super().insert_new_data(table_name, data)
        except Exception as e:
            result = e
        finally:
            self._end_write()

        if isinstance(result, Exception):
            raise result
        return result

    def insert_many(self, table_name, data):
        """
        Thread-safe version of insert_many.
        Beware of this function is not ACID compliant. Use begin_translation if you need ACID compliance.
        Parameters:
            table_name (str): The name of the table to insert into.
            data (list): The data to insert.

        Returns:
            str: "done." if the data is inserted successfully.

        Raises:
            ValueError: When the data is not found or it violates unique constraint.
        """
        self._start_write()
        try:
            result = super().insert_many(table_name, data)
        except Exception as e:
            result = e
        finally:
            self._end_write()

        if isinstance(result, Exception):
            raise result

        return result

    def update_entry(self, table_name, entry_id, updated_data):
        """
        Thread-safe version of update_entry.

        Parameters:
            table_name (str): The name of the table to update.
            entry_id (str): The ID of the entry to update.
            updated_data (dict): The data to update.

        Returns:
            str: "done." if the update is successful.

        Raises:
            ValueError: If the table or entry does not exist.
        """
        self._start_write()
        results = None
        try:
            results = super().update_entry(table_name, entry_id, updated_data)
        except Exception as e:
            results = e
        finally:
            self._end_write()

        if isinstance(results, Exception):
            raise results

        return results

    def update_many(self, table_name, condition, updated_data, flags=None):
        """
        Thread-safe version of update_many.
        Beware of this function is not ACID compliant. Use begin_translation if you need ACID compliance.

        Parameters:
            table_name (str): The name of the table to update.
            condition (dict): The condition to match on.
            updated_data (dict): The data to update.
            flags (dict, optional): The flags to use. Defaults to None.

        Returns:
            str: "done." if the update is successful.

        Raises:
            ValueError: If the table or entry does not exist.
        """
        self._start_write()
        result = None
        try:
            result = super().update_many(table_name, condition, updated_data, flags)
        except Exception as e:
            result = e
        finally:
            self._end_write()

        if isinstance(result, Exception):
            raise result

        return result

    def delete_entry(self, table_name, entry_id):
        """
        Thread-safe version of delete_entry.

        Parameters:
            table_name (str): The name of the table to delete from.
            entry_id (str): The unique identifier of the entry to be deleted.

        Returns:
            str: "done." if the deletion is successful.

        Raises:
            ValueError: If the table or entry does not exist.
        """
        self._start_write()
        result = super().delete_entry(table_name, entry_id)
        self._end_write()
        return result

    def delete_many(self, table_name, query):
        """
        Thread-safe version of delete_many
        Parameters:
            table_name (str): The name of the table to delete from.
            query (dict): The query to filter the records to be deleted.

        Returns:
            str: "done." if the data is deleted successfully.

        Raises:
            Exception: If the table is not found.

        """
        self._start_write()
        try:
            result = super().delete_many(table_name, query)
        except Exception as e:
            result = e
        finally:
            self._end_write()

        if isinstance(result, Exception):
            raise result

        return result

    def find_jmes(self, table_name, query: str):
        """
        Thread-safe version of find_jmes.
        """
        self._start_read()
        try:
            result = super().find_jmes(table_name, query)
        except Exception as e:
            result = e
        finally:
            self._end_read()

        if isinstance(result, Exception):
            raise result

        return result

    def find_all(self, table_name):
        """
        Thread-safe version of find_all.
        """
        self._start_read()
        result = None
        try:
            result = super().find_all(table_name)
        except Exception as e:
            result = e
        finally:
            self._end_read()

        if isinstance(result, Exception):
            raise result
        return result

    def execute_query(self, table_name, query_data):
        """
        Thread-safe version of execute_query.
        """
        self._start_read()
        result = None
        try:
            result = super().execute_query(table_name, query_data)
        except Exception as e:
            result = e
        finally:
            self._end_read()

        if isinstance(result, Exception):
            raise result

        return result

    def get_data_by_id(self, table_name, entry_id):
        """

        A function that retrieves data by ID from a specific table. (Threadsafe)

        Parameters:
            table_name (str): The name of the table to retrieve data from.
            entry_id (int): The ID of the entry to retrieve.

        Returns:
            contents: The data associated with the provided entry ID in the specified table.
        """

        self._start_read()
        result = None
        try:
            result = super().get_data_by_id(table_name, entry_id)
        except Exception as e:
            result = e
        finally:
            self._end_read()

        if isinstance(result, Exception):
            raise result

        return result

    def to_pandas(self, table_name):
        """
        Thread-safe version of to_pandas.
        """
        self._start_read()
        result = None
        try:
            result = super().to_pandas(table_name)
        except Exception as e:
            result = e
        finally:
            self._end_read()

        if isinstance(result, Exception):
            raise result

        return result


class QYAMLDBFine(QYAMLDB):
    """
    A subclass of QYAMLDB that implements fine-grained locking. It implements read/write lock in record level.

    """

    def __init__(self, path, key_file='key.file', encrypted=False, byaml=None, log_file='qyaml.log',
                 enable_logging=True,
                 log_level=logging.DEBUG, silent=False):

        super().__init__(path, key_file, encrypted, byaml, log_file, enable_logging, log_level, silent)
        self._lock_manager = RecordLockManager(create_logger=self.logger_enabled, logger=self._logger)

    def insert_new_data(self, table_name, data):
        """
        Insert new data into the table in a thread-safe manner.

        Parameters:
            table_name (str): Name of the table.
            data (dict): Data to insert.

        Returns:
            str: A message indicating the insertion operation is done.

        Raises:
            ValueError: If the table does not exist, the entry does not exist, or a unique constraint is violated.
        """
        if table_name not in self.tables:
            raise ValueError("Table does not exist.")

        # Generate a unique Record ID for the new data
        entry_id = self.generate_new_id(table_name)

        # Acquire a write lock for the newly generated ID
        self._lock_manager.acquire_writer_lock(table_name, entry_id)

        try:
            # Check for unique constraints
            unique_columns = self.tables[table_name]['metadata'].get_unique_columns(table_name)
            if any(data.get(column) in [row.get(column) for row in self.tables[table_name]['data'].values()] for column
                   in unique_columns):
                raise ValueError("Unique constraint violated.")

            # Insert the data
            self.tables[table_name]['data'][entry_id] = data
            self.save_db()
            self._logger.debug(f"Inserted data for record {entry_id} into table {table_name}")
        except Exception as e:
            raise e
        finally:
            # Release the write lock
            self._lock_manager.release_writer_lock(table_name, entry_id)

        return "done."

    def update_entry(self, table_name, entry_id, updated_data):
        """"""
        if table_name not in self.tables or entry_id not in self.tables[table_name]['data'].keys():
            raise ValueError("Table or entry does not exist.")
        try:
            self._lock_manager.acquire_writer_lock(table_name, entry_id)
            self.tables[table_name]['data'][entry_id].update(updated_data)
            self.save_db()

        except Exception as e:
            raise e
        finally:
            # Release the lock
            self._lock_manager.release_writer_lock(table_name, entry_id)

        return "done."

    def update_many(self, table_name, condition, update_data, flags=None):
        """
        Updates data based on given condition.
        Parameters:
            condition (dict): Filtering Conditions.
            update_data (dict): Data to be updated.
            flags: Additional flags (Supported: { add_missing_values : 'True'/False}).
            table_name: Name of table.
        """
        if flags is None:
            flags = {'add_missing_values': True}
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")
        self._log('Updating table.........')
        # Retrieve the metadata to check for unique constraints
        self._lock_for_read(table_name)
        qp = QueryProcessor(self.tables[table_name]['data'])
        qp.filter_id(condition)
        matching_ids = qp.results
        self._release_read(table_name)
        if not matching_ids:
            return None  # No data matching the condition

        # Sort IDs to avoid deadlock
        matching_ids.sort()

        locked_ids = []
        try:
            # Acquire locks for all relevant records
            #print('Acquiring lock for ids.........')
            for entry_id in matching_ids:
                self._lock_manager.acquire_writer_lock(table_name, entry_id)
                locked_ids.append(entry_id)

            # Perform updates
            super().update_many(table_name, condition, update_data, flags)

            # Release locks


        except Exception as e:
            raise e
        finally:
            # Release locks
            for entry_id in locked_ids:
                self._lock_manager.release_writer_lock(table_name, entry_id)

        return "done"

    def delete_entry(self, table_name, entry_id):
        """"""
        if table_name not in self.tables or entry_id not in self.tables[table_name]['data'].keys():
            raise ValueError("Table or entry does not exist.")
        try:
            self._lock_manager.acquire_writer_lock(table_name, entry_id)
            del self.tables[table_name]['data'][entry_id]

            self.save_db()
        except Exception as e:
            raise e
        finally:
            # Release the lock
            self._lock_manager.release_writer_lock(table_name, entry_id)
            self._lock_manager.delete_lock_id(table_name, entry_id)

        return "done"

    def delete_table(self, table_name):
        """"""

        if table_name not in self.tables:
            raise ValueError("Table does not exist.")

        # Acquire lock for entire id
        for i in self.tables[table_name]['data'].keys():
            self._lock_manager.acquire_writer_lock(table_name, i)
        del self.tables[table_name]

        self.save_db()

        return "done"

    def delete_many(self, table_name, condition):
        """
        Delete multiple records from a table based on a given condition.
        Threadsafe
        Parameters:
            table_name (str): The name of the table to delete records from.
            condition (dict): The condition to filter the records to be deleted.
        Raises:
            ValueError: If the table does not exist in the database.
        Returns:
            str: A message confirming the deletion process is done.
        """
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        # Retrieve the metadata to check for unique constraints
        qp = QueryProcessor(self.tables[table_name]['data'])
        qp.filter_id(condition)
        matching_ids = qp.results

        if not matching_ids:
            return None  # No data matching the condition

        # Sort IDs to avoid deadlock
        matching_ids.sort()

        locked_ids = []
        try:
            # Acquire locks for all relevant records
            for entry_id in matching_ids:
                self._lock_manager.acquire_writer_lock(table_name, entry_id)
                locked_ids.append(entry_id)

            # Perform updates
            for entry_id in matching_ids:
                del self.tables[table_name]['data'][entry_id]

            self.save_db()

        except Exception as e:
            raise e
        finally:
            # Release locks
            for entry_id in locked_ids:
                self._lock_manager.release_writer_lock(table_name, entry_id)
                # remove all the locks associated with id
                self._lock_manager.delete_lock_id(table_name, entry_id)

        return "done"

    def find_all(self, table_name):
        """
        Returns all the record.
        Returns:
            list: A list of all the records in the table.
        Raises:
            ValueError: If the table does not exist in the database.
        """
        if table_name not in self.tables:
            raise ValueError("Table does not exist.")

        self._lock_for_read(table_name)
        results = self.tables[table_name]['data'].values()
        self._release_read(table_name)
        return results

    def find(self, table_name, query):
        """
        Find for specific records based on $filter query

        Parameters:
            table_name (str): The name of the table to search in.
            query (dict): The query to filter the data.

        Returns:
            list: The results of the query execution.
        Raises:
            ValueError: If the table does not exist in the database.
        """
        if table_name not in self.tables:
            raise ValueError("Table does not exist.")

        self._lock_for_read(table_name)
        qp = QueryProcessor(self.tables[table_name])
        results = qp.filter(query)
        self._release_read(table_name)
        return results

    def get_data_by_id(self, table_name, entry_id):
        """Gets Data by Object ID"""

        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        if isinstance(entry_id, int):
            # convert it to string
            entry_id = str(entry_id)
        try:
            self._lock_manager.acquire_reader_lock(table_name, entry_id)

            data = self.tables[table_name]['data'][entry_id]

        except Exception as e:
            raise e
        finally:
            # Release the lock
            self._lock_manager.release_reader_lock(table_name, entry_id)
        return data

    def execute_query(self, table_name, query):
        """Executes the query on the table.
        Parameters:
            table_name (str): The name of the table to execute the query on.
            query (dict): The query to be executed.
        """

        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        self._lock_for_read(table_name)
        qp = QueryProcessor(self.tables[table_name])
        results = qp.process_query(query)
        self._release_read(table_name)
        return results

    def _lock_for_read(self, table_name):
        """
        Lock All the record in the table for reading

       **DO NOT USE THIS FUNCTION. IT IS MEANT FOR INTERNAL PURPOSES.**

        Parameters:
            table_name (str): The name of the table to lock.

        Returns:
            None
        """
        self._log('Waiting to acquire reader lock for entire table.', 'debug')

        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        k = self.tables[table_name]['data'].keys()
        # lock for all data
        for i in k:
            self._lock_manager.acquire_reader_lock(table_name, i)
        pass

    def _release_read(self, table_name):
        """
        Release All the record in the table for reading

       **DO NOT USE THIS FUNCTION.
       IT IS MEANT FOR INTERNAL PURPOSES.**

        Parameters:
            table_name (str): The name of the table to lock.

        Returns:
            None
        """

        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")
        self._log('Releasing reader lock for entire table.', 'debug')
        # lock for all data
        for i in self.tables[table_name]['data'].keys():
            self._lock_manager.release_reader_lock(table_name, i)

        self._log(f"Released reader lock for the table. {table_name}", 'debug')

    # _lock_write

    def _lock_for_write(self, table_name):
        """
        Lock All the record in the table for writing

       **DO NOT USE THIS FUNCTION. IT IS MEANT FOR INTERNAL PURPOSES.**

        Parameters:
            table_name (str): The name of the table to lock.

        Returns:
            None
        """
        print('locking for write for entire table.')
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")
        key_list = list(self.tables[table_name]['data'].keys())

        self._log('Waiting to acquire writer lock for entire table.', 'debug')
        key_list.sort()
        # lock for all data
        for i in key_list:
            self._lock_manager.acquire_writer_lock(table_name, i)

        self._log(f'Acquired writer lock for the table. {table_name}', 'debug')

    def _release_write(self, table_name):
        """
        Release All the record in the table for writing

       **DO NOT USE THIS FUNCTION. IT IS MEANT FOR INTERNAL PURPOSES.**

        Parameters:
            table_name (str): The name of the table to lock.

        Returns:
            None
        """
        print('Releasing write lock for all table')
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist.")

        self._log('Releasing writer lock for entire table.', 'debug')
        # lock for all data
        for i in self.tables[table_name]['data'].keys():
            self._lock_manager.release_writer_lock(table_name, i)

        self._log(f"Released writer lock for the table. {table_name}", 'debug')


class GraphGen(object):
    """

    A static class Graph Generator that uses matplotlib class to generate the grqph.
    """

    def create_simple_visual(x,y,chart_type,**kwargs):

        """
        Create visualization for data
        Returns: Matlplotlib figure.
        Parameters:
            x (list): x axis data
            y (list): y axis data
            type (str): type of graph
            **kwargs: optional arguments based on the graph type
        """

        # Bar( horizontal or vertical or stacked), Pie, line and scatter plot supported
        # distinguished by chart type
        if chart_type == 'bar':

            plt.bar(x,y,**kwargs)
        elif chart_type == 'pie':
            plt.pie(y,labels=x)
        elif chart_type == 'line':
            plt.plot(x,y)
        elif chart_type == 'scatter':
            plt.scatter(x,y)
        else:
            raise ValueError('Invalid chart type')
        return plt


