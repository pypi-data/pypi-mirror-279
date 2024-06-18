"""
DigiRM auth plugin for HTTPie.
See https://github.com/httpie/cli/blob/master/httpie/plugins/base.py
"""
__version__ = '0.3.0'
__author__ = 'Fred A Kulack'
__licence__ = 'MIT'

import re
import base64
from httpie.plugins import AuthPlugin

API_KEY_ID_REGEX = '[0-9a-f]{32}'
API_KEY_SECRET_REGEX = '[0-9a-f]{64}'

class DigiRM:
    def __init__(self, id: str=None, secret: str=None):
        self.id = id
        self.secret = secret

    def __call__(self, r):
        if self.id is None or self.secret is None:
            raise ValueError('No user or password could be resolved for the X-API-KEY-ID and X-API-KEY-SECRET HTTP headers used for DigiRM API authentication.')

        if not re.match(API_KEY_ID_REGEX, self.id) or not re.match(API_KEY_SECRET_REGEX, self.secret):
            # use Basic auth
            r.headers['Authorization'] = f'Basic {base64.b64encode(f"{self.id}:{self.secret}".encode()).decode()}'
        else:
            # This is an API key
            r.headers['X-API-KEY-ID'] = self.id
            r.headers['X-API-KEY-SECRET'] = self.secret
        return r

class DigiRMAuthPlugin(AuthPlugin):
    name = 'Digi Remote Manager Auth'
    auth_type = 'drm'
    auth_require = False
    netrc_parse = True
    description = 'Specifies the X-API-KEY-ID and X-API-KEY-SECRET headers for DigiRM API authentication, HTTP basic auth for other authentication.'

    def get_auth(self, username: str = None, password: str = None):
        return DigiRM(username, password)
