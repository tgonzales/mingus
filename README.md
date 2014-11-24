Mingus
======

Mingus is Rest Framework powerful and flexible toolkit that makes it easy to build Web APIs.

requirements
------------
```sh
motor
tornado
schematics
```

Is Simple
---------
```sh
   #app.py
    from mingus.server import main
    main()
```

Install
-------
```sh
   $ pip install mingus-rest-framework
```

start rest services:
```sh
$ mongod
# other terminal
$ python app.py
# other terminal
$ curl -X POST -v -H "Accept: application/json" -d 'bulk={"insert":[{"slug":"1","song":"My Funny Valentine"},{"slug":"2","song":"500 Miles High"},{"slug":"3","song":"All of Me"}]}' http://127.0.0.1:8888/song/
$ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/song
$ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/song/?slug=1
```

Set Database is Simple
----------------------
```sh
$ python app.py --database=MyProjectDB
```

Set Port HTTP is Simple
-----------------------
```sh
$ python app.py --port=5555
# or port and database
$ python app.py --port=5555 --database=MyProjectDB
```

Rest HTTP Commands with curl
----------------------------
```sh
#Insert one single object
$ curl -X POST -v -H "Accept: application/json" -d "id=2002&artist=MikeArtistMike&song=SongToSongSong&rank=8001" http://127.0.0.1:8888/song/
$ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/song/8888d58dd1e5ba35fc062788/?id=2002
$ curl -X PUT -v -H "Accept: application/json" -d "artist=MikeArtistMike&song=SongToSongSong&rank=1021" http://127.0.0.1:8888/song/?id=2002
$ curl -X DELETE -v -H "Accept: application/json" http://127.0.0.1:8888/song/8888d58dd1e5ba35fc062788/?id=2002

#bulk
$ curl -X POST -v -H "Accept: application/json" -d 'bulk={"insert":[{"_id":1,"song":"My Funny Valentine"},{"_id":2,"song":"500 Miles High"},{"_id":3,"song":"All of Me"}]}' http://127.0.0.1:8888/song/
```
   
