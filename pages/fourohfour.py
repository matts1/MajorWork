from models.users import User
from pages.base import BaseHandler


class FourOhFourHandler(BaseHandler):
    template = '404.html'

    def myget(self):
        return {'page': self.request.get('page')}

class FourOhFourRedirecter(BaseHandler):
    def myget(self, url):
        self.error(404)
