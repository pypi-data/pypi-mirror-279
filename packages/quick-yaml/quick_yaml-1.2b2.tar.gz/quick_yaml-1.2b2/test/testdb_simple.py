import unittest
import pandas as pd
from src.quick_yaml.manager import QYAMLDB as breezedb
class TestEazyDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the database before running tests."""
        cls.db_path = 'test_db.ezdb'
        cls.db = breezedb(cls.db_path, encrypted=False)
        cls.table_name = 'TestTable'
        cls.db.create_table(cls.table_name, unique_columns=['name'], indexes=['name'])

    def test_insert_and_retrieve_data(self):
        """Test data insertion and retrieval by ID."""
        data = {'name': 'Test Item', 'value': 42}
        self.db.insert_new_data(self.table_name, data)
        retrieved_data = self.db.get_data_by_id(self.table_name, '1')
        self.assertEqual(data['name'], retrieved_data['name'])

    def test_update_data(self):
        """Test updating data for an existing entry."""
        updated_data = {'value': 100}
        self.db.update_entry(self.table_name, '1', updated_data)
        retrieved_data = self.db.get_data_by_id(self.table_name, '1')
        self.assertEqual(updated_data['value'], retrieved_data['value'])

    def test_to_pandas(self):
        """Test converting table data to a pandas DataFrame."""
        df = self.db.to_pandas(self.table_name)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue('name' in df.columns and 'value' in df.columns)

    def test_update_many(self):
        """Test updating multiple records based on a condition."""
        # Insert multiple records to update
        records_to_insert = [
            {'name': 'Multi Update 1', 'value': 10},
            {'name': 'Multi Update 2', 'value': 20},
            {'name': 'Other', 'value': 30}
        ]
        for record in records_to_insert:
            self.db.insert_new_data(self.table_name, record)

        # Define the condition to match records for update
        condition = {'name': {'$eq': 'Multi Update 2'}}

        # Define the update data
        update_data = {'value': 123122342}

        # Define the flags
        flags = {'add_missing_keys': True}

        # Execute update_many
        self.db.update_many(self.table_name, condition, update_data, flags)

        # Validate the update
        updated_records = self.db.tables[self.table_name]['data'].values()

        print(updated_records)

    @classmethod
    def tearDownClass(cls):
        """Clean up the database after tests."""
        import os
        os.remove(cls.db_path)


if __name__ == '__main__':
    unittest.main()
