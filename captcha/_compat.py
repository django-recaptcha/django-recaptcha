import sys

PY2 = sys.version_info[0] == 2
if PY2:
    text_type = unicode
    from urllib import urlencode

    from urllib2 import HTTPError, ProxyHandler, Request, build_opener, urlopen
else:
    from urllib.error import HTTPError
    from urllib.parse import urlencode
    from urllib.request import ProxyHandler, Request, build_opener, urlopen

    text_type = str
