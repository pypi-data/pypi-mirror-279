from typing import Any, Optional
import redis
import boto3

class GlobyQueue:
    """
    Common interface for a queue.
    """
    def enqueue(self, item: Any) -> None:
        """Add an item to the queue."""
        raise NotImplementedError

    def dequeue(self) -> Optional[Any]:
        """Remove and return an item from the queue. Return None if the queue is empty."""
        raise NotImplementedError

    def put(self, item: Any) -> None:
        """Add an item to the queue."""
        return self.enqueue(item)

    def pop(self) -> Optional[Any]:
        """Remove and return an item from the queue. Return None if the queue is empty."""
        return self.dequeue()

    def is_empty(self) -> bool:
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

    def enqueue(self, item: Any) -> None:
        self._client.rpush(self._name, item)

    def dequeue(self) -> Optional[Any]:
        item = self._client.lpop(self._name)
        return item

    def is_empty(self) -> bool:
        return self._client.llen(self._name) == 0

class SQSQueue(GlobyQueue):
    def __init__(self, queue_name: str):
        self._sqs = boto3.resource('sqs')
        self._queue = self._sqs.get_queue_by_name(QueueName=queue_name)

    def enqueue(self, item: Any) -> None:
        self._queue.send_message(MessageBody=str(item))

    def dequeue(self) -> Optional[Any]:
        messages = self._queue.receive_messages(MaxNumberOfMessages=1)
        if not messages:
            return None
        message = messages[0]
        message.delete()
        return message.body

    def is_empty(self) -> bool:
        # Note: This is not the most efficient way to check if an SQS queue is empty and is used here for demonstration.
        # SQS's nature does not allow a straightforward way to check if it's empty without polling for messages.
        messages = self._queue.receive_messages(MaxNumberOfMessages=1, VisibilityTimeout=1, WaitTimeSeconds=1)
        return len(messages) == 0
