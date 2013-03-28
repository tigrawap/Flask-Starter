from flask import session
from starter import app
from starter.core.utils.text import uuid_string

__author__ = 'tigra'

from starter.core.views import MainPage as baseMainPage

class MainPage(baseMainPage):
    """
    The good place to redefine functions for MainPage
    For example, let's make view class available inside context for every views
    """
    extend_with = "index.html" #default html for future extending

    def prepare(self,*k,**kk):
        super(MainPage,self).prepare(*k,**kk) #in most cases parent prepare should be called first
        self.context['view']=self

        #also will make sure, that csrf assigned to user
        if not session.has_key('csrf'):
            session['csrf']=uuid_string()