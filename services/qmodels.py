
from schematics.types import StringType, BooleanType, DateType
from schematics.types.compound import ListType, ModelType
from mingus.service.models import BaseModel

class Todolist(BaseModel):
    title = StringType(max_length=60, required=True)
    tag = StringType(max_length=40)
    checked = BooleanType(default=False)
    created = DateType()

class User(BaseModel):
    name = StringType(max_length=40, required=True)
    todolist = ListType(ModelType(Todolist))
