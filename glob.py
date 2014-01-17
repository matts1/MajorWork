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
