#Factory

class ModelFactory(object):

    def __init__(self, db, objects, resource_models, params):
        self.db = db
        self.objects = objects
        self.resource_models = resource_models
        self.params = params

    def build(self, prefix, request, args, kwargs):
        collection = self.db[prefix]
        obj = self.objects[prefix]
        params = self.params(obj._fields, args, kwargs, request.arguments)
        return self.resource_models[request.method](collection, obj, params)