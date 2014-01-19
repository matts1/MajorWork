from pages.base import BaseHandler


class SettingsHandler(BaseHandler):
    require_login = True
    template = 'user/settings.html'

    def mypost(self):
        # find out which form they filled in
        self.formid = self.request.get('whichform')
        if self.formid == 'chgpwd':
            self.success_msg = 'Your password has been changed'
            self.adderr(self.user.chgpwd(
                self.request.get('oldpwd'),
                self.request.get('newpwd'),
                self.request.get('confpwd')
            ))
