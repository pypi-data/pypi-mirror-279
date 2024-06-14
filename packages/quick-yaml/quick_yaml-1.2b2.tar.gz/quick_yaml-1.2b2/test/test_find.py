import unittest

from src.quick_yaml.manager import QYAMLDB


class TestEazyDBFindMethod(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database and insert sample data."""
        self.db = QYAMLDB(path='sample.ezdb', encrypted=False)  # Adjust parameters as needed
        self.db.create_table('devices', unique_columns=['id', 'name'], indexes=['id'])
        self.db.insert_new_data('devices', {'id': '1', 'name': 'Sensor', 'status': 'active', 'value': 20})
        self.db.insert_new_data('devices', {'id': '2', 'name': 'Actuator', 'status': 'inactive', 'value': 35})
        self.db.insert_new_data('devices', {'id': '3', 'name': 'Sensor2', 'status': 'active', 'value': 15})
        print(self.db.tables['devices']['data'].pretty_print())

    def tearDown(self):
        """Tear down the test environment."""
        # Implement any cleanup necessary to remove the temporary database
        pass

    def test_find_active_devices(self):
        """Test finding active devices."""
        query = "[?status == 'active']"
        results = self.db.find_jmes('devices', query)
        print(results)

    def test_find_device_by_name(self):
        """Test finding a device by its name."""
        query = "[?name == 'Actuator'] | [0]"
        result = self.db.find_jmes('devices', query)
        print("Found device by name ", result)


# More test cases as needed

if __name__ == "__main__":
    unittest.main()
