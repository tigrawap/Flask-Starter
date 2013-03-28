from flask import Blueprint
from starter import app
from starter.main.views import main
from starter.user.views import user
from starter.core import core

__author__ = 'tigra'

app.register_blueprint(core) #registered just to get /templates folder from there
app.register_blueprint(main,url_prefix="/demos") #by the way, templates can be stored inside separate blueprints or inside one common /templates folder. On your choice
app.register_blueprint(user,url_prefix="/user")
app.add_url_rule("/","main.index") #attach /demos/ to /
