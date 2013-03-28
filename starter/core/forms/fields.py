from flask import session
from wtforms import HiddenField
from validators import CSRFCheck

__author__ = 'tigra'

class CSRFField(HiddenField):
    """
    Used for csrf protection, must be included in each form
    """
    def __init__(self, label=None, validators=None, filters=tuple(),
                 description=u'', id=None, default=None, widget=None,
                 _form=None, _name=None, _prefix='', _translations=None):
        if validators is None:
            validators=[CSRFCheck()]
        super(CSRFField,self).__init__(label,validators,filters,description,id,default,widget,_form,_name,_prefix,_translations)

    def _value(self):
        return self.data is not None and unicode(self.data) or session.get('csrf')