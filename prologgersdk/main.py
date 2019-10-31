import logging
import random

from .log import ProLoggerHandler

pro_logger_handler = ProLoggerHandler(secret_key='1234567890')
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

try:
    a = [1, 2, 3, 4]
    print(a[20])
except Exception as E:
    exec (random.choice(
        ["logger.debug(E, exc_info=True)", "logger.info(E, exc_info=True)", "logger.warning(E, exc_info=True)",
         "logger.error(E, exc_info=True)"]))
