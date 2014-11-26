# ToDo > urllib2 and Unitest

import random
import unittest
import requests

# python -m unittest -v

uri = 'http://localhost:8888/v1/song/'

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(10))

    def test_bulk_objs_status_code(self):
        params = '?bulk={"insert":[{"slug":"1","song":"My Funny Valentine"},{"slug":"2","song":"500 Miles High"},{"slug":"3","song":"All of Me"}]}'
        r = requests.post('{0}{1}'.format(uri,params))
        self.assertEqual(r.status_code, 200)
        r.connection.close()

if __name__ == '__main__':
    unittest.main()