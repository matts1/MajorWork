from google.appengine.ext import db
import webapp2
from globals import *
from oldmodels import User, Course, Search

from pages.auth import LoginHandler, LogoutHandler, ProfileHandler, RegisterHandler, SettingsHandler
from pages.auth import ResetPwdHandler, ForgotPwdHandler
from pages.courses import ListCoursesHandler, CreateCourseHandler, ViewCourseHandler
from pages.other import FourOhFourHandler, FourOhFourRedirecter, IndexHandler, SearchHandler
import time

handlers = [
    (INDEX_URL, IndexHandler),
    (LOGIN_URL, LoginHandler),
    (REGISTER_URL, RegisterHandler),
    (LOGOUT_URL, LogoutHandler),
    (HOME_URL, None),
    (SETTINGS_URL, SettingsHandler),
    (FORGOT_URL, ForgotPwdHandler),
    (RESET_PWD_URL, ResetPwdHandler),
    (PROFILE_URL + r'(\d+)', ProfileHandler),
    (LIST_COURSES_URL, ListCoursesHandler),
    (OPEN_COURSE_URL + r'(\d+)', ViewCourseHandler),
    (CREATE_COURSE_URL, CreateCourseHandler),
    (SEARCH_URL, SearchHandler),
    ('/404', FourOhFourHandler),
    ('/(.*)', FourOhFourRedirecter),
]

print('--------------------')
app = webapp2.WSGIApplication(
    handlers,
    debug=True,
)

# ADD INITIAL DATA - CLEAR DATABASE AFTER MAKING ANY CHANGES
if User.all().get() is None:
    db.delete(Course.all())  # chucks an error if we don't delete all datastore stuff
    db.delete(Search.all())
    time.sleep(0.1)
    assert User.register(None, 'mattstark75@gmail.com', 'a', 'a', 'matt', 'stark') is None
    me = User.all().filter('email =', 'mattstark75@gmail.com').get()
    assert me is not None and me.make_teacher() is None
    assert User.register(None, 'teacher@gmail.com', 'a', 'a', 'teacher', 't') is None
    teacher = User.all().filter('email =', 'teacher@gmail.com').get()
    assert teacher is not None and teacher.make_teacher() is None
    assert User.register(None, 'student@gmail.com', 'a', 'a', 'student', 's') is None

    assert Course.create(teacher, 'public course', '') is None
    assert Course.create(teacher, 'private course', 'on') is None
    assert Course.create(me, 'my public course', '') is None
    assert Course.create(me, 'my private course', 'on') is None
    print 'Added initial data'
