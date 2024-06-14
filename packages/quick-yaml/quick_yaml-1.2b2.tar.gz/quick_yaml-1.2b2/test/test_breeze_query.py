import unittest

from src.quick_yaml.data_structures import NestedDict


class TestNestedDictFindComplex(unittest.TestCase):
    def setUp(self):
        self.data = {
            "people": [
                {"name": "John", "age": 30, "city": "New York", "skills": ["Python", "SQL"]},
                {"name": "Jane", "age": 25, "city": "Paris", "skills": ["Java", "C++"]},
                {"name": "Mike", "age": 35, "city": "London", "skills": ["HTML", "CSS", "JavaScript"]},
            ],
            "config": {
                "version": "1.0.0",
                "settings": {
                    "enabled": True,
                    "features": ["feature1", "feature2"]
                }
            }
        }
        self.nd = NestedDict(self.data)

    def test_find_people_older_than_30(self):
        query = "people[?age > `30`]"
        result = self.nd.find(query)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "Mike")

    def test_project_names_and_ages(self):
        query = "people[].{name: name, age: age}"
        result = self.nd.find(query)
        self.assertTrue(all('name' in person and 'age' in person for person in result))
        self.assertEqual(len(result), 3)

    def test_find_max_age(self):
        query = "max_by(people, &age).age"
        result = self.nd.find(query)
        self.assertEqual(result, 35)

    def test_find_names_with_python_skill(self):
        query = "people[?skills.contains(@, `Python`)].name"
        result = self.nd.find(query)
        self.assertIn("John", result)

    def test_get_enabled_features(self):
        query = "config.settings | [?enabled == `true`].features | [0]"
        result = self.nd.find(query)
        self.assertListEqual(result, ["feature1", "feature2"])


if __name__ == "__main__":
    unittest.main()
