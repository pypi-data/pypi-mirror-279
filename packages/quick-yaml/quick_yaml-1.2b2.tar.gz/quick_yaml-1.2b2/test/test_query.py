import unittest
import time

from src.quick_yaml.data_structures import NestedDict
from src.quick_yaml.parser import QueryProcessor

from src.quick_yaml.mock_generator import DataGenerator
import yaml


class TestQueryProcessorPerformance(unittest.TestCase):
    # This data setup will be used for all tests

    sample_data = yaml.safe_load(DataGenerator.generate_sample_data())

    def test_filter_performance(self):
        query_processor = QueryProcessor(self.sample_data)
        query = {
            "$filter": {
                "key1": {"$gt": 11}
            }
        }

        start_time = time.time()
        query_processor.process_query(query)
        duration = time.time() - start_time

        print(f"Filter operation took {duration:.4f} seconds.")
        self.assertTrue(duration < 1)  # Example threshold, adjust based on expected performance

    def test_sort_performance(self):
        query_processor = QueryProcessor(self.sample_data)
        query = {
            "$sort": [("key4", "asc")],
        }

        start_time = time.time()
        query_processor.process_query(query)
        duration = time.time() - start_time

        print(f"Sort operation took {duration:.10f} seconds.")
        self.assertTrue(duration < 1)  # Example threshold, adjust based on expected performance

    def test_convert_pandas(self):
        p = NestedDict.convert_nested(TestQueryProcessorPerformance.sample_data)
        print(type(p))
        x = p["data"].to_pandas()
        print(x)

    def test_aggregate_performance_simple(self):
        query_processor = QueryProcessor(TestQueryProcessorPerformance.sample_data)
        query = {
            "$operations": [
                {"$action": "sum", "$on": "key4"}

            ]
        }

        start_time = time.time()
        query_processor.process_query(query)
        duration = time.time() - start_time

        print(f"Aggregate operation took {duration:.10f} seconds.")


if __name__ == "__main__":
    unittest.main()
