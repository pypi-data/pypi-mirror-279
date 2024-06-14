import random
from datetime import datetime, timedelta
import yaml
from .manager import QYAMLDB


class SetupDeviceTable:

    @staticmethod
    def generate_random_data(i=None):
        """
        Generate random data.
        Parameters:
            i (int): A random integer number. If None, a random integer between 1 and 1000 is generated.
        Returns:
            dict: A dictionary containing keys 'id', 'name', 'status', and 'value' with random data.
            """
        if i is None:
            i = random.randrange(1, 1000)
        return {'id': str(i), 'name': random.choice(['sensor', 'fan', 'light', 'fridge']) + str(i),
                'status': 'active', 'value': random.randrange(10, 100)}

    def __init__(self):
        self.db = None

    def setup_db(self, db='sample.ezdb', key='sample.key', encrypted=False,count=10):
        """
        Set up the database for testing.
        Parameters:
            db (str): The path to the database file.
            key (str): The path to the key file.
            encrypted (bool): Whether to encrypt the database or not.
            count (int): The number of records to insert.
        Returns:
            None

        """
        self.db = QYAMLDB(db, key, encrypted)
        self.db.create_table('devices_table', unique_columns=['id', 'name'], indexes=['id'])

        for i in range(1,count):
            self.db.insert_new_data('devices_table', SetupDeviceTable.generate_random_data(i))

        print(self.db.tables['devices_table']['metadata'])


class DataGenerator:
    def __init__(self, db_path='sample_data.ezdb', key_file='sample_key.key', encrypted=False):
        self.db_path = db_path
        self.key_file = key_file
        self.encrypted = encrypted

    @staticmethod
    def generate_random_date(start_year, end_year):
        """Generates a random date between two years."""
        start_date = datetime(year=start_year, month=1, day=1)
        end_date = datetime(year=end_year, month=12, day=31)
        time_between_dates = end_date - start_date
        random_number_of_days = random.randrange(time_between_dates.days)
        return (start_date + timedelta(days=random_number_of_days)).strftime('%Y-%m-%d')

    @staticmethod
    def generate_sample_data_dict(num_samples=100):
        """Generates sample data in dictionary format."""
        key2_options = ['A', 'B', 'C', 'D']
        type_options = ['X', 'Y', 'Z']
        subkey_values = [f'value{i}' for i in range(1, 11)]
        sample_data = {}

        for i in range(1, num_samples + 1):
            sample_data[str(i)] = {
                'key1': random.randint(5, 25),
                'key2': random.choice(key2_options),
                'time': DataGenerator.generate_random_date(1980, 2023),
                'type': random.choice(type_options),
                'key3': {'subkey': random.choice(subkey_values)},
                'key4': random.randint(50, 200),
                'key5': random.randint(10, 100000)
            }
        return {'data': sample_data}

    def modify_generate_sample_data_and_save(self, num_samples=100):
        """Generates sample data and saves it into a quick_yaml database."""
        sample_data_dict = self.generate_sample_data_dict(num_samples)
        db = QYAMLDB(path=self.db_path, key_file=self.key_file, encrypted=self.encrypted)
        table_name = "sample_table"
        db.create_table(table_name=table_name)

        for key, value in sample_data_dict['data'].items():
            db.insert_new_data(table_name=table_name, data=value)

        return self.db_path

    @staticmethod
    def generate_sample_data(num_samples=100, ret_type='yaml'):
        """Generates sample data and returns it in YAML format or as a dict."""
        sample_data_dict = DataGenerator.generate_sample_data_dict(num_samples)
        if ret_type == 'yaml':
            return yaml.dump(sample_data_dict, allow_unicode=True)
        return sample_data_dict
