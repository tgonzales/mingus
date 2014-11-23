#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import motor

from mingus.resources import models, ModelParams
from mingus.handler import rest_routes
from mingus.factories import ModelFactory
from mingus.register import objects

define("port", default=8888, help="run on the given port", type=int)
define("database", default='test', help="run on the database")

#db = motor.MotorClient().test
#resource = ModelFactory(db, objects, models, ModelParams)

def main():
    tornado.options.parse_command_line()
    db = motor.MotorClient()[options.database]
    print('*******')
    print('MongoDatabase: {0}'.format(options.database))
    print('ServerHTTPPort: {0}'.format(options.port))
    resource = ModelFactory(db, objects, models, ModelParams)
    application = tornado.web.Application(rest_routes(objects, resource), debug=True)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()	

if __name__ == "__main__":
	main()


