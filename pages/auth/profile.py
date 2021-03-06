from models import User
from pages import BaseHandler


class ProfileHandler(BaseHandler):
    template = 'user/profile.html'

    def myget(self, person_id):
        person = User.get_by_id(int(person_id))
        if person is None:
            self.error(404)
        return {'person': person}

    def mypost(self, person_id):
        person = User.get_by_id(int(person_id))
        if self.user.teacher and person is not None:
            person.make_teacher()

