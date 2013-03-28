from datetime import timedelta
from flask import Flask
from flask.ext.babel import Babel
from werkzeug.datastructures import ImmutableDict
from flask.ext.login import LoginManager


__author__ = 'Anton Bykov, aka Tigra'

#setting up application
class MyFlask(Flask):
    jinja_options = ImmutableDict(
        extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_','jinja2.ext.loopcontrols','jinja2.ext.i18n','starter.core.jinja2.ext.PygmentsExtension']
        #not used in this demo, by in general need i18n for localisation
        #also, you can remove last one(code highlighting)
    )
    permanent_session_lifetime = timedelta(days=3650)

app = MyFlask(__name__,)

#loading default config
app.config.from_object('settings')
#loading environmental config, if exists
app.config.from_envvar(app.config.get('ENVIRONMENT_CONFIG_VAR'),silent=True)

#register some additional common context processors
from starter import context_processors

#init login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"

#init babel, translation manager
babel=Babel(app)



import views
import blueprints

