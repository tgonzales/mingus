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
    $ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/song
    $ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/song/?slug=1

    Set Database is Simple
    ----------------------
    $ python app.py --database=MyProjectDB


    Set Port HTTP is Simple
    ----------------------
    $ python app.py --port=5555
    # or port and database
    $ python app.py --port=5555 --database=MyProjectDB


    Rest HTTP Commands with curl
    ----------------------------

    Insert one single object
    $ curl -X POST -v -H "Accept: application/json" -d 'data={"slug":"4","song":"Donna Lee"}' http://127.0.0.1:8888/song/


	curl -X POST -v -H "Accept: application/json" -d "id=8008&artist=8MikeArtistMike&song=8SongToSongSong&rank=8001" http://127.0.0.1:8888/song/
	curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/song/8888d58dd1e5ba35fc062788/?id=2002
	curl -X PUT -v -H "Accept: application/json" -d "artist=MikeArtistMike&song=SongToSongSong&rank=1021" http://127.0.0.1:8888/song/?id=2002
	curl -X DELETE -v -H "Accept: application/json" http://127.0.0.1:8888/song/8888d58dd1e5ba35fc062788/?id=2002

    json
    curl -X POST -v -H "Accept: application/json" -d 'data={"id":8008,"artist":"8MikeArtistMike", "song":"8SongToSongSong", "rank":8001}' http://127.0.0.1:8888/song/

    bulk
    curl -X POST -v -H "Accept: application/json" -d 'bulk={"insert":[{"_id":1,"song":"My Funny Valentine"},{"_id":2,"song":"500 Miles High"},{"_id":3,"song":"All of Me"}]}' http://127.0.0.1:8888/song/

	"""
