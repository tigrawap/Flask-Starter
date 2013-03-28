from flask import Blueprint, request, render_template, Response, redirect, session
from flask.ext.login import login_user, logout_user
from starter.core.views import action
from starter.user.forms import UserForm
from starter.user.models import User
from starter.views import MainPage

__author__ = 'tigra'


user = Blueprint('user',__name__)

class Login(MainPage):
    track = False #no need to track login page
    template = "user/login.html"
    page_header="Login"

    def get(self,*k,**kk):
        self.context['form']=UserForm()

        #remember where from request came
        if not session.has_key('login_url'):
            session['login_url']=self.tracker.current

        return render_template(self.template,**self.context)



    def post(self,*k,**kk):
        form=UserForm(request.form)
        if not form.validate():
            self.context['form']=form
            return render_template(self.template,**self.context)

        user=User(form.name.data) #create virtual user
        login_user(user,remember=True) #login virtual user

        if session.has_key('login_url'):
            return redirect(session.get('login_url'))
        else:
            return redirect(self.tracker.current)

class Logout(MainPage):
    track = False

    def get(self,*k,**kk):
        return redirect(self.tracker.current)

    @action
    def post(self,*k,**kk):
        logout_user()
        return redirect(self.tracker.current)


user.add_url_rule('/login',view_func=Login.as_view('login'))
user.add_url_rule('/logout',view_func=Logout.as_view('logout'))