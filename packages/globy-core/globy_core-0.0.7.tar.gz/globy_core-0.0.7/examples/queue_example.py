import sys
sys.path.append('../src')

from globy_core.logging.logger import Logger
from globy_core.store.queue import RedisQueue as GlobyQueue

# This example demonstrates how to use the RedisQueue class with the Logger class
if __name__ == "__main__":
    logger = Logger().logger
    queue = GlobyQueue("test_queue", logger)
    queue.put("test")
    print(queue.pop())
    logger.info("Queue test passed")