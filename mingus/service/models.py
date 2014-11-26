#import motor
from schematics.models import Model
from schematics.types import (StringType, IntType, UUIDType, DateTimeType)
from schematics.contrib.mongo import ObjectIdType

 
class BaseModel(Model):
    _id = ObjectIdType()

class Song(BaseModel):
    slug = StringType(max_length=20, required=True)
    song = StringType(max_length=40)
    artist = StringType(max_length=40)
    rank = IntType()
    created = DateTimeType()

    """
    Is Simple
    ---------
    #app.py
    from rest_framework.server import main

    main()

    $ python app.py
    # In other terminal
    $ curl -X POST -v -H "Accept: application/json" -d 'bulk={"insert":[{"slug":"1","song":"My Funny Valentine"},{"slug":"2","song":"500 Miles High"},{"slug":"3","song":"All of Me"}]}' http://127.0.0.1:8888/song/
    $ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/v1/song
    $ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/v1/song/?slug=1
    $ curl -X POST -v -H "Accept: application/json" -d '{"slug":"88","artist":"8MikeArtistMike", "song":"8SongToSongSong", "rank":8001}' http://127.0.0.1:8888/v1/song/
    $ curl -X DELETE -v -H "Accept: application/json" http://127.0.0.1:8888/v1/song/?slug=1
    $ curl -X PUT -v -H "Accept: application/json" -d '{"slug":"33","song":"All of Me Update"}' http://127.0.0.1:8888/v1/song/
    $ curl -X PATCH -v -H "Accept: application/json" -d '{"song":"All of Me UpdatePatch"}' http://127.0.0.1:8888/v1/song/54746cc6d1e5ba151cd46269

    """ 