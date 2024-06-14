import logging
import threading
import time
from random import randint

from src.quick_yaml.manager import QYAMLDB, QYAMLDBCoarse, QYAMLDBFine

# Initialize the database
db_path = "test_db.ezdb"
db = QYAMLDBFine(path=db_path,encrypted=False,enable_logging=True,silent=False,log_level=logging.DEBUG,log_file='concurent.log')

# Setup initial tables and data
db.create_table("test_table")
for i in range(200):
    db.insert_new_data("test_table", {"id": i, "value": f"initial_data_{i}"})


# Reader thread function
def reader_thread(db, table_name, read_count):
    for _ in range(read_count):
        entry_id = randint(1, 9)
        try:
            data = db.get_data_by_id(table_name, entry_id)
            print(f"Reader got data: {data}")
        except Exception as e:
            print(f"Reader encountered an error: {str(e)}")
            # print stack trace
            import traceback
            traceback.print_exc()
        time.sleep(randint(1, 5))  # Simulate read time


# Writer thread function
def writer_thread(db, table_name, write_count):
    print('Writer')
    for _ in range(write_count):
        entry_id = randint(0, 9)

        new_value = f"updated_data_{randint(100, 200)}"
        try:

            db.update_many(table_name,{'id':{'$neq':entry_id}},{'value':new_value})

            print(f"Writer updated entry {entry_id} to {new_value}")
        except Exception as e:

            print(f"Writer encountered an error: {str(e)}")
        time.sleep(randint(2, 4))  # Simulate write time


# Create thread groups
readers = []
writers = []

# Create 5 reader threads
for _ in range(10):
    t = threading.Thread(target=reader_thread, args=(db, "test_table", 5),daemon=True)
    readers.append(t)

for _ in range(2):
    t = threading.Thread(target=writer_thread, args=(db, "test_table", 1,),daemon=True)
    writers.append(t)

# Start all threads
for reader in readers:
    reader.start()
for writer in writers:
    writer.start()

# Wait for all threads to complete
# for reader in readers:
#     reader.join()
for writer in writers:
    writer.join()

print("Test complete.")
