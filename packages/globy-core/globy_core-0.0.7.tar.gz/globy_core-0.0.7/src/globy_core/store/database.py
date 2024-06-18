from pymongo import MongoClient
import boto3
from typing import Any, Optional

class GlobyDatabase:
    """
    Common interface for a database.
    """
    def put(self, item: Any) -> None:
        """Add an item to the database."""
        raise NotImplementedError

    def get(self, key: Any) -> Optional[Any]:
        """Retrieve an item from the database by key. Return None if the item is not found."""
        raise NotImplementedError

    def delete(self, key: Any) -> None:
        """Delete an item from the database by key."""
        raise NotImplementedError

    def is_empty(self) -> bool:
        """Return True if the database is empty, False otherwise."""
        raise NotImplementedError

class DynamoDBDatabase(GlobyDatabase):
    def __init__(self, table_name: str):
        self._dynamodb = boto3.resource('dynamodb')
        self._table = self._dynamodb.Table(table_name)

    def put(self, item: dict) -> None:
        self._table.put_item(Item=item)

    def get(self, key: dict) -> Optional[dict]:
        response = self._table.get_item(Key=key)
        return response.get('Item')

    def delete(self, key: dict) -> None:
        self._table.delete_item(Key=key)

    def is_empty(self) -> bool:
        # DynamoDB does not provide a straightforward way to check if a table is empty.
        # This is a naive implementation and might not be efficient for large tables.
        response = self._table.scan(Limit=1)
        return len(response.get('Items', [])) == 0

class MongoDBDatabase(GlobyDatabase):
    def __init__(self, database_name: str, collection_name: str, host='localhost', port=27017):
        self._client = MongoClient(host, port)
        self._db = self._client[database_name]
        self._collection = self._db[collection_name]

    def put(self, item: dict) -> None:
        self._collection.insert_one(item)

    def get(self, key: dict) -> Optional[dict]:
        return self._collection.find_one(key)

    def delete(self, key: dict) -> None:
        self._collection.delete_one(key)

    def is_empty(self) -> bool:
        return self._collection.count_documents({}) == 0
