import unittest
from urllib.parse import urlparse, parse_qs

from http import cookies

class TestUtil(unittest.TestCase):
    def test_urllib_01(self):
        o = urlparse('http://127.0.0.1/admin?page=users&pagination=2')
        # print(o)
        params = parse_qs(o.query)
        # print(params)

        # path
        self.assertEqual(o.path, '/admin')
        self.assertEqual(params['page'], ['users'])

    def test_http_cookie_01(self):
        c = cookies.SimpleCookie()
        c.load('session=7fbad53f-168a-4044-907e-98a61a9dc676')

        print("aaaa")
        print(c['session'].value)