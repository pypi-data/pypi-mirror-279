
# QuickYAML
# **Project Overview**
A lightweight, serverless database management system that stores data in a Binary YAML format, supports basic CRUD operations, query processing with mathematical functions, and optional encryption for data security.

#  **Features and Specifications**

- **Data Storage**: Binary YAML format for efficient storage and retrieval of Python objects.
- **CRUD Operations**: Support for create, read, update, and delete operations.
- **Query Processing**: Integration with Pandas for advanced data manipulation and query capabilities.
- **Indexing**: Implementation of a B-tree or similar structure for efficient data indexing.
- **Encryption**: Optional data encryption for enhanced security.
- **Unique Constraints**: Support for enforcing uniqueness in specified columns.
  


# Installation steps

To install the package for python, use pip package manager.
```bash
 pip install quick_yaml
 ```
# Basic Usage
This section will be expanded later in [https://gitlab.com/eazy-home-admin/QuickYAML/-/wikis/home](Wiki)
```python
from quick_yaml.manager import QYAMLDB
db = QYAMLDB('f.ezdb','f.key',encrypted=True) # Encrpytion by default is optional
db.create_table('sample', unique_columns=['name'] ) # Indexes to be bought in future.
data = {'name': 'Test Item', 'value': 42}
db.insert_new_data('sample', data) # Insert a data 
```
# Queries supported

QuickYAML aims to provide a rich set of query features that facilitate deep and flexible interaction with the data. 
These features are designed to cater to both simple and complex data manipulation needs, ensuring users can easily 
retrieve, analyze, and modify data as required. Below, we expand on the proposed query features, highlighting their
functionality and potential use cases within QuickYAML.

## Basic Queries

- **Access Subkeys**: Enables direct access to nested data within documents. This feature is particularly 
useful, for databases storing complex, hierarchical data structures, allowing users to query specific parts of a document without retrieving the entire record.


## Advanced Query Processing with Pandas

QuickYAML plans to leverage Pandas, a powerful data analysis and manipulation library, to provide advanced querying capabilities. This integration will allow for sophisticated data operations that are both efficient and intuitive.

- **Range Queries (`$range`)**: Allows for retrieving records where a specified field falls within a given range. This is crucial for scenarios where boundaries define the data of interest, such as dates or numerical thresholds.
  
- **Comparison Queries**:
  - **Greater Than (`$gt`)**: Retrieves records where a field's value is greater than a specified value.
  - **Less Than (`$lt`)**: Similar to `$gt` but for values less than the specified value.
  - **Greater Than or Equal (`$ge`)**: Extends `$gt` to include equality.
  - **Less Than or Equal (`$le`)**: Extends `$lt` to include equality.
  - **Equal (`$eq`)**: Retrieves records with a field's value exactly matching the specified value.

- **Membership Query (`$in`)**: Fetches records where a field's value matches any in a specified set of values. 
This is particularly useful for filtering data based on a list of identifiers, categories, or any discrete set of values.

- **Pattern Matching (`$like`)**: Offers regex-based querying to find records where a text field matches a given pattern.
This feature is invaluable for text search, allowing for flexible matching based on partial text, patterns, or conditions.
- **String Search (`$contains`)**: Offers a regex-based querying to search for substring present in the key.
### Grouping and Sorting

- **Group By (`$group_by`)**: This operation groups records by one or more fields, facilitating aggregate calculations 
or summaries on these groups. It's essential for analytical queries where understanding data in segments or categories is required.

- **Sort (`$sort`)**: Orders the records based on one or more fields, in ascending or descending order. Sorting is 
fundamental for organizing query results, especially in reporting or when order matters in data presentation.

## Selection

- **Select (`$select`)**: Allows specifying a subset of fields to be returned in the query results.
This feature helps focus on relevant data, reducing the overhead of processing and transferring unnecessary information.

## Aggregate Functions in QuickYAML

QuickYAML supports a variety of aggregate functions that can be used to perform calculations on a dataset. These functions
are crucial for data analysis and can provide significant insights into the data. Below is a description of each aggregate
function supported by QuickYAML.

### Supported Aggregate Functions

- **`$sum`**: Calculates the total sum of numeric values in a specified field.
- **`$avg`** (Average): Computes the average of numeric values in a specified field.
- **`$count`**: Counts the number of items in the dataset or a specific group.
- **`$max`**: Finds the maximum value among numeric values in a specified field.
- **`$min`**: Finds the minimum value among numeric values in a specified field.
- **`$median`**: Determines the median value among numeric values in a specified field.
- **`$mode`**: Finds the mode (the most frequently occurring value) in a specified field.
- **`$stddev`** (Standard Deviation): Calculates the standard deviation of numeric values in a specified field, indicating the dispersion of data points.
- **`$variance`**: Calculates the variance of numeric values in a specified field, measuring the degree of variation.

#### How to Use Aggregate Functions

Aggregate functions can be used as part of the `$operations` component of a query. These operations can be applied 
directly to the dataset or to data that has been grouped using the `$groupby` operation. 

Here is an example query that uses aggregate functions:

```json
{
    "$filter": {
      "price": {"$gt": 100}
    },
    "     $groupby": "category",
    "$operations": [
        {"$action": "$sum", "$on": "price"},
        {"$action": "$avg", "$on": "price"}
    ]
}
```

In this example, the dataset is first filtered to include only items with a price greater than 100. Then, the data is grouped by the "category" field. Finally, two aggregate operations are performed on each group: summing the prices and calculating the average price.

#### Note on Using Aggregate Functions with `$select`

When using aggregate functions in a query, it is not recommended to use the `$select` operation in conjunction with `$operations`. This is because aggregate functions typically reduce the dataset to summary values, which may not align with the field projections specified in `$select`.


## Query Sample Syntax's

- Access Sub-keys:
  `key1.subkey1.`

- Where conditions: 
  - $range:[2,3]: ranged values
  - $gt:10: value greater than 10
  - $lt:10: value less than 10
  - $ge:10: value greater than  or equal 10
  - $le:10: value less than or equal 10
  - $eq:10: value equal to 10
  - $group_by:'type': group data by attribute type
  - $sort:['time_updated','type']): sort by attribute timestamp and type.
  - $select:['attribute1','attribute2']: only show the attributes in select.
  - $like:'regex': only show the attributes that match the regex pattern.
  - $in:['value1','value2']: only show the attributes that are within the set.
  
```json
{
  "$filter": {
    "key1": {"$gt": 10}
  },
  "$groupby": "key2",
  "$sort": ["time", "type"],
  "$select": ["key3.subkey"],
  "$operations": [
    {"$operation": "sum", "$on": "key4"},
    {"$operation": "average", "$on": "key5"}
  ]
}
```



## Priority of operators
### 1. `$filter`

- **Rationale**: Filtering as the first operation reduces the dataset to only those records that meet the specified criteria. This is fundamental because it limits the amount of data processed in subsequent steps, improving performance and ensuring that operations like grouping, sorting, and aggregations are only performed on relevant data. It's more efficient to operate on a smaller, more relevant subset of data in the later stages.

### 2. `$groupby`

- **Rationale**: Grouping data is logically placed after filtering because it organizes the already narrowed down dataset into categories or groups based on shared values of a specified key. Grouping at this stage allows for meaningful aggregations and transformations within groups, and it's preparatory for sorting within or across these groups. Performing grouping after filtering ensures groups are only formed from relevant data, making the groups themselves more meaningful.

### 3. `$sort`

- **Rationale**: Sorting comes after grouping because it allows for the ordered presentation of the grouped data, which is essential for readability and further analysis. If sorting were done before grouping, the group operation might disrupt the order. Sorting can apply to the order of groups themselves or to items within each group, depending on the query's needs. This stage ensures that the final output is organized in a user-specified manner, enhancing data interpretation.

### 4. `$select`

- **Rationale**: Selection narrows down the dataset to only include specified fields, reducing the complexity and size of the final dataset presented to the user. Placing selection after sorting ensures that sorting operations have access to all necessary fields before any are excluded from the result. This is particularly important when sorting might depend on fields that are not ultimately presented in the final output.

### 5. `$operations` (Aggregations)

- **Rationale**: Aggregate functions such as sum, average, median, etc., are applied last because they typically produce summary information about the dataset that might be grouped and sorted. Aggregations often serve as the final step in data analysis, summarizing detailed data into more digestible metrics. Applying aggregations after operations like filtering, grouping, and sorting ensures these summaries are both relevant (because they operate on filtered data) and organized (because they can be applied within sorted and grouped structures).

## Translations
Transactions in our database management system provide a mechanism for batch executing a series of commands, 
ensuring that all commands within a transaction are completed without errors. This functionality emulates the transactional capabilities found in traditional DBMS, 
enhancing reliability and consistency during batch operations. To further enhance error handling during transactions, we support three distinct error control strategies:

- **Rollback:** This strategy reverts the database to its state prior to the start of the transaction, ensuring ACID compliance by maintaining atomicity, consistency, isolation, and durability. It is the default behavior, safeguarding against the persistence of partial transaction outcomes.
- **Continue:** Under this strategy, the transaction proceeds despite encountering errors, allowing subsequent commands within the transaction to be executed.
- **Break:** This halts the transaction upon the first error encountered, stopping further execution of any remaining commands within the transaction.

The format for defining a transaction is structured to clearly specify each operation within the transaction, the table involved, and the data being manipulated or criteria being applied. Here is an example of a transaction that includes various operations such as insert, insert_many, delete, delete_many, update, and update_many:

```
{
    "$transaction_id": 100,
    "$operations": [
        { "type": "$insert", "$table_name": "my_table", "$data": {"name": "Alice", "age": 30} },
        { "type": "$insert_many", "$table_name": "my_table", "$data": [{"name": "Bob", "age": 25}, {"name": "Charlie", "age": 35}] },
        { "type": "$delete", "$table_name": "my_table", "$obj_id": "2" },
        { "type": "$delete_many", "$table_name": "my_table", "$condition": {"age": {"$gt": 32}} },
        { "type": "$update", "$table_name": "my_table", "$obj_id": "3", "$data": {"age": 28} },
        { "type": "$update_many", "$table_name": "my_table", "$condition": {"name": "Alice"}, "$data": {"age": 31}, "$flags": {} }
            { "type": "$create_table", "$table_name": "my_table"}
    ],
    "$on_error": "rollback" | "continue" | "break",
          "$on_invalid_command": 'break' | 'rollback' | 'continue';
}
```

Each transaction is uniquely identified by a `$transaction_id` and specifies a list of `$operations` to be performed. The `$on_error` field determines the error control strategy to be applied in case of an operation failure within the transaction. This structured approach to defining and executing transactions ensures that batch operations are performed reliably and according to the specified error handling strategy, thereby enhancing data integrity and consistency.