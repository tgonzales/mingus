from schematics.types.base import GeoPointType
from schematics.types.compound import ListType, DictType, ModelType

import tornado.gen
import tornado.web
import tornado.escape
from schematics.exceptions import ValidationError, ModelConversionError
from bson.objectid import ObjectId
import json
import datetime

from mingus.serializers import JSONSerializer

class ModelParams(object):
    def __init__(self, fields, args, kwargs, arguments):
        self.fields = fields
        self.args = args
        self.kwargs = kwargs
        self.arguments = arguments

    def getFieldKeys(self):
        return self.fields.keys()

    def getParams(self):
        """
        Check the schematic object to see if arguments from Tornado can be lists or dictionaries
        """
        types = [DictType, GeoPointType, ListType, ModelType]
        fieldkeys = self.fields.keys()

        j = JSONSerializer() 
        if 'q' in self.arguments:
            params = tornado.escape.to_unicode(self.arguments['q'][0])
            params = tornado.escape.json_decode(params)
            self.arguments = params
        else:
            for k,v in self.arguments.items():
                if type(v) is list and k in fieldkeys and self.fields[k] not in types:
                    self.arguments[k] = self.arguments[k][0].decode("utf-8")

        if len(self.args):
            self.arguments['_id'] = self.args[0]

        return self.arguments

    def getParamsParse(self):
        """
        Check the schematic object to see if arguments from Tornado can be lists or dictionaries
        """
        #types = [DictType, GeoPointType, ListType, ModelType]
        #fieldkeys = self.fields.keys()

        j = JSONSerializer() 
        if 'bulk' in self.arguments:
            params = tornado.escape.to_unicode(self.arguments['bulk'][0])
            params = tornado.escape.json_decode(params)
            self.arguments['bulk'] = params
        else:
            for k,v in self.arguments.items():
                self.arguments =  j.deserialize(k)
                break

        if len(self.args):
            self.arguments['_id'] = self.args[0]

        return self.arguments


class Model(object):

    responseDict = ""

    def __init__(self, collection, schematic, params):
        self.collection = collection
        self.schematic = schematic
        self.params = params

    def setResponseDict(self):

        """
            Main logic for request is performed here
              self.collection ( mongo collection )
              self.schematic ( schematic model )
              self.params ( ModelParams )
            Nothing is returned because generally a coroutine and yield statement is used.
        """
    def pagination(self):
        params = self.params.getParams()

        if 'limit' in params: 
            limit = params.get('limit', 50)
            if int(limit[0]) > 100:
                limit = 100
            else:
                limit = int(limit[0])
        else:
            limit = 50

        if 'page' in params:
            page = int(params['page'][0])
        else:
            page = 1

        pagination = {}
        pagination['page'] = page
        pagination['limit'] = limit
        pagination['next'] = page + 1
        previous = page - 1
        if previous < 1:
            previous = None 
        pagination['previous'] = previous 
        return pagination


    def setResponseDictSuccess(self, result, meta=None):
        if meta:
            self.responseDict = {"status": "Success", "meta":meta, "objects":result}
        else:
            self.responseDict = {"status": "Success", "object":result}

    def setResponseDictErrors(self, errors):
        self.responseDict = {"status": "Errors",  "errors": errors}

    def getIdDict(self):
        params = self.params.getParams()
        if 'id' in params:
            oid = {'id':int(params['id'])}
        elif '_id' in params:
            oid = {'_id':ObjectId(params['_id'])}
        else:
            oid = None
        return oid

    def getSlace(self, **pagination):
        end = pagination['page'] * pagination['limit']
        start = end - pagination['limit']
        slace = {'start':start, 'end':end} 
        return slace

    def getResponseDict(self):
        return self.responseDict


    def blacklist(self):
        f = self.schematic()
        try:
            f_whitelist = [field for field in f.to_primitive(role='public').keys()]
            print(f_whitelist)

            blacklist = {k:0 for k in self.params.getFieldKeys() if k not in f_whitelist}
            print(blacklist)
        except:
            blacklist = None
        return blacklist        

    def queryset(self):
        f = self.schematic()
        params = self.params.getParams()
        try:
            query = f.queryset()
            print('query ~~~~~~~~~~~~~~~~~~')
            print(query)
            for k,v in query.items():
                params[k] = v
            print('params ~~~~~~~~~~~~~~~~~~')
            print(params)
        except:
            pass
        return params   

