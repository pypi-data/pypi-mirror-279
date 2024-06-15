"""
DigiRM auth plugin for HTTPie.
"""
try:
    import urlparse
except ImportError:
    import urllib.parse

__version__ = '0.1.0'
__author__ = 'Fred A Kulack'
__licence__ = 'MIT'

class DigiRMAuth:
    def __init__(self, access_id, secret_key):
        self.access_id = access_id
        self.secret_key = secret_key.encode('ascii')

    def __call__(self, r):
        # method = r.method.upper()
        #
        # content_type = r.headers.get('content-type')
        # if not content_type:
        #     content_type = ''
        #
        # content_md5  = r.headers.get('content-md5')
        # if not content_md5:
        #     content_md5 = ''
        #
        # httpdate = r.headers.get('date')
        # if not httpdate:
        #     now = datetime.datetime.utcnow()
        #     httpdate = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
        #     r.headers['Date'] = httpdate
        #
        # url  = urlparse.urlparse(r.url)
        # path = url.path
        # if url.query:
        #   path = path + '?' + url.query
        #
        # string_to_sign = '%s,%s,%s,%s,%s' % (method, content_type, content_md5, path, httpdate)
        # digest = hmac.new(self.secret_key, string_to_sign, hashlib.sha1).digest()
        # signature = base64.encodestring(digest).rstrip()

        r.headers['X-API-KEY'] = self.access_id
        r.headers['X-API-KEY-SECRET'] = self.secret_key
        return r

class DigiRMAuthPlugin(DigiRMAuth):

    name = 'DigiRM auth'
    auth_type = 'digirm'
    auth_require = False
    netrc_parse = True
    description = 'Specify the X-API-KEY and X-API-KEY-SECRET headers for DigiRM API authentication.'

    def get_auth(self, access_id, secret_key):
        return DigiRMAuth(access_id, secret_key)
