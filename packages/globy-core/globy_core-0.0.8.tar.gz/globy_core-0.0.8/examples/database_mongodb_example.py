import sys
sys.path.append('../src')

from globy_core.logging.logger import Logger
from globy_core.store.database import MongoDBDatabase as GlobyDatabase

# This example demonstrates how to use the MongoDBDatabase class with the Logger class
if __name__ == "__main__":
    logger = Logger().logger
    database = GlobyDatabase(database_name="testdb", collection_name="testcollection")

    item = {'_id': '123', 'name': 'Alice'}
    key = {'_id': '123'}

    database.put(item)
    retrieved_item = database.get(key)
    print(retrieved_item)

    database.delete(key)
    is_empty = database.is_empty()
    print(f"Database is empty: {is_empty}")

    logger.info("MongoDB test passed")
