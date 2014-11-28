# ToDo > urllib2 and Unitest

import random
import unittest
import requests

# python -m unittest -v

uri = 'http://localhost:8888/v1/song'

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(10))

    def test_bulk_objs_status_code(self):
        params = '?bulk={"insert":[\
        {"rank":10, "score":8, "slug":"1", "artist":"Duke Elington", "song":"My Funny Valentine"},\
        {"rank":9,  "score":8, "slug":"2", "artist":"Duke Elington", "song":"500 Miles High"},\
		{"rank":8,  "score":8, "slug":"3", "artist":"Duke Elington", "song":"Days of Wine and Roses"},\
		{"rank":12, "score":6, "slug":"12","artist":"Duke Elington", "song":"All of Me"}\
        ]}'
        r = requests.post('{0}/{1}'.format(uri,params))
        self.assertEqual(r.status_code, 200)
        r.connection.close()

if __name__ == '__main__':
    unittest.main()

'''
        {"rank":7,  "score":8, "slug":"4", "artist":"Duke Elington", "song":"Stella by Starlight"},\
		{"rank":6,  "score":9, "slug":"5", "artist":"Duke Elington", "song":"Summertime"},\
		{"rank":5,  "score":9, "slug":"6", "artist":"Duke Elington", "song":"Safira"},\
		{"rank":4,  "score":9, "slug":"7", "artist":"Duke Elington", "song":"Waltz for Branca"},\
		{"rank":3,  "score":6, "slug":"8", "artist":"Duke Elington", "song":"Zyryab"},\
		{"rank":2,  "score":6, "slug":"9", "artist":"Duke Elington", "song":"After Midnight"},\
		{"rank":1,  "score":6, "slug":"10","artist":"Duke Elington", "song":"Autumn Leaves"},\
		{"rank":11, "score":6, "slug":"11","artist":"Duke Elington", "song":"Aquarela do Brasil"},\

'''