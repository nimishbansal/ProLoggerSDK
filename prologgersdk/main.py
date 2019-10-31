import inspect
import linecache
import logging
import random
from inspect import stack

from .log import ProLoggerHandler

pro_logger_handler = ProLoggerHandler(secret_key='9876543210')
logger = logging.getLogger('testProLogger')
logger.setLevel(logging.DEBUG)
logger.addHandler(pro_logger_handler)
# logger.debug("1", extra={'tags': {"aww": "hmm1"}})
# logger.info("2", extra={'tags': {"aww": "hmm2"}})
# logger.warning("3", extra={'tags': {"aww": "hmm3"}})
# logger.error("4", extra={'tags': {"aww": "hmm4"}})
# logger.critical("5", extra={'tags': {"aww": "hmm5"}})
try:
    4 / 0
except Exception as E:
    logger.error(E, exc_info=True)

# raise KeyboardInterrupt

a = [1, 2, 3, 4]
print(a[20])
