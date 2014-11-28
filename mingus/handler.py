import tornado.web
import tornado.escape
import json
from bson import json_util

import tornado.gen
from mingus.serializers import JSONSerializer

class MotorHandler(tornado.web.RequestHandler):
    def initialize(self, model, prefix, mtype):
        self.model = model
        self.prefix = prefix
        self.mtype = mtype
        self.response_dict = ""

    def sendJson(self, data):
        data = json.dumps(data, sort_keys=True, indent=4, default=json_util.default)
        self.write(data)


def generate_response_get(request):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def _request(self, *args, **kwargs):

        model = self.model.build(self.prefix, self.request, args, kwargs)
        yield model.getobj(self.request.uri)
        self.response_dict = model.getResponseDict()
        tornado.gen.coroutine(request)(self, *args, **kwargs)

    return _request

def generate_response_getlist(request):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def _request(self, *args, **kwargs):

        model = self.model.build(self.prefix, self.request, args, kwargs)
        yield model.getlist(self.request.uri)
        self.response_dict = model.getResponseDict()
        tornado.gen.coroutine(request)(self, *args, **kwargs)

    return _request

def generate_response_post(request):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def _request(self, *args, **kwargs):

        model = self.model.build(self.prefix, self.request, args, kwargs)
        yield model.post()
        self.response_dict = model.getResponseDict()
        tornado.gen.coroutine(request)(self, *args, **kwargs)

    return _request


def generate_response_put(request):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def _request(self, *args, **kwargs):

        model = self.model.build(self.prefix, self.request, args, kwargs)
        yield model.put()
        self.response_dict = model.getResponseDict()
        tornado.gen.coroutine(request)(self, *args, **kwargs)

    return _request


def generate_response_delete(request):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def _request(self, *args, **kwargs):

        model = self.model.build(self.prefix, self.request, args, kwargs)
        yield model.delete()
        self.response_dict = model.getResponseDict()
        tornado.gen.coroutine(request)(self, *args, **kwargs)

    return _request


def generate_response_patch(request):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def _request(self, *args, **kwargs):

        model = self.model.build(self.prefix, self.request, args, kwargs)
        yield model.patch()
        self.response_dict = model.getResponseDict()
        tornado.gen.coroutine(request)(self, *args, **kwargs)

    return _request

'''
def generate_response_getFilters(request):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def _request(self, *args, **kwargs):

        model = self.model.build(self.prefix, self.request, args, kwargs)
        yield model.getlist(self.request.uri)
        self.response_dict = model.getResponseDict()
        tornado.gen.coroutine(request)(self, *args, **kwargs)

    return _request
'''

class DetailHandler(MotorHandler):
    
    SUPPORTED_METHODS = ("GET", "POST", "PUT","DELETE", "PATCH")
    
    @generate_response_get
    def get(self, *args, **kwargs):
        self.sendJson(self.response_dict)

    @generate_response_post
    def post(self, *args, **kwargs):
        self.sendJson(self.response_dict)

    @generate_response_put
    def put(self, *args, **kwargs):
        self.sendJson(self.response_dict)

    @generate_response_delete
    def delete(self, *args, **kwargs):
        self.sendJson(self.response_dict)

    @generate_response_patch
    def patch(self, *args, **kwargs):
        self.sendJson(self.response_dict)


class ListHandler(MotorHandler):
    
    SUPPORTED_METHODS = ("GET", "POST")
    
    @generate_response_getlist
    def get(self, *args, **kwargs):
        self.sendJson(self.response_dict)

    @generate_response_post
    def post(self, *args, **kwargs):
        self.sendJson(self.response_dict)


class ESHandler(MotorHandler):
    '''
    ElasticSearch Handler
    '''
    def get(self, *args, **kwargs):
        params = tornado.escape.to_unicode(self.get_argument('q'))
 
        j = JSONSerializer() 
        d = j.deserialize(params)

        print(repr(d))
        print(repr(type(d)))
        self.write(str(d['asdf']))

'''
class FiltersHandler(MotorHandler):
    @generate_response_getFilters
    def get(self, *args, **kwargs):
        self.sendJson(self.response_dict)
'''


def rest_routes(objects, model, version):
    routes = []
    for name, cls in objects.items():
        #version = 'v1'
        uri = '{0}/{1}'.format(version,name.lower())
        route = (r'/%s/?' % uri, ListHandler, dict(model=model, prefix=name, mtype="list"))
        #print(route)
        print('model:{0} - /{1}/?  --> allowed method: GET POST'.format(name.lower(),uri))
        routes.append( route )
        
        route = (r'/%s/([0-9a-fA-F]{24,})/' % uri, DetailHandler, dict(model=model, prefix=name, mtype="detail"))
        #print(route)
        print('model:{0} - /{1}/([0-9a-fA-F]{{24,}})/  --> allowed method: GET POST PUT PATCH DELETE'.format(name.lower(),uri))
        routes.append( route )

        route = (r'/%s/search/?' % uri, ESHandler, dict(model=model, prefix=name, mtype="search"))
        #print(route)
        print('model:{0} - /{1}/search/? --> allowed method: GET'.format(name.lower(),uri))
        routes.append( route )
        '''
        route = (r'/%s/filters/?' % uri, FiltersHandler, dict(model=model, prefix=name, mtype="search"))
        print('model:{0} - get --> /{1}/filters/?'.format(name.lower(),uri))
        routes.append( route )
        '''
    return routes