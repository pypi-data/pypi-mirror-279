"""
DigiRM auth plugin for HTTPie.
See https://github.com/httpie/cli/blob/master/httpie/plugins/base.py
"""
__version__ = '0.2.0'
__author__ = 'Fred A Kulack'
__licence__ = 'MIT'

from httpie.plugins import AuthPlugin

class DigiRM:
    def __init__(self, id: str=None, secret: str=None):
        self.id = id
        self.secret = secret

    def __call__(self, r):
        if self.id is None or self.secret is None:
            raise ValueError('No user or password could be resolved for the X-API-KEY-ID and X-API-KEY-SECRET HTTP headers used for DigiRM API authentication.')

        r.headers['X-API-KEY-ID'] = self.id
        r.headers['X-API-KEY-SECRET'] = self.secret
        return r

class DigiRMAuthPlugin(AuthPlugin):
    name = 'Digi Remote Manager Auth'
    auth_type = 'drm'
    auth_require = False
    netrc_parse = True
    description = 'Specifies the X-API-KEY-ID and X-API-KEY-SECRET headers for DigiRM API authentication.'

    def get_auth(self, username: str = None, password: str = None):        return DigiRM(username, password)
