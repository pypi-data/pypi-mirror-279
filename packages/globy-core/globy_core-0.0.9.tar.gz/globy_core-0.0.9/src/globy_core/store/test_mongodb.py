import pytest
from pymongo import MongoClient

# Configuration
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "testdb"
COLLECTION_NAME = "testcollection"

@pytest.fixture(scope="module")
def mongo_client():
    client = MongoClient(MONGO_URI)
    yield client
    client.close()

@pytest.fixture(scope="module")
def test_db(mongo_client):
    db = mongo_client[DATABASE_NAME]
    yield db
    mongo_client.drop_database(DATABASE_NAME)

@pytest.fixture(scope="function")
def test_collection(test_db):
    collection = test_db[COLLECTION_NAME]
    yield collection
    collection.delete_many({})

def test_insert_document(test_collection):
    doc = {"name": "Alice", "age": 30}
    result = test_collection.insert_one(doc)
    assert result.acknowledged is True

def test_find_document(test_collection):
    doc = {"name": "Bob", "age": 25}
    test_collection.insert_one(doc)
    result = test_collection.find_one({"name": "Bob"})
    assert result is not None
    assert result["age"] == 25

def test_update_document(test_collection):
    doc = {"name": "Charlie", "age": 35}
    test_collection.insert_one(doc)
    test_collection.update_one({"name": "Charlie"}, {"$set": {"age": 36}})
    result = test_collection.find_one({"name": "Charlie"})
    assert result is not None
    assert result["age"] == 36

def test_delete_document(test_collection):
    doc = {"name": "Dave", "age": 40}
    test_collection.insert_one(doc)
    test_collection.delete_one({"name": "Dave"})
    result = test_collection.find_one({"name": "Dave"})
    assert result is None

