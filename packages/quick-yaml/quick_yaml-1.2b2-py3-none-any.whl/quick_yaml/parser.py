import statistics
from collections import defaultdict

from .data_structures import NestedDict
import re

filter_options = {
    '$gte': lambda val, thr: val >= thr,
    '$lte': lambda val, thr: val <= thr,
    '$gt': lambda val, thr: val > thr,
    '$lt': lambda val, thr: val < thr,
    '$eq': lambda val, thr: val == thr,
    '$neq': lambda val, thr: val != thr,
    '$range': lambda val, thr: thr[0] <= val < thr[1],
    '$in': lambda val, thr: val in thr,
    '$like': lambda val, thr: bool(re.match(re.compile(thr), val)) if val is not None else False,
    '$matches': lambda val, thr: bool(re.match(re.compile(thr), val)) if val is not None else False,
    '$contains': lambda val, thr: bool(re.findall(re.compile(thr), val)) if val is not None else False,
}


class QueryFormatError(Exception):
    def __init__(self, data, message="Invalid Query Data"):
        self.data = data
        self.message = message
        super().__init__(self.message)


class KeywordNotFoundError(Exception):
    def __init__(self, data, message="Invalid Keyword found"):
        self.data = data
        self.message = message
        super().__init__(self.message)


class QueryProcessor(object):
    """
       Initializes the QueryProcessor with a dataset.

       Attributes:
           dataset (NestedDict): A dataset wrapped in a NestedDict object.
           results (NestedDict): The result set after applying the query operations on the dataset.

    """

    def __init__(self, data: NestedDict):

        self.results = data # The entire table Data without MetaData Object, Since it has nothing to do with Metadata


    def process_query(self, query):
        """
           Processes a structured query and applies the specified operations on the dataset.


           Args:
               query (dict): A structured query dict containing operations like $filter, $groupby, $sort, $select, and
                $operations.

           Raises:
               QueryFormatError: If 'select' and aggregate functions are requested in the same query.

           Returns: The result set after applying the query operations on the dataset. It Returns the entire dataset
           if no query is given.
        """
        operation_order = ('$filter', '$groupby', '$sort', '$select', '$operations')

        sorted_operations = sorted(query.items(), key=lambda item: operation_order.index(item[0]))
        if '$select' in query and '$operations' in query:
            # Handle the situation where both operations are requested together
            raise QueryFormatError(query,"Combining 'select' and aggregate functions in the same query is not "
                                         "supported.")
        for operation, parameters in sorted_operations:
            if operation == '$filter':
                self.filter(parameters)
            elif operation == '$groupby':
                self.group_by(parameters)
            elif operation == '$sort' and '$operations' not in query:
                self.sort(parameters)
            elif operation == '$select':
                self.select(parameters)
            elif operation == '$operations':
                self.execute_operations(parameters)

        return self.results  # Or the modified dataset

    def filter(self, data):
        """
        Filters the dataset based on the conditions specified in the data argument.

        Args:
            data (dict): A dictionary containing field names as keys and conditions as values.

        Raises:
            KeywordNotFoundError: If an invalid filter condition is specified.

        """

        result = self.results.values()

        for key, query_constraint in data.items():
            operator, constraint = next(iter(query_constraint.items()))
            if operator not in filter_options:
                raise KeywordNotFoundError(key,
                                           f"This keyword is invalid. Supported keywords are: {list(filter_options.keys())}")

            filter_func = filter_options[operator]
            result = [record for record in result if filter_func(record.get(key, None), constraint)]

        self.results = result

    def filter_id(self, data):
        """
        Filters the dataset based on the conditions specified in the data argument.

        Args:
            data (dict): A dictionary containing field names as keys and conditions as values.

        Raises:
            KeywordNotFoundError: If an invalid filter condition is specified.
        """
        results = self.results

        for key, query_constraint in data.items():
            operator, constraint = next(iter(query_constraint.items()))
            if operator not in filter_options:
                raise KeywordNotFoundError(key,
                                           f"This keyword is invalid. Supported keywords are: {list(filter_options.keys())}")

            filter_func = filter_options[operator]
            results = [index for index, record in results.items() if filter_func(record.get(key, None), constraint)]

        self.results = results

    def group_by(self, key):
        """
          Groups the dataset based on a specified key.

          Args:
              key (str): The key to group the data by.

          Raises:
              ValueError: If the group by key is None.
          """
        if not key:
            raise ValueError("Group by key cannot be None")

        grouped_results = defaultdict(list)
        for item in self.results:
            group_key_value = item.get(key)  # Get the key value for grouping
            grouped_results[group_key_value].append(item)  # append the item into the group

        self.results = dict(grouped_results)

    def sort(self, data):
        """
          Sorts the dataset or grouped data based on specified fields and directions.

          Args:
              data (list of tuples): Each tuple contains the field to sort by and the direction ('asc' or 'desc').
          """
        if isinstance(self.results, list):  # Ungrouped data

            sort_keys = [item[0] for item in data]
            sort_directions = [item[1] for item in data]
            # Build a list of tuples based on the sort keys and directions
            self.results = sorted(self.results, key=lambda x: tuple(
                x[k] * (-1 if d == 'desc' else 1) for k, d in zip(sort_keys, sort_directions)))

        elif isinstance(self.results, dict):  # Grouped data

            for group_key, records in self.results.items():
                sort_keys = [item[0] for item in data]
                sort_directions = [item[1] for item in data]
                # Sort each group individually
                self.results[group_key] = sorted(records, key=lambda x: tuple(
                    x[k] * (-1 if d == 'desc' else 1) for k, d in zip(sort_keys, sort_directions)))

    def select(self, fields):
        """
        Projects only the specified fields in the results.

        Args:
            fields (list): A list of fields to include in the output.
        """
        # If the data is grouped (dict), iterate through groups
        if type(self.results) is dict:
            selected_results = {}
            for group_key, group_items in self.results.items():
                # Apply selection on each item within the group
                selected_results[group_key] = [{field: item.get(field) for field in fields} for item in group_items]
        elif isinstance(self.results, list):
            # Directly apply selection on the list of items
            selected_results = [{field: item.get(field) for field in fields} for item in self.results]
        else:
            # Handle other types or raise an error
            raise TypeError("Unsupported data type for selection operation.")

        self.results = selected_results
        print(self.results)

    def execute_operations(self, operations):
        """
           Executes specified aggregate operations on the dataset or grouped data.

           Args:
               operations (list of dicts): Each dictionary contains an aggregate op to perform and the field it operates on.

           Note:
               Supported operations include sum, average (avg), count, max, min, median, mode, standard deviation (stddev), and variance.
        """
        # Define aggregate functions
        aggregate_functions = {
            '$sum': sum,
            '$avg': lambda vals: sum(vals) / len(vals) if vals else 0,
            '$count': len,
            '$max': max,
            '$min': min,
            '$median': lambda vals: statistics.median(vals) if vals else 0,
            '$mode': lambda vals: statistics.mode(vals) if vals else None,
            '$stddev': lambda vals: statistics.stdev(vals) if len(vals) > 1 else 0,
            '$variance': lambda vals: statistics.variance(vals) if len(vals) > 1 else 0,
        }

        # Initialize a variable to hold the aggregated results
        # The structure will depend on whether the data is grouped or not
        aggregated_results = {}

        # Helper function to perform the aggregation
        def perform_aggregation(items, op):
            op_action = op['$action']
            op_field = op['$on']
            values = [item.get(op_field, 0) for item in items]
            try:
                result = aggregate_functions[op_action](values)
            except Exception:
                result = 0
            return result

        # Check if results are grouped (dict) or ungrouped (list)
        if isinstance(self.results, dict):
            # Grouped data: iterate over each group
            for group_key, group_items in self.results.items():
                group_aggregates = {}
                for operation in operations:
                    aggregated_value = perform_aggregation(group_items, operation)
                    # Store each op result in a dictionary under the group key
                    group_aggregates[operation['$action']] = aggregated_value
                aggregated_results[group_key] = group_aggregates
        elif isinstance(self.results, list):
            # Ungrouped data: apply operations directly on the list of results
            for operation in operations:
                aggregated_value = perform_aggregation(self.results, operation)
                # Store each op result directly in the results dictionary
                aggregated_results[operation['$action']] = aggregated_value

        # Update self.results with the final aggregated results
        self.results = aggregated_results