class ResourceModel(Model):


    @tornado.gen.coroutine
    def getlist(self, uri):
        """
        Get a list of results
        """
        blacklist = self.blacklist()
        params = self.queryset()
        pagination = self.pagination()
        slace = self.getSlace(**pagination)
        start, end = (slace['start'], slace['end'])
        try:
            count = yield self.collection.find(params)[start:end].count()
            cursor = self.collection.find(params,blacklist).sort([('_id', -1)])[start:end]
            meta = {
                "limit": pagination['limit'],
                "next": pagination['next'],
                "offset": pagination['page'],
                "previous": pagination['previous'],                    
            }
            meta['total_count'] = str(count)
            if count <  pagination['limit']:
                meta['next'] = None
            objects = []
            while (yield cursor.fetch_next):
                obj = cursor.next_object()
                obj['uri'] = uri + str(obj["_id"])
                objects.append(obj)
            results = [document for document in objects]
            self.setResponseDictSuccess(results,meta)
        except Exception as e:
            self.setResponseDictErrors("Not Found!")
        return


    @tornado.gen.coroutine
    def getobj(self, uri):
        """
        Get a single result
        """
        #params = self.params.getParams()
        oid = self.getIdDict()
        blacklist = self.blacklist()
        try:
            result = yield self.collection.find_one(oid,blacklist)
            result['_id'] = str(result['_id'])
            result['uri'] = uri
            self.setResponseDictSuccess(result)
        except Exception as e:
            self.setResponseDictErrors("Not Found!")
        return


    @tornado.gen.coroutine
    def post(self):
        params = self.params.getParamsParse()

        if 'bulk' in params:
            try:
                self.bulk()
                self.setResponseDictSuccess({"bulk":"Implemented"})
            except ValidationError as e:
                self.setResponseDictErrors(e)
            return

        else:
            obj = self.schematic(params)
            try:
                obj.validate()
                obj.created = datetime.datetime.utcnow()
                obj._id = ObjectId()
                result = yield self.collection.insert(obj.to_native())
                self.setResponseDictSuccess({"_id": str(result)})
            except ValidationError as e:
                self.setResponseDictErrors(e.messages)
            return


    @tornado.gen.coroutine
    def put(self):
        params = self.params.getParamsParse()
        obj = {key: value for key, value in params.items() if key is not '_id'}
        oid = self.getIdDict()
        obj_validate = self.schematic(params)
        try:
            obj_validate.validate()
            result = yield self.collection.update(oid, obj, upsert=False)
            self.setResponseDictSuccess({"_id": str(result)})
        except ValidationError as e:
            self.setResponseDictErrors(e.messages)
        return


    @tornado.gen.coroutine
    def delete(self):
        #params = self.params.getParams()
        oid = self.getIdDict()
        try:
            result = yield self.collection.remove(oid)
            self.setResponseDictSuccess({"_id": str(result)})
        except ValidationError as e:
            self.setResponseDictErrors(e)
        return

    @tornado.gen.coroutine
    def bulk(self):
        params = self.params.getParams()
        data = params['bulk']
        try:
            bulk = self.collection.initialize_ordered_bulk_op()
            data = params['bulk']
            if 'insert' in data:
                for obj in data['insert']:
                    obj['created'] = datetime.datetime.utcnow()
                    obj['_id'] = ObjectId()
                    bulk.insert(obj)
            result = yield bulk.execute()
        except BulkWriteError as e:
            self.setResponseDictErrors(e)

            '''
            bulk = self.collection.initialize_ordered_bulk_op()
            # Remove all documents from the previous example.
            bulk.find({}).remove()
            for i in range(10000):
                bulk.insert({'_id': i})
            #bulk.insert({'_id': 2})
            #bulk.insert({'_id': 3})
            bulk.find({'_id': 1}).update({'$set': {'foo': 'bar'}})
            bulk.find({'_id': 4}).upsert().update({'$inc': {'j': 1}})
            bulk.find({'j': 1}).replace_one({'j': 2})
            result = yield bulk.execute()
            '''

    @tornado.gen.coroutine
    def patch(self):
        params = self.params.getParamsParse()
        obj = {key: value for key, value in params.items() if key is not '_id'}
        oid = self.getIdDict()
        try:
            result = yield self.collection.update(oid,  {'$set':obj}, upsert=True)
            self.setResponseDictSuccess({"_id": params['_id']})
        except ValidationError as e:
            self.setResponseDictErrors(e)
        return


try:
    from services.resource import models_factory
except:
    #pass
    models_factory = {k: ResourceModel for k in ["GET", "POST", "PUT", "DELETE", "PATCH"]}

models = models_factory
