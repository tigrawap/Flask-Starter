from flask import session
from wtforms.validators import StopValidation

__author__ = 'tigra'

class CSRFCheck(object):
    field_flags = ('required', )

    def __init__(self, message=None):
       self.message = message

    def __call__(self, form, field):
        if field.data!= session.get('csrf'):
           if self.message is None:
               self.message = field.gettext(u'CSRF Token invalid')
               field.errors[:] = []
               raise StopValidation(self.message)