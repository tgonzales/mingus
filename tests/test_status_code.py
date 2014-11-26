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


    def test_post_obj_status_code(self):
        payload = {"slug":"88","artist":"8MikeArtistMike", "song":"8SongToSongSong", "rank":8001}
        r = requests.post(uri, data=json.dumps(payload))
        self.assertEqual(r.status_code, 200)
        r.connection.close()
        
    '''
    	GET - Status Code
    '''
    def test_get_list_status_code(self):
        r = requests.get(uri)
        self.assertEqual(r.status_code, 200)
        r.connection.close()

    def test_get_simple_filter_status_code(self):
        r = requests.get('{0}/{1}'.format(uri, '?slug=1'))
        r2 = requests.get('{0}/{1}'.format(uri, '?song=My%20Funny%20Valetine'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r2.status_code, 200)
        r.connection.close()
        r2.connection.close()

    def test_get_obj_status_code(self):
        r = requests.get('{0}/{1}'.format(uri, obj_uri))
        self.assertEqual(r.status_code, 200)
        r.connection.close()

    def test_get_obj_status_code_404(self):
        r = requests.get('{0}/{1}'.format(uri, 'geterror'))
        self.assertEqual(r.status_code, 404)
        r.connection.close()

    '''
    	PUT - Status Code
    '''
    def test_put_objs_status_code(self):
        payload = {"slug":"333","song":"All of Me Update"}
        url = '{0}/{1}/'.format(uri, obj_uri)
        r = requests.put(url, data=json.dumps(payload))
        self.assertEqual(r.status_code, 200)
        r.connection.close()

    '''
    	DELETE - Status Code
    '''
    #@unittest.skip("showing class skipping")
    def test_delete_objs_status_code(self):
        r = requests.delete('{0}/{1}'.format(uri, obj_uri))
        self.assertEqual(r.status_code, 200)
        r.connection.close()

    '''
    	PATCH - Status Code
    '''
    def test_patch_objs_status_code(self):
        url = '{0}/{1}/'.format(uri, obj_uri)
        payload = {"slug":"33888883"}
        r = requests.patch(url, data=json.dumps(payload))
        self.assertEqual(r.status_code, 200)
        r.connection.close()

if __name__ == '__main__':
    unittest.main()
    