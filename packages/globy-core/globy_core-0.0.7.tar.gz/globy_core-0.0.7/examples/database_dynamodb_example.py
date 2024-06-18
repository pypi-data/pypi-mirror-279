import sys
sys.path.append('../src')

from globy_core.logging.logger import Logger
from globy_core.store.database import DynamoDBDatabase as GlobyDatabase

# This example demonstrates how to use the DynamoDBDatabase class with the Logger class
if __name__ == "__main__":
    logger = Logger().logger
    database = GlobyDatabase(table_name="YourTableName")

    item = {'id': '123', 'name': 'Alice'}
    key = {'id': '123'}

    database.put(item)
    retrieved_item = database.get(key)
    print(retrieved_item)

    database.delete(key)
    is_empty = database.is_empty()
    print(f"Database is empty: {is_empty}")

    logger.info("DynamoDB test passed")
