import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# URLS
INDEX_URL = '/'
LOGIN_URL = '/login'
REGISTER_URL = '/register'
LOGOUT_URL = '/logout'
HOME_URL = '/home'
PROFILE_URL = '/profile'
SETTINGS_URL = '/settings'
FORGOT_URL = '/forgot'
RESET_PWD_URL = '/doreset'
CREATE_COURSE_URL = '/createcourse'

TEACHER = 2

# put all our *_URL variables into the template
for variable, content in locals().items():
    if variable.endswith("_URL"):
        JINJA_ENVIRONMENT.globals[variable[:-4]] = content

SESSION_NUM_DAYS = 7

WEBSITE_URL = 'chsorganiser.appspot.com'
WEBSITE_EMAIL = 'chsorganiser.appspotmail.com'
