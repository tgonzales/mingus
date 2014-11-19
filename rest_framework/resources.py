from schematics.types.base import GeoPointType
from schematics.types.compound import ListType, DictType, ModelType

import tornado.gen
import tornado.web
#import motor
from schematics.exceptions import ValidationError
#from schematics.contrib.mongo import ObjectIdType
from bson.objectid import ObjectId
import json
import datetime

from rest_framework.serializers import JSONSerializer

class ModelParams(object):
    def __init__(self, fields, args, kwargs, arguments):
        self.fields = fields
        self.args = args
        self.kwargs = kwargs
        self.arguments = arguments

    def getParams(self):
        """
        Check the schematic object to see if arguments from Tornado can be lists or dictionaries
        """
        types = [DictType, GeoPointType, ListType, ModelType]
        fieldkeys = self.fields.keys()
        for argument, value in self.arguments.items():
            if type(value) is list and argument in fieldkeys and self.fields[argument] not in types:
                self.arguments[argument] = self.arguments[argument][0]
        if len(self.args):
            self.arguments['_id'] = self.args[0]

        #params = self.params.getParams()
        for k,v in self.arguments.items():
            if type(v) == bytes:
                self.arguments[k]= v.decode("utf-8") 
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
            previous = 1 
        pagination['previous'] = previous 
        return pagination


    def setResponseDictSuccess(self, result):
        self.responseDict = {"status": "Success", "result":result}

    def setResponseDictErrors(self, errors):
        self.responseDict = {"status": "Errors",  "errors": errors}

    def getIdDict(self):
        params = self.params.getParams()
        if 'id' in params:
            oid = {'id':int(params['id'])}
        elif '_id' in params:
            oid = {'_id':params['_id']}
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


class ResourceModel(Model):

    @tornado.gen.coroutine
    def getList(self, uri):
        """
        Either send get a single result if there is an _id parameter or send a list of results
        """
        params = self.params.getParams()
        pagination = self.pagination()
        uri = uri
        slace = self.getSlace(**pagination)
        start, end = (slace['start'], slace['end'])
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(slace)
        oid = self.getIdDict()
        if oid:
            try:
                result = yield self.collection.find_one(oid)
                result['_id'] = str(result['_id'])
                self.setResponseDictSuccess(result)
            except Exception as e:
                self.setResponseDictErrors("Not Found!")
        else:
            cursor = self.collection.find().sort([('_id', -1)])[start:end]
            objects = []
            while (yield cursor.fetch_next):
                objects.append(cursor.next_object())
            results = {'data':[document for document in objects]}
            self.setResponseDictSuccess(results)
        return


    @tornado.gen.coroutine
    def setPostResponseDict(self):
        params = self.params.getParams()
        '''
        for k,v in params.items():
            if type(v) == bytes:
                params[k]= v.decode("utf-8")
        ''' 
        obj = self.schematic(params)
        try:
            obj.created = datetime.datetime.utcnow()
            obj._id = ObjectId()
            obj.validate()
            result = yield self.collection.insert(obj.to_primitive())
            self.setResponseDictSuccess({"_id": str(result)})
        except ValidationError as e:
            self.setResponseDictErrors(e)
        return

    @tornado.gen.coroutine
    def setPutResponseDict(self):
        params = self.params.getParams()
        '''
        for k,v in params.items():
            if type(v) == bytes:
                params[k]= v.decode("utf-8")
        '''
        obj = {key: value for key, value in params.items() if key is not '_id'}

        if 'id' in params:
            oid = {'id':int(params['id'])}
        else:
            oid = {'_id':params['_id']}
        try:
            result = yield self.collection.update(oid,  {"$set": obj}, upsert=True)
            self.setResponseDictSuccess({"_id": params['_id']})
        except ValidationError as e:
            self.setResponseDictErrors(e)
        return


    @tornado.gen.coroutine
    def setDeleteResponseDict(self):
        params = self.params.getParams()
        '''
        for k,v in params.items():
            if type(v) == bytes:
                params[k]= v.decode("utf-8") 
        '''
        if params['id']:
            oid = {'id':int(params['id'])}
        else:
            oid = {'_id':params['_id']}
        try:
            result = yield self.collection.remove(oid)
            self.setResponseDictSuccess({"_id": str(result)})
        except ValidationError as e:
            self.setResponseDictErrors(e)
        return


models = {k: ResourceModel for k in ["GET", "POST", "PUT", "DELETE"]}
#models = {"GET": ResourceModel, "POST": ResourceModel, "PUT": ResourceModel, "DELETE": ResourceModel}

