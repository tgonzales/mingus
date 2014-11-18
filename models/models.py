#import motor
from schematics.models import Model
from schematics.types import (StringType, IntType, UUIDType, DateTimeType)
from schematics.contrib.mongo import ObjectIdType

 
class BaseModel(Model):
    _id = ObjectIdType()

class Song(BaseModel):
    id = IntType() # for test
    song = StringType(max_length=40)
    artist = StringType(max_length=40)
    rank = IntType()
    created = DateTimeType()

    """
	curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/song/?id=2002
	curl -X POST -v -H "Accept: application/json" -d "id=8008&artist=8MikeArtistMike&song=8SongToSongSong&rank=8001" http://127.0.0.1:8888/song/
	curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/song/8888d58dd1e5ba35fc062788/?id=2002
	curl -X PUT -v -H "Accept: application/json" -d "artist=MikeArtistMike&song=SongToSongSong&rank=1021" http://127.0.0.1:8888/song/?id=2002
	curl -X DELETE -v -H "Accept: application/json" http://127.0.0.1:8888/song/8888d58dd1e5ba35fc062788/?id=2002
	"""

class Test(BaseModel):
    id = IntType() # for test
    song = StringType(max_length=40)
    artist = StringType(max_length=40)
    rank = IntType()
    created = DateTimeType()
