# ToDo > urllib2 and Unitest

import random
import unittest
import requests

# python -m unittest -v

uri = 'http://localhost:8888/song/'

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(10))

    '''
    	POST - Status Code
    '''
    def test_bulk_objs_status_code(self):
        r = requests.post('{0}{1}'.format(uri, '?bulk={"insert":[{"slug":"1","song":"My Funny Valentine"},{"slug":"2","song":"500 Miles High"},{"slug":"3","song":"All of Me"}]}'))
        self.assertEqual(r.status_code, 200)
        r.connection.close()

    def test_post_objs_status_code(self):
	    pass

    '''
    	GET - Status Code
    '''

    def test_get_list_status_code(self):
        r = requests.get(uri)
        self.assertEqual(r.status_code, 200)
        r.connection.close()

    def test_get_simple_filter_status_code(self):
        r = requests.get('{0}{1}'.format(uri, '?slug=1'))
        r2 = requests.get('{0}{1}'.format(uri, '?song=My%20Funny%20Valetine'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r2.status_code, 200)
        r.connection.close()
        r2.connection.close()

    def test_get_obj_status_code(self):
        r = requests.get('{0}{1}'.format(uri, '546d65e4d1e5ba1643f36e27'))
        self.assertEqual(r.status_code, 200)
        r.connection.close()

    def test_get_obj_status_code_404(self):
        r = requests.get('{0}{1}'.format(uri, 'geterror'))
        self.assertEqual(r.status_code, 404)
        r.connection.close()

    '''
    	PUT - Status Code
    '''
    def test_put_objs_status_code(self):
	    pass

    '''
    	DELETE - Status Code
    '''
    def test_delete_objs_status_code(self):
        r = requests.delete('{0}{1}'.format(uri, '546d65e4d1e5ba1643f36e27'))
        self.assertEqual(r.status_code, 200)
        r.connection.close()

    '''
    	PATCH - Status Code
    '''
    def test_patch_objs_status_code(self):
	    pass


if __name__ == '__main__':
    unittest.main()