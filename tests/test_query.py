import random
import unittest
import requests
import json
# python -m unittest tests/test_status_code.py -v

uri = 'http://localhost:8888/v1/song'
r = requests.get(uri)
objects = r.json()
obj = [obj['_id']['$oid'] for obj in objects['objects']]
obj_uri = obj[0] 
r.connection.close()

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(10))

    def test_query(self):
        pass 

if __name__ == '__main__':
    unittest.main()
    