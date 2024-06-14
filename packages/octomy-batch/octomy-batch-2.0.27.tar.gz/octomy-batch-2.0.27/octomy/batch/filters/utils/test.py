import time
import random
import logging

logger = logging.getLogger(__name__)


def batch_filter_entrypoint(batch_item={}, config={}):
	data = batch_item.get("data", "data-field-missing")
	logger.info(f"TEST BATCH FILTER IS RUNNING WITH {data} ######################")
	if data == "fast":
		logger.info("We are simulating a fast task by completing immediately")
		return "Task completed quickly", None
	elif data == "slow":
		logger.info("We are simulating a slow task by completing  after 1 min")
		time.sleep(60 * 1)
		return "Task completed slowly (60 seconds)", None
	elif data == "random":
		time_to_wait = 60.0 * random.uniform(0, 1)
		logger.info(f"We are simulating a randomly fast task by completing after a random interval between 0 and 1 minute. In this case it was {time_to_wait} seconds.")
		time.sleep(time_to_wait)
		return f"Task completed after random time ({time_to_wait} seconds)", None
	elif data == "hang":
		logger.info("We are testing a hanging task by just waiting forever")
		time.sleep(1000000000)
		return "Task hung", None
	elif data == "fail":
		logger.info("We are testing a task that returns failure")
		return None, "Task is failing on purpose"
	elif data == "exception":
		logger.info("We are testing a task that produces an exception during execution")
		raise Exception("This is a failure test")
		return "Task with exception somehow succeeded (not expected)", None
	else:
		logger.info(f"The data '{data}' was not recognized and so we don't know what to test.")
	return None, f"Unknown test task type: {data}"
