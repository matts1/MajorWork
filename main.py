import os
import sys
import webapp2
from glob import *

from pages.auth.login import LoginHandler
from pages.auth.logout import LogoutHandler
from pages.auth.register import RegisterHandler
from pages.courses.viewcourses import CourseHandler
from pages.index import IndexHandler

handlers = [
    (INDEX_URL, IndexHandler),
    (LOGIN_URL, LoginHandler),
    (REGISTER_URL, RegisterHandler),
    (LOGOUT_URL, LogoutHandler),
    (HOME_URL, CourseHandler),
]

print('--------------------')
app = webapp2.WSGIApplication(
    handlers,
    debug=True,
)

