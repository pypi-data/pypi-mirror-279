import unittest
import os
import random

from src.quick_yaml.data_structures import BYAML


class TestBYAML(unittest.TestCase):

    def setUp(self):
        self.filepath = "sample_databases/sample.ezdb"
        self.key_file = "test.key"
        i = random.randint(1, 100)
        self.data = {'id': str(i),'name': random.choice(['sensor', 'fan', 'light', 'fridge']) + str(i),
                                     'status': 'active', 'value': random.randrange(10,100)}
        self.byaml = BYAML(self.filepath, encryption_enabled=False, key_file=self.key_file)

    def test_key_generation_and_loading(self):
        self.assertTrue(os.path.exists(self.key_file))
        key = self.byaml.load_key()
        self.assertIsNotNone(key)

    def test_encode_decode_binary_yaml(self):
        self.byaml.encode_to_binary_yaml(self.data)
        self.assertTrue(os.path.exists(self.filepath))
        decoded_data = self.byaml.decode_from_binary_yaml()

        self.assertEqual(decoded_data.to_dict(), self.data)

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        if os.path.exists(self.key_file):
            os.remove(self.key_file)


if __name__ == '__main__':
    unittest.main()
