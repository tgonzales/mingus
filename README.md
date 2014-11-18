tornado-rest-framework
======================

Tornado Rest Framework is a powerful and flexible toolkit that makes it easy to build Web APIs.

requirements
------------
motor
tornado
schematics

start rest services:
```sh
$ mongod
$ git clone https://github.com/tgonzales/tornado-rest-framework.git
$ cd tornado-rest-framework
$ pip install requirements.txt
$ python server.py
```
Rest with example model:
```sh
$ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/song/?id=2002
$ curl -X POST -v -H "Accept: application/json" -d "id=8008&artist=8MikeArtistMike&song=8SongToSongSong&rank=8001" http://127.0.0.1:8888/song/
$ curl -X GET -v -H "Accept: application/json" http://127.0.0.1:8888/song/8888d58dd1e5ba35fc062788/?id=2002
$ curl -X PUT -v -H "Accept: application/json" -d "artist=MikeArtistMike&song=SongToSongSong&rank=1021" http://127.0.0.1:8888/song/?id=2002
$ curl -X DELETE -v -H "Accept: application/json" http://127.0.0.1:8888/song/8888d58dd1e5ba35fc062788/?id=2002
```
   
Create Your Model Resource:
```sh
   $ vim models/models.py
   class Car(BaseModel):
       name = StringType(max_length=40)
```
Restart Service
