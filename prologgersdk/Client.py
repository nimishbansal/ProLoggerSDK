import json
import requests
import sys

sys.path.append("/home/nimish/PycharmProjects/ProLoggerBackend/")
from .utils import AUTH_ENDPOINT, EVENT_ACCEPT_ENDPOINT, LEVEL_NOTSET

# def foo(exctype, value, tb):
#     print('My Error Information')
#     print('Type:', exctype)
#     print('Value:', value)
#     print('Traceback:', tb)
#
#
# sys.excepthook = foo

# print(4 / 0)


class Client(object):
    def __init__(self):
        self.setup_finished = False
        self.secret_key = None

    def setup(self, secret_key=None):
        if secret_key is None:
            raise AssertionError("secret_key can't be None")
        self.verify_secret_key(secret_key)
        return 'success'

    def verify_secret_key(self, secret_key):
        r = requests.post(AUTH_ENDPOINT,
                          data=json.dumps({'secret_key': secret_key}),
                          headers={'Content-type': 'application/json'}, )

        if r.status_code == 200:
            if r.json()['status'] == 'success':
                self.setup_finished = True
                self.secret_key = secret_key
                return True
            else:
                raise AssertionError(r.json()['message'])
        else:
            raise AssertionError('Some error occured with response code =', r.status_code)

    @staticmethod
    def format_log_entry_data(data):
        if 'level' not in data:
            data['level'] = LEVEL_NOTSET
        if 'title' not in data:
            data['title'] = ' '
        if 'tags' not in data:
            data['tags'] = {}
        if 'message' not in data:
            data['message'] = ' '

    def send_data(self, data):
        if not self.setup_finished:
            raise AssertionError('call setup() with secret_key first')
        print(data)
        self.format_log_entry_data(data['main_data'])
        r = requests.post(EVENT_ACCEPT_ENDPOINT,
                          data=json.dumps(data),
                          headers={'Content-type': 'application/json', 'Project-Token': self.secret_key}, )
