# tornadoapp.py
import tornado.ioloop
import tornado.web
from settings import settings


class Application(tornado.web.Application):
    def route(self, pattern):
        def _(handler):
            handler_pattern = [(pattern, handler)]
            self.add_handlers(".*$", handler_pattern)
            return handler
        return _

app = Application(handlers=None, default_host=None, transforms=None,**settings)
