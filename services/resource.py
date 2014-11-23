from mingus.resources import ResourceModel

#ToDo Inplementations ResourceModelCustom for ResourceModel
class MyCustomResourceModel(ResourceModel):
    def setGet(self):
        # My Custom Resource get all objects with :param status = True
        
        params = self.params.getParams()
        pagination = self.pagination()
        uri = uri
        slace = self.getSlace(**pagination)
        start, end = (slace['start'], slace['end'])
        oid = self.getIdDict()
        if oid:
            try:
                result = yield self.collection.find_one(oid)
                result['_id'] = str(result['_id'])
                self.setResponseDictSuccess(result)
            except Exception as e:
                self.setResponseDictErrors("Not Found!")
        else:
            params['status'] = True
            cursor = self.collection.find(params).sort([('_id', -1)])[1:1]#[start:end]
            objects = []
            while (yield cursor.fetch_next):
                objects.append(cursor.next_object())
            results = {'data':[document for document in objects]}
            self.setResponseDictSuccess(results)
        return



#models_factory = {k: MyCustomResourceModel for k in ["GET", "POST", "PUT", "DELETE", "PATCH"]}

