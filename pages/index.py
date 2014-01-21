from pages import BaseHandler


class IndexHandler(BaseHandler):
    require_login = None
    template = 'index.html'

    # if I actually want to put anything in here, need to think about the fact that
    # register and login use this template, so they're gonna need the variables too
