import webapp2
import glob
import datetime
import models
import Cookie

from glob import LOGIN_URL, HOME_URL

class BaseHandler(webapp2.RequestHandler):
    template = '/base.html'
    formid = None
    require_login = True
    def do_request(self, fn):
        self.user = self.get_user()
        if self.allowed():
            self.to_write = True
            self.err = {}
            res = fn()
            if res is None:
                res = {}
            if self.err.get(None, 1) is None:
                del self.err[None]
            if self.err:
                res['outerid'] = self.formid
                res['origvals'] = {field: getattr(self, field) for field in self.attrs}
                res['err'] = self.err
            self.output(res)

    def get(self):
        self.do_request(self.myget)

    def post(self):
        self.do_request(self.mypost)

    def myget(self):
        pass

    def mypost(self):
        pass

    def redirect(self, *args, **kwargs):
        self.to_write = False
        return webapp2.RequestHandler.redirect(self, *args, **kwargs)

    def get_data(self, *args):
        self.attrs = args
        for arg in args:
            setattr(self, arg, self.request.get(arg))

    def get_user(self):
        sessionID = self.get_cookie("session")
        if sessionID is not None:
            return models.users.User.all().filter("session =", sessionID).get()

    def allowed(self):
        if self.require_login is None:
            return True
        elif self.require_login == True:
            if self.user:
                return True
            else:
                self.redirect(LOGIN_URL)
                return False
        elif self.require_login == False:
            if self.user:
                self.redirect(HOME_URL)
                return False
            else:
                return True

    def adderr(self, data):
        if isinstance(data, tuple):
            self.err[data[0]] = data[1]
        elif isinstance(data, dict):
            self.err.update(data)
        elif isinstance(data, str):
            self.err[None] = data
        return data


    def output(self, data, template=None):
        if self.to_write:
            data["user"] = self.user
            template = self.template if template is None else template
            self.response.write(glob.JINJA_ENVIRONMENT.get_template(template).render(**data))

    def clear_cookie(self,name,path="/",domain=None):
        expires = datetime.datetime.utcnow() - datetime.timedelta(days=365)
        self.set_cookie(name,value="",path=path,expires=expires,
                                        domain=domain)
    
    def clear_all_cookies(self):
        """Deletes all the cookies the user sent with this request."""
        for name in self.cookies.iterkeys():
            self.clear_cookie(name)
    
    def get_cookie(self,name,default=None):
        """Gets the value of the cookie with the given name,else default."""
        if name in self.request.cookies:
            return self.request.cookies[name]
        return default
    
    def set_cookie(self,name,value,domain=None,expires=None,path="/",expires_days=None):
        new_cookie = Cookie.BaseCookie()
        new_cookie[name] = value
        if domain:
            new_cookie[name]["domain"] = domain
        if expires_days is not None and not expires:
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=expires_days)
        if expires:
            timestamp = calendar.timegm(expires.utctimetuple())
            new_cookie[name]["expires"] = email.utils.formatdate(timestamp,localtime=False,usegmt=True)
        if path:
            new_cookie[name]["path"] = path
        for morsel in new_cookie.values():
            self.response.headers.add_header('Set-Cookie',morsel.OutputString(None))
