from models.users import User
from pages.base import BaseHandler


class ProfileHandler(BaseHandler):
    require_login = True
    template = 'user/profile.html'

    def myget(self, person_id):
        person = User.get_by_id(int(person_id))
        if person is None:
            self.error(404)
        return {'person': person}
