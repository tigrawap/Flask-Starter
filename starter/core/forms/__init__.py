from fields import CSRFField
from starter.core.i18n import _

__author__ = 'tigra'

#from flaskext.wtf import Form as BaseForm
from wtforms.form import Form as BaseForm

class Form(BaseForm):
    """
    This class extends default wftforms forms by adding translation,
     sorting in right order and providing ability to use tna_data dictionary to pass custom data to field
    """
    #used to pass data inside form rendered (by acessing form itself)
    tna_data={}

    def __init__(self,*k,**kk):
        super(Form,self).__init__(*k,**kk)
        self.tna_data={}

        order=[]
        for field in self._unbound_fields:
            order.append(field[0])
        ordered_fields=sorted(self._fields,cmp=lambda x,y:cmp(order.index(x),order.index(y)))
        self._ordered_fields=[]
        for field in ordered_fields:
            o_field=self._fields[field]
            #FORCE TRANSLATIONS, definition of form uses __ instead of _, becouse class created and stored in memory
            #and translation made upon displaying
            if o_field.description:
                o_field.description=_(o_field.description)
            if o_field.label.text:
                o_field.label.text=_(o_field.label.text)
            self._ordered_fields.append((field,o_field))

    def translate_select(self,select_field):
        pass

class SafeForm(Form):
    """
    Just like Form class, but also forces CSRFField
    """
    csrf=CSRFField()