from wtforms import TextField, SubmitField
from wtforms.validators import  DataRequired
from starter.core.forms import SafeForm
from starter.core.i18n import __, _

__author__ = 'tigra'

class UserForm(SafeForm):
    name=TextField(__("Name"),validators=[DataRequired()])
    submit=SubmitField(_("Login"))