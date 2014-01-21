from pages import BaseHandler


class FourOhFourHandler(BaseHandler):
    require_login = None
    template = 'other/404.html'

    def myget(self):
        return {'page': self.request.get('page')}

class FourOhFourRedirecter(BaseHandler):
    require_login = None
    def myget(self, url):
        self.error(404)
