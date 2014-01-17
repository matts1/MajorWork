import os
import sys
import jinja2
import tornado.web
import tornado.ioloop

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(JINJA_ENVIRONMENT.get_template('viewcourses.html').render())

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def path(x):
    return (
        '/' + x + '/(.*)',
        tornado.web.StaticFileHandler,
        {'path': os.path.join(os.path.dirname(__file__), 'static', x)}
    )

handlers = [
    (r"/", MainHandler),
    path('js'),
    path('css'),
    path('images'),
    path('fonts'),
    path(r'favicon\.ico'), # matches favicon.ico/(.*), but meh
]

if __name__ == '__main__':
    settings = dict(
        debug='debug' in sys.argv[1:],
    )
    app = tornado.web.Application(handlers, **settings)
    app.listen(8080)
    print('--------------------')
    tornado.ioloop.IOLoop.instance().start()
