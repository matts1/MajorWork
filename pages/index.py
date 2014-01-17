from pages.base import BaseHandler

class IndexHandler(BaseHandler):
    require_login = None
    template = 'index.html'
