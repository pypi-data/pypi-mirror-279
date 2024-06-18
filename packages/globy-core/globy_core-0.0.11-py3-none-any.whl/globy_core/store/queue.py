from typing import Any, Optional
import redis
import boto3

class GlobyQueue:
    """
    Common interface for a queue.
    """
    def enqueue(self, key: str, item: Any) -> None:
        """Add an item to the queue."""
        raise NotImplementedError

    def dequeue(self, key: str) -> Optional[Any]:
        """Remove and return an item from the queue. Return None if the queue is empty."""
        raise NotImplementedError

    def put(self, key: str, item: Any) -> None:
        """Add an item to the queue."""
        return self.enqueue(key, item)

    def pop(self, key: str) -> Optional[Any]:
        """Remove and return an item from the queue. Return None if the queue is empty."""
        return self.dequeue(key)

    def is_empty(self, key: str) -> bool:
        """Return True if the queue is empty, False otherwise."""
        raise NotImplementedError

class RedisQueue(GlobyQueue):
    """
    A queue implementation using Redis.
    """
    def __init__(self, name: str, logger=None, host='localhost', port=6379, db=0):
        self._name = name
        self._logger = logger  # Not implemented
        self._client = redis.Redis(host=host, port=port, db=db)

    def push(self, item: Any) -> None:
        self._client.rpush(self._name, item)

    def pop(self, key: str) -> Optional[Any]:
        item = self._client.lpop(key)
        return item

    def enqueue(self, key: str, item: Any) -> None:
        return self.push(key, item)

    def dequeue(self, key: str) -> Optional[Any]:
        return self.pop(key)

    def is_empty(self, key: str) -> bool:
        return self._client.llen(key) == 0

class SQSQueue(GlobyQueue):
    NotImplementedError
