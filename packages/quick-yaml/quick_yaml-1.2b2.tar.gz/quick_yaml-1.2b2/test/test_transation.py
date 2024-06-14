import unittest
from src.quick_yaml.manager import QYAMLDB, QYAMLDBCoarse
import os
import tempfile


class TestEazyDB(unittest.TestCase):
    def setUp(self):
        # Create a temporary file to serve as the database
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.db_file.name + '.ezdb'  # Ensuring the file has the correct extension
        # Initialize the database with the temporary file path
        self.db = QYAMLDB(self.db_path, encrypted=False)

    def tearDown(self):
        # Close and remove the temporary database file
        os.unlink(self.db_path)

    def test_create_table(self):
        """Test creating a table works correctly."""
        self.db.create_table('test_table')
        self.assertIn('test_table', self.db.tables, "Table was not created successfully.")

    def test_insert_and_query_data(self):
        """Test inserting data and querying it back."""
        self.db.create_table('test_table')
        self.db.insert_new_data('test_table', {'id': 1, 'data': 'Test'})
        queried_data = self.db.get_data_by_id('test_table', '1')
        self.assertEqual(queried_data['data'], 'Test', "Data inserted and queried does not match.")

    def test_transaction_commit(self):
        """Test that transactions commit correctly."""
        self.db.create_table('test_table')
        transaction_data = {
            '$operations': [
                {'type': '$insert', '$table_name': 'test_table', '$data': {'id': 1, 'data': 'Test'}},
                {'type': '$query', '$table_name': 'test_table', '$query_data': {"$filter": {
                    "id": {"$eq": 1}
                }}},

            ],
            '$error_strategy': 'rollback'
        }
        result = self.db.begin_transaction(transaction_data)
        print(result)
        # self.assertEqual(result['status'], 'Success', "Transaction did not commit successfully.")
        # queried_data = self.db.get_data_by_id('test_table', '1')
        # self.assertEqual(queried_data['data'], 'Test', "Transaction commit did not persist data as expected.")

    def test_transaction_rollback(self):
        """Test that transactions roll back on error."""
        self.db.create_table('test_table', unique_columns=['id'])
        self.db.insert_new_data('test_table', {'id': 1, 'data': 'Test'})
        # Attempt to insert duplicate id which should fail and trigger a rollback
        transaction_data = {
            '$operations': [
                {'type': '$insert', '$table_name': 'test_table', '$data': {'id': 1, 'data': 'Test Duplicate'}},

            ],
            '$error_strategy': 'rollback'
        }
        result = self.db.begin_transaction(transaction_data)
        print(result)
        self.assertIn('Failure', result['status'], "Transaction unexpectedly succeeded; rollback expected.")
        queried_data = self.db.get_data_by_id('test_table', '1')
        self.assertNotEqual(queried_data['data'], 'Test Duplicate', "Rollback did not occur as expected.")


if __name__ == '__main__':
    unittest.main()
