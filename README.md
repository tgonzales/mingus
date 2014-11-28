Mingus
======

Mingus is Rest Framework powerful and flexible toolkit that makes it easy to build Web APIs.

requirements
------------
```sh
motor - https://github.com/mongodb/motor
tornado - https://github.com/tornadoweb/tornado 
schematics - https://github.com/schematics/
```

Is Simple
---------
```sh
   #app.py
    from mingus.server import main
    main()
```

```sh
$ mongod
# other terminal
$ python app.py
# other terminal
$ curl -X POST -v -H "Accept: application/json" -d 'bulk={"insert":[{"slug":"1","rank":4,"song":"My Funny Valentine"},{"slug":"2","rank":4,"song":"500 Miles High"},{"slug":"3","rank":5,"song":"All of Me"}]}' http://127.0.0.1:8888/v1/song/
$ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/song
$ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/song/?slug=1
```

GetStarter
----------

Install
-------
```sh
   $ pip install mingus-rest-framework
   # or
   $ mkdir myproject
   $ cd myproject
   $ touch app.py
   $ git clone https://github.com/tgonzales/mingus (recommended)
   $ git checkout 0.2-dev
   $ pip install -r mingus/requirements.txt
   # config your app.py
   $ mongod
   $ python app.py   

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

Set HTTP Port is Simple
-----------------------
```sh
$ python app.py --port=5555
# or port and database
$ python app.py --port=5555 --database=MyProjectDB
```

Set API Version is Simple
-----------------------
```sh
$ python app.py --port=5555 --database=MyProjectDB --version=v1.1
```

Create Rest Versions Instances is Simple
----------------------------------------
```sh
$ python app.py --port=5551 --database=MyProjectDB --version=v2
$ python app.py --port=5550 --database=MyProjectDB --version=v1
```

Rest HTTP Commands with curl
----------------------------
```sh
    $ curl -X POST -v -H "Accept: application/json" -d 'bulk={"insert":[{"slug":"1","song":"My Funny Valentine"},{"slug":"2","song":"500 Miles High"},{"slug":"3","song":"All of Me"}]}' http://127.0.0.1:8888/v1/song/
    $ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/v1/song
    $ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/v1/song/?slug=1
    $ curl -X POST -v -H "Accept: application/json" -d '{"slug":"88","artist":"8MikeArtistMike", "song":"8SongToSongSong", "rank":8001}' http://127.0.0.1:8888/v1/song/
    $ curl -X DELETE -v -H "Accept: application/json" http://127.0.0.1:8888/v1/song/?slug=1
    $ curl -X PUT -v -H "Accept: application/json" -d '{"slug":"33","song":"All of Me Update"}' http://127.0.0.1:8888/v1/song/
    $ curl -X PATCH -v -H "Accept: application/json" -d '{"song":"All of Me UpdatePatch"}' http://127.0.0.1:8888/v1/song/54746cc6d1e5ba151cd46269
```
   
Run Tests
---------
```sh
	$ python -m unittest tests/test_bulk.py -v
	$ python -m unittest tests/test_status_code.py -v
```

Set You Models
--------------
```sh
	$ mkdir services
	$ touch __init__.py
	$ touch models.py
	# models.py
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
	 

	$ python app.py
```