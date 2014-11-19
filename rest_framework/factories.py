#Factory

class ModelFactory(object):

    def __init__(self, db, objects, get_http_methods, params):
        self.db = db
        self.objects = objects
        self.get_http_methods = get_http_methods
        self.params = params

    def build(self, prefix, request, args, kwargs):
        collection = self.db[prefix]
        obj = self.objects[prefix]
        params = self.params(obj._fields, args, kwargs, request.arguments)
        return self.get_http_methods[request.method](collection, obj, params)