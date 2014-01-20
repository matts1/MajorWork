import calendar
import email
import webapp2
import globals
import datetime
import Cookie

from globals import LOGIN_URL, HOME_URL
from models.users import User


class BaseHandler(webapp2.RequestHandler):
    template = '/base.html'
    formid = None
    require_login = True
    success_msg = None

    def do_request(self, fn, *args, **kwargs):
        """
        called on any request, both GET and POST, with a function to execute.
        The function changes based on the method
        """
        self.user = self.get_user()
        if self.allowed():
            self.to_write = True
            self.err = {}
            self.attrs = {}
            res = fn(*args, **kwargs)
            if res is None:
                res = {}
            if self.err.get(None, 1) is None:
                del self.err[None]
            res['formid'] = self.formid
            self.output(res)

    def get(self, *args, **kwargs):
        self.using_post = False
        self.do_request(self.myget, *args, **kwargs)

    def post(self, *args, **kwargs):
        self.using_post = True
        self.do_request(self.mypost, *args, **kwargs)

    def myget(self):
        pass

    def mypost(self):
        pass

    def redirect(self, url, *args, **kwargs):
        """
        Redirects the user to another page. Also stops the current page from
        outputting HTML to the user, so we only get one page
        """
        self.to_write = False
        if self.using_post:
            # we issued a redirect, but we're using post, not get.
            # because we're using ajax I need to issue a different response
            self.response.write('REDIRECT:' + url)
        else:
            return webapp2.RequestHandler.redirect(self, url, *args, **kwargs)

    def get_data(self, *args):
        """
        Gets the form data specified, and gets ready to fill it in to the
        next form if this form doesn't work. Don't use it for passwords
        """
        for arg in args:
            self.attrs[arg] = self.request.get(arg)

    def get_user(self):
        """
        Gets the current user that is logged on based on session data
        """
        session_id = self.get_cookie('session')
        if session_id is not None:
            return User.all().filter('session =', session_id) \
                .filter('session_expiry >', datetime.datetime.now()).get()

    def error(self, code):
        if code == 404:
            self.redirect('/404?page=' + self.request.url)
        else:
            raise NotImplementedError

    def allowed(self):
        """
        Checks whether the user is allowed on the current page. If they aren't,
        redirect them to the appropriate page
        """
        if self.require_login is None:
            return True
        elif self.require_login:
            if self.user:
                return True
            else:
                self.redirect(LOGIN_URL)
                return False
        elif not self.require_login:
            if self.user:
                self.redirect(HOME_URL)
                return False
            else:
                return True

    def adderr(self, data):
        """
        Use for database functions which return their error message.
        Adds the error message to a list of errors, which will automatically populate
        """
        if isinstance(data, tuple):
            self.err[data[0]] = data[1]
        elif isinstance(data, dict):
            self.err.update(data)
        elif isinstance(data, str) or isinstance(data, unicode):
            self.err[None] = data
        return data

    def output(self, data, template=None):
        """
        Outputs to a specified template the data given. Called from do_request normally
        """
        if self.to_write:
            if self.using_post:
                self.response.write('FORMDATA:')
                if self.err:
                    for key, val in self.err.items():
                        self.response.write('<div class="alert alert-danger" data-for="%s">%s</div>' %
                                            ('' if key is None else key, val))
                else:
                    self.response.write('<div class="alert alert-success" data-for="">%s</div>' %
                                        self.success_msg)
            else:
                data['user'] = self.user
                template = self.template if template is None else template
                self.response.write(globals.JINJA_ENVIRONMENT.get_template(template).render(**data))

    def clear_cookie(self, name, path='/', domain=None):
        expires = datetime.datetime.utcnow() - datetime.timedelta(days=365)
        self.set_cookie(name, value='', path=path, expires=expires, domain=domain)
    
    def get_cookie(self, name, default=None):
        """
        Gets the value of the cookie with the given name,else default.
        """
        if name in self.request.cookies:
            return self.request.cookies[name]
        return default
    
    def set_cookie(self, name, value, domain=None, expires=None, path='/', expires_days=None):
        new_cookie = Cookie.BaseCookie()
        new_cookie[name] = value
        if domain:
            new_cookie[name]['domain'] = domain
        if expires_days is not None and not expires:
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=expires_days)
        if expires:
            timestamp = calendar.timegm(expires.utctimetuple())
            new_cookie[name]['expires'] = email.utils.formatdate(timestamp, localtime=False, usegmt=True)
        if path:
            new_cookie[name]['path'] = path
        for morsel in new_cookie.values():
            self.response.headers.add_header('Set-Cookie', morsel.OutputString(None))
