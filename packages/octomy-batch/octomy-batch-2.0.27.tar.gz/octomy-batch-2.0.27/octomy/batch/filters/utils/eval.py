import logging
import pprint

logger = logging.getLogger(__name__)

batch_item = {}
config = {}


def batch_filter_entrypoint(bi={}, c={}):
	global batch_item
	global config
	batch_item = bi
	config = c
	code = batch_item.get("data", None)
	if not code:
		return None, "No code for eval"
	logger.info(f"EVAL CODE #####################")
	logger.info(code)
	logger.info(f"EVAL LOG ######################")
	try:
		exec(code, globals(), globals())
		logger.info(f"EVAL DONE WITH SUCCESS ########")
		return "Eval completed successfully", None
	except Exception as e:
		logger.error(f"Eval failed with {e}", exc_info=True)
		logger.info(f"EVAL DONE WITH FAILURE ########")
		return None, f"Eval failed with {e}"
