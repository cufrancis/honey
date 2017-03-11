#!/usr/bin/env python
# codin=utf-8

import tornado.ioloop
import tornado.web
from tornado.options import define, options
from settings import settings
from route import urls
# from app import app

define("port", default="8888", help="listen port")


def make_app():
    return tornado.web.Application(urls, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
