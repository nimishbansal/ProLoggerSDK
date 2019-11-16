import logging

from .log import ProLoggerHandler

# pro_logger_handler = ProLoggerHandler(secret_key='kfPS5HdrIc')
pro_logger_handler = ProLoggerHandler(secret_key='EXutay6NLO')
logger = logging.getLogger('testProLogger')
logger.setLevel(logging.DEBUG)
logger.addHandler(pro_logger_handler)


logger.debug("1", extra={'tags': {"abc": "hmm1"}})
logger.info("2", extra={'tags': {"def": "hmm2"}})
logger.warning("3", extra={'tags': {"ghi": "hmm3"}})
logger.error("4", extra={'tags': {"jkl": "hmm4"}})
logger.critical("5", extra={'tags': {"mno": "hmm5"}})
try:
    4 / 0
except Exception as E:
    logger.error(E, exc_info=True)

# raise KeyboardInterrupt

def fun1():
    a = [1, 2, 3, 4]
    print(a[20])


def fun2():
    b = 24
    c = 28
    fun1()


# fun2()
try:
    4 / 0
except Exception as E:
    print(E)
    print("ouyk")
    logger.debug("hmmou", 1, 2, 3, 4, exc_info=True, extra={"tags": {"abc": "Defghi"}})
