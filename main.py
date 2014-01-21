import webapp2
from globals import *

from pages.auth import LoginHandler
from pages.auth import LogoutHandler
from pages.auth import ProfileHandler
from pages.auth import RegisterHandler
from pages.auth import ResetPwdHandler, ForgotPwdHandler
from pages.auth import SettingsHandler
from pages.courses import ViewCourseHandler
from pages.courses import CreateCourseHandler
from pages import FourOhFourHandler, FourOhFourRedirecter
from pages import IndexHandler

handlers = [
    (INDEX_URL, IndexHandler),
    (LOGIN_URL, LoginHandler),
    (REGISTER_URL, RegisterHandler),
    (LOGOUT_URL, LogoutHandler),
    (HOME_URL, ViewCourseHandler),
    (SETTINGS_URL, SettingsHandler),
    (FORGOT_URL, ForgotPwdHandler),
    (RESET_PWD_URL, ResetPwdHandler),
    (PROFILE_URL + r'/(\d+)', ProfileHandler),
    (CREATE_COURSE_URL, CreateCourseHandler),
    ('/404', FourOhFourHandler),
    ('/(.*)', FourOhFourRedirecter),
]

print('--------------------')
app = webapp2.WSGIApplication(
    handlers,
    debug=True,
)
