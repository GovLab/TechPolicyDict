
#!/usr/bin/env python

import os.path
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.escape import json_encode 
import logging

#Mongo
from mongoengine import *
import models
import bson
from bson import json_util
import csv
import json
import re
import bcrypt
from datetime import datetime
from handlers.handlers import *

# import and define tornado-y things
from tornado.options import define
define("port", default=5000, help="run on the given port", type=int)

#Connect to mongo
connect('db', host=os.environ.get('MONGOLAB_URI'))


# application settings and handle mapping info
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/about/?", AboutHandler),
            (r"/login/?", LoginHandler),
            (r"/register/?", RegisterHandler),
            (r"/submit/?", SubmitHandler),
            (r"/logout/?", LogoutHandler),
            (r"/word/?", WordHandler),
            (r"/search/?", SearchHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={
                "datetime": datetime},
            debug=True,
            cookie_secret=os.environ.get('COOKIE_SECRET'),
            xsrf_cookies=True,
            login_url="/login"
        )
        tornado.web.Application.__init__(self, handlers, **settings)



# RAMMING SPEEEEEEED!
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
