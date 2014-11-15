import motor
from schematics.models import Model
from schematics.types import (StringType, IntType, UUIDType, DateTimeType)
from schematics.contrib.mongo import ObjectIdType

class BaseModel(Model):
    _id = ObjectIdType()

class Song(BaseModel):
    name = StringType(max_length=40)
    created = DateTimeType()


objects = {"Song": Song}

"""
curl --data "name=pig" http://127.0.0.1:8888/animal
curl --data "name=horse" http://127.0.0.1:8888/animal
curl --data "name=cow" http://127.0.0.1:8888/animal
curl http://127.0.0.1:8888/animal
"""