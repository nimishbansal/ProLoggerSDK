import logging
import sys

import time

from pytz import unicode

from .utils import FATAL, LEVEL_FATAL
from .Client import Client
from inspect import getframeinfo, stack

__excepthook__ = None


class ProLoggerHandler(logging.Handler):
    def __init__(self, secret_key=None):
        super(ProLoggerHandler, self).__init__()
        self.client = Client()
        self.client.setup(secret_key=secret_key)
        self.setup_sys_hook()

    def emit(self, record):
        level_no = record.levelno
        message = ""
        if hasattr(record, 'tags'):
            assert type(record.tags) == dict, "'tags' must be of type dictionary"
        else:
            record.tags = dict()

        try:
            title = unicode(record.msg)
        except UnicodeDecodeError:
            title = repr(record.msg)[1:-1]

        print(record.msg, record.exc_info)
        if record.exc_info is not None:
            title, message = self.get_title_and_message_from_exc_info(record.exc_info)
        data = {'level': level_no, 'title': title, 'message': message, "tags": record.tags}
        self.client.send_data(data=data)
        # print(dir(record))
        # if record.levelname == "ERROR":
        #     print(record.created, record.exc_info, record.exc_text, record.filename, record.funcName,
        #           record.lineno, record.msg, record.pathname, record.name)
        #     print(record.stack_info)
        #     for j in stack()[::-1]:
        #         print(j.filename, j.function, j.lineno, j.code_context[0].strip())
        #         if j.filename == record.pathname and j.function == record.funcName and j.lineno == record.lineno:
        #             break

    def setup_sys_hook(self):
        global __excepthook__

        if __excepthook__ is None:
            __excepthook__ = sys.excepthook

        def handle_exception(*exc_info):
            self.handle_fatal_exception(exc_info=exc_info)
            __excepthook__(*exc_info)

        sys.excepthook = handle_exception

    def get_title_and_message_from_exc_info(self, exc_info):
        try:
            title = unicode(exc_info[0].__name__)
        except UnicodeDecodeError:
            title = repr(exc_info[0].__name__)[1:-1]

        try:
            message = unicode(exc_info[1])
        except UnicodeDecodeError:
            message = repr(exc_info[1][1:-1])

        return title, message

    def handle_fatal_exception(self, exc_info):
        print("handling fatal")
        level = LEVEL_FATAL
        title, message = self.get_title_and_message_from_exc_info(exc_info)
        data = {'level': level, 'title': title, 'tags': {}, 'message': message}
        self.client.send_data(data=data)


if __name__ == '__main__':
    pro_logger_handler = ProLoggerHandler(secret_key='1234567890')
    logger = logging.getLogger('testProLogger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(pro_logger_handler)
    # logger.debug("okies", extra={'tags': {'TenantPaymentBatch': {}}})
    try:
        print(4 / 0)
    except Exception as E:
        logger.error(E, exc_info=True)
