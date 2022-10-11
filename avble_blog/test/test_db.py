import unittest
from avble_blog import db


class TestDb(unittest.TestCase):
    # post db
    def test_01(self):
        posts = db.post_read()
        for p in posts:
            print (p)

        self.assertEqual(len(posts), 5)
        