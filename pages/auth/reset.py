from globals import FORGOT_URL, LOGIN_URL
from models.users import User
from pages.base import BaseHandler


class ForgotPwdHandler(BaseHandler):
    formid = 'forgot'
    require_login = False
    template = 'index.html'
    success_msg = 'An email has been sent containing a link to reset your account'

    def myget(self):
        # chuck an invisible error on the form - should bring up the form
        self.err[None] = ''

    def mypost(self):
        self.get_data('email')
        self.adderr(User.setup_reset(self.attrs['email'], send_email=True))


class ResetPwdHandler(BaseHandler):
    success_msg = 'Your password has been reset. You can <a href="%s">login</a> now' % LOGIN_URL
    template = 'index.html'
    formid = 'doreset'
    require_login = None

    def myget(self):
        # chuck an invisible error on the form - should bring up the form
        self.err[None] = ''
        code = self.request.get('code')
        if not code:
            self.redirect(FORGOT_URL)
        return {'reset_code': self.request.get('code')}

    def mypost(self):
        code = self.request.get('code')
        self.adderr(User.do_reset(
            code,
            self.request.get('pwd'),
            self.request.get('confpwd')
        ))
        print self.err
        return {'reset_code': code}
