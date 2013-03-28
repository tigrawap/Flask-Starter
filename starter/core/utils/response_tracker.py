__author__ = 'tigra'

from flask.globals import request,session


class RequestTracker():
    """
    User tracker based on writing previous location of user to session
    The referrer-blocker-proof
    The View class responsible for not tracking modal windows or to track them in some specific manner
    """

    def set_path(self,key,path):
        if not session.has_key('tracker'):
            session['tracker']=dict()

        session['tracker_'+key]=path

    def get_path(self,key):
        try:
            return session['tracker_'+key]
        except KeyError:
            return '/'

    def update_referrer(self):
        if request.url!=self.get_path(key='current'):
            self.set_path(key='prev',path=self.referrer)
            self.set_path(key='referrer',path=self.current)
            self.set_path(key='current',path=request.url)

        #self.set_path(key='prev',path=self.get_path('referrer'))
        #self.set_path(key='referrer',path=self.get_path('current'))
        #self.set_path(key='current',path=request.path)

    def rollback_referrer(self):
        self.set_path(key="current",path=self.referrer)
        self.set_path(key='referrer',path=self.prev_referrer)

    @property
    def current(self):
        try:
            return session['tracker_current']
        except KeyError:
            return '/'

    @property
    def prev_referrer(self):
        try:
            return session['tracker_prev']
        except KeyError:
            return '/'

    @property
    def referrer(self):
        #if has next value count it as primary, otherwise do inner magic
        if request.args.has_key('next'):
            return request.args['next']

        #try to return value from session, if not found fall back to request referrer, if still not found redirect to index
        try:
            return session['tracker_referrer']
        except KeyError:
            if request.referrer:
                redirect_to=request.referrer
            else:
                redirect_to="/"
            return redirect_to