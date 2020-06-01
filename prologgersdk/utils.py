import linecache
from inspect import stack

# BASE_URL = 'http://192.168.0.107:5000/'
# BASE_URL = 'http://3.17.182.118:5000/'
BASE_URL = 'http://18.216.69.35:5000/'
AUTH_ENDPOINT = BASE_URL + 'projects/verify_secret_key/'
EVENT_ACCEPT_ENDPOINT = BASE_URL + 'projects/new_log_entry/'

LEVEL_NOTSET = 0
LEVEL_DEBUG = 10
LEVEL_INFO = 20
LEVEL_WARNING = 30
LEVEL_ERROR = 40
LEVEL_CRITICAL = 50
LEVEL_FATAL = 50  # Critical and Fatal are conceptually the same

NOTSET = 'NOTSET'
DEBUG = 'DEBUG'
INFO = 'INFO'
WARNING = 'WARNING'
ERROR = 'ERROR'
CRITICAL = 'CRITICAL'
FATAL = 'FATAL'

LogEntryLevelChoices = [
    (LEVEL_NOTSET, NOTSET),
    (LEVEL_DEBUG, DEBUG),
    (LEVEL_INFO, INFO),
    (LEVEL_WARNING, WARNING),
    (LEVEL_ERROR, ERROR),
    (LEVEL_CRITICAL, CRITICAL),
    (LEVEL_FATAL, FATAL),
]

LEVEL_NAME_TO_LEVEL_VALUE_DICT = {
    NOTSET: LEVEL_NOTSET,
    DEBUG: LEVEL_DEBUG,
    WARNING: LEVEL_WARNING,
    ERROR: LEVEL_ERROR,
    INFO: LEVEL_INFO,
    FATAL: LEVEL_FATAL,
    CRITICAL: LEVEL_CRITICAL
}

LEVEL_VALUE_TO_LEVEL_NAME_DICT = {
    LEVEL_NOTSET: NOTSET,
    LEVEL_DEBUG: DEBUG,
    LEVEL_WARNING: WARNING,
    LEVEL_ERROR: ERROR,
    LEVEL_INFO: INFO,
    LEVEL_FATAL: FATAL,
    LEVEL_CRITICAL: CRITICAL
}


def get_frame_data():
    """
    Sample structure :

    frames_data = {
        'no_of_frames': None,
        'frames': [
            {
                'code_context': None,
                'pre_code_context': None,
                'post_code_context': None,
                'line_no': None,
                'filename': None,
                'locals': {

                },
            }
        ]
    }

    :return:
    """
    current_stack = stack()
    _frames_data = {'frames': [], 'no_of_frames': len(current_stack)}

    for frame_info in current_stack:
        current_frame = dict()
        filename = frame_info.filename
        line_no = frame_info.lineno
        no_of_lines_in_file = len(linecache.getlines(filename))

        pre_code_lines = linecache.getlines(filename)[max(0, line_no - 5):line_no - 1]
        post_code_lines = linecache.getlines(filename)[line_no:min(line_no + 5, no_of_lines_in_file)]

        current_frame['filename'] = filename
        current_frame['line_no'] = line_no
        current_frame['locals'] = frame_info.frame.f_locals
        current_frame['code_context'] = frame_info.code_context
        current_frame['pre_code_context'] = pre_code_lines
        current_frame['post_code_context'] = post_code_lines

        _frames_data['frames'].append(current_frame)

    return _frames_data
