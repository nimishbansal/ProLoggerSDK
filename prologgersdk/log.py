import json
import linecache
import logging
import sys

from .Client import Client
from .utils import LEVEL_FATAL, LEVEL_VALUE_TO_LEVEL_NAME_DICT

__excepthook__ = None


def pretty_print_frame_code_lines(result, i):
    frame_data = result[i]
    print("----------x-------------x-----------x-------------------")
    print(*frame_data['previous_lines'])
    print("..........................\n" + frame_data['code_line'].strip("\n") + "\n..........................")
    print(*frame_data['next_lines'])
    print("----------x-------------x-----------x-------------------")


def get_exception_frames(exc_info):
    result = []
    exc_traceback = exc_info[2]
    frame_dict = {
        'line_no': None,
        'locals': None,
        'previous_lines': None,
        'code_line': None,
        'next_lines': None,
        'filepath': None,
        'function_name': None
    }
    while True:
        temp_dict = frame_dict.copy()
        if hasattr(exc_traceback, 'tb_frame'):
            exc_frame = exc_traceback.tb_frame
            temp_dict['locals'] = exc_frame.f_locals
            line_no = temp_dict['line_no'] = exc_traceback.tb_lineno
            f_code = getattr(exc_frame, 'f_code', None)
            if f_code:
                file_path = exc_frame.f_code.co_filename
                function_name = exc_frame.f_code.co_name
                temp_dict['filepath'] = file_path
                temp_dict['function_name'] = function_name
                no_of_lines_in_file = len(linecache.getlines(file_path))
                temp_dict['previous_lines'] = linecache.getlines(file_path)[max(0, line_no - 5):line_no - 1]
                temp_dict['code_line'] = linecache.getline(file_path, line_no)
                temp_dict['next_lines'] = linecache.getlines(file_path)[line_no:min(line_no + 5, no_of_lines_in_file)]
            result.append(temp_dict)
            exc_traceback = exc_traceback.tb_next
            if exc_traceback is None:
                break
        else:
            break
    return list(reversed(result))


class ProLoggerHandler(logging.Handler):
    def __init__(self, secret_key=None):
        super(ProLoggerHandler, self).__init__()
        self.client = Client()
        self.client.setup(secret_key=secret_key)
        self.setup_sys_hook()

    def emit(self, record):
        if hasattr(record, 'tags'):
            assert type(record.tags) == dict, "'tags' must be of type dictionary"
        else:
            record.tags = dict()

        tags = record.tags

        message = record.msg
        exc_info = record.exc_info
        level_no = record.levelno

        self.handle_logging_event(level_no=level_no, exc_info=exc_info, msg=message, tags=tags)

    def setup_sys_hook(self):
        global __excepthook__

        if __excepthook__ is None:
            __excepthook__ = sys.excepthook

        def handle_exception(*exc_info):
            self.handle_fatal_exception(exc_info=exc_info)
            __excepthook__(*exc_info)

        sys.excepthook = handle_exception

    def handle_fatal_exception(self, exc_info):
        self.handle_logging_event(LEVEL_FATAL, exc_info=exc_info, msg=None)

    def handle_logging_event(self, level_no=None, exc_info=None, msg=None, tags=None):
        """
        if record.exc_info is None
            exc_info = False
        elif record.exc_info = (None, None, None)
            exc_info = True and No exception is there at the top of stack
        else:
            exc_info = True and there is an exception at top of stack
        """
        # Used for notifying too
        if tags is None:
            tags = {}
        else:
            assert type(tags) == dict

        # populate basic tags
        tags['level'] = LEVEL_VALUE_TO_LEVEL_NAME_DICT[level_no]

        main_data = {'level': level_no, 'tags': tags, 'message': None, 'title': msg}
        is_exception = False
        exception_name = None
        exception_string = None
        exception_frames_data = None

        if exc_info is None or exc_info is (None, None, None):
            pass
        else:
            exception_name = exc_info[0].__name__
            exception_string = str(exc_info[1])
            exception_frames_data = get_exception_frames(exc_info=exc_info)
            is_exception = True
            main_data['message'] = exception_name + ', ' + exception_string
            if main_data['title'] is None:
                main_data['title'] = exception_name
                main_data['message'] = exception_string

        if main_data['message'] is None:
            main_data['message'] = str(msg)
        complete_data = {'main_data': main_data, 'full_data': {'exception': None}}
        if is_exception:
            complete_data['full_data']['exception'] = {}
            complete_data['full_data']['exception']['name'] = exception_name
            complete_data['full_data']['exception']['string'] = exception_string
            complete_data['full_data']['exception']['frames'] = exception_frames_data

        complete_data = json.loads(json.dumps(complete_data, default=lambda x: repr(x)))
        self.client.send_data(data=complete_data)


if __name__ == '__main__':
    pro_logger_handler = ProLoggerHandler(secret_key='EXutay6NLO')
    logger = logging.getLogger('testProLogger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(pro_logger_handler)

    def fun3(x, y, z):
        a = 4
        b = 5
        z = 4/0

    def fun2():
        z =9
        fun3(10, 20, z)

    try:
        print(fun2())
    except Exception as E:
        print("ouu")
        logger.warning("he hehehe haas dele", exc_info=True)
