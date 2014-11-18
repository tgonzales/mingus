#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import motor

from rest_framework.models import models, ModelParams
from rest_framework.handler import rest_routes
from rest_framework.factories import ModelFactory
#from rest_framework.register import objects
from rest_framework.register import objects

define("port", default=8888, help="run on the given port", type=int)

db = motor.MotorClient().test
resource = ModelFactory(db, objects, models, ModelParams)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = tornado.web.Application(rest_routes(objects, resource), debug=True)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

