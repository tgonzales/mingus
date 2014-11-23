import tornado.web
import json
from bson import json_util

import tornado.gen


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
        yield model.get(self.request.uri)
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

class ResourceHandler(MotorHandler):
    
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

def rest_routes(objects, model):
    routes = []
    for name, cls in objects.items():
        print('Starting Server - Tornado Rest Framework')
        
        route = (r'/%s/?' % name.lower(), ResourceHandler, dict(model=model, prefix=name, mtype="list"))
        #print(route)
        print('model:{0} - list and post --> /{0}/?'.format(name.lower()))
        routes.append( route )
        
        route = (r'/%s/([0-9a-fA-F]{24,})/?' % name.lower(),  ResourceHandler, dict(model=model, prefix=name, mtype="detail"))
        #print(route)
        print('model:{0} - get, put, delete --> /{0}/([0-9a-fA-F]{{24,}})/?'.format(name.lower()))
        routes.append( route )
        
    return routes