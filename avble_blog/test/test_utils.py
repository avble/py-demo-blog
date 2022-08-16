import unittest
from urllib.parse import urlparse, parse_qs

class TestUtil(unittest.TestCase):
    def test_urllib_01(self):
        o = urlparse('http://127.0.0.1/admin?page=users&pagination=2')
        # print(o)
        params = parse_qs(o.query)
        # print(params)

        # path
        self.assertEqual(o.path, '/admin')
        self.assertEqual(params['page'], ['users'])

