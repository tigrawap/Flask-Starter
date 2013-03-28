import copy
from flask.globals import current_app, request,g, session
from flask.helpers import url_for
from flask.templating import render_template
from flask.views import MethodView
from flask.ext.login import current_user
from werkzeug.utils import redirect, html
from werkzeug.wrappers import BaseResponse, Response
import settings
from starter import app
from starter.core.utils.response import response_error, response_redirect, response_ok
from starter.core.utils.response_tracker import RequestTracker

__author__ = 'Anton Bykov, aka Tigra'


class RedirectException(Exception):
    """
    If this exception is raise user redirected to specified location
    """
    location=None

    def __init__(self,location=None,*k, **kk):
        self.location=location
        super(RedirectException,self).__init__(*k,**kk)

class ResponseException(Exception):
    """
    If this exception in raised(usually inside prepare())
    the response passed as Call argument returned as Response
    instead of regular routine
    """
    response=None
    def __init__(self,response=None, *args, **kwargs):
        self.response=response
        super(ResponseException,self).__init__(*args,**kwargs)

class ResponseErrorException(Exception):
    """
    If this error raised some error should be displayed to user
    """
    error =None
    def __init__(self,error=None, *args, **kwargs):
            self.error=error
            super(ResponseErrorException,self).__init__(*args,**kwargs)

class PermissionDeniedException(Exception):
    """
    If this exception raised user error should be displayed or some response returned
    """
    error = None
    return_response = None
    def __init__(self,error=None,return_response=None,*k,**kk):
        self.error=error
        self.return_response=return_response
        super(PermissionDeniedException,self).__init__(*k,**kk)


class MainPage(MethodView):
    """
    Main View class, responsible for permissions, context, navigation, meta tags, tracking of user activity
    User class should be inherited from this

    """
    login_required=False
    admin_required=False
    item_user=None #if current view can be viewed only by specific user it should be assigned to this parameter
    track=True  #if page should not be tracked set to False
    tracker=RequestTracker()
    permission_response=None
    title=app.config.get('BASE_TITLE') #setting up default values for application
    keywords=app.config.get('BASE_KEYWORDS')
    description=app.config.get('BASE_DESCRIPTION')
    template=None #defalt Get response based on this template, also looks much better when template moved to header of class
    extend_with=None #magic for modal/html response
    with_navigation=True #determines if depth navigation panel should be built
    navigation=[] #depth navigation list, each super call of prepare can add his location here
    context={} #context of view
    required_permissions=[] #required permissions for this page (moderator/admin)
    method = 'html'
    remember_modal=False
    #if set to True and this View displayed as modal and requires login-> login window will be automaticaly shown and after login redirected to this page
    redirect_in_modal=None
    #determines if redirect occured on this page should be in modal or not, only if window displayed as modal
    page_header=None #used for both regular and modal pages

    def dispatch_request(self, *args, **kwargs):
        #check permissions, if something failed will quit
        self.setEnv()

        ret=False
        error=False


        try:
            if not self.check_permissions(*args,**kwargs):
                ret=self.permission_response
        except PermissionDeniedException as e:
            ret=e.return_response
            if request.url==self.tracker.current:
                self.tracker.rollback_referrer() #infinite loop protection
            error=e.error


        if not ret:
            try:
                ret=self.prepare(*args,**kwargs)
            except RedirectException as e:
                ret=redirect(e.location)
            except ResponseException as e:
                ret=e.response
            except ResponseErrorException as e:
                error=e.error
            except PermissionDeniedException as e:
                ret=e.return_response
                error=e.error

        if not ret and not error:
            #actual response is being serving by requested method name(get/post/etc)
            if self.track and self.method=='html':
                self.tracker.update_referrer()  #update tracker only on html pages
                if session.has_key('login_url'):#after login redirect made by this session var, delete it now
                    del session['login_url']

            try:
                ret=super(MainPage,self).dispatch_request(*args,**kwargs)
                #sucessfull request
            except ResponseErrorException as e:
                error=e.error
            except PermissionDeniedException as e:
                ret=e.return_response
                error=e.error
            #response should be returned in type set by method


        if self.method=='modal':
            if error:
                #return JS based error
                return response_error(error=error)
            if isinstance(ret,BaseResponse):
                #if response is redirect return it with all required settings
                if ret.headers.get('Location'):
                    return response_redirect(
                        redirect_to=ret.headers.get('Location'),
                        in_modal=self.redirect_in_modal,
                        remember_modal=self.remember_modal
                    )
            else:
                #everything fine, show response
                return response_ok(data=ret,force_modal=True)

        if error: #got some error, return to current page (tracker was not updated) and show error
            session['error']=error
            return redirect(self.tracker.current)

        return ret



    def setMetatada(self,title=None,keywords=None,description=None,description_append=False,title_append_base=True,title_append_current=False,keywords_append_current=True):
        """

        :param title:  New title
        :param keywords: New keywords
        :param description: New Description
        :param description_append: Should description be appended to base one?
        :param title_append_base:  Should title be appended to base one?
        :param title_append_current: Should title be appended to current one?
        :param keywords_append_current: Should keywords be appended to current one?
        :return: None
        """
        if title is not None:
            if title_append_base:
                self.title=app.config.get('BASE_TITLE')+" :: "+title
            elif title_append_current:
                self.title=self.title+" :: "+title
            else:
                self.title=title

        if keywords is not None:
            if keywords_append_current:
                self.keywords=self.keywords+","+keywords
            else:
                self.keywords=keywords

        if description is not None:
            if description_append:
                self.description=self.description+" "+description
            else:
                self.description=description

        self.context['title']=self.title
        self.context['keywords']=self.keywords
        self.context['description']=self.description

    def view_level_permissions(self,*k,**kk):
        """
        This function should be overrided if some View has specific logic for permission
        For example if you want to set item_user for View this is the place
        :return: Bool
        """
        return True

    def check_permissions(self,*k,**kk):
        #permissions check
        try:
            self.view_level_permissions(*k,**kk)
        except ResponseException as e:
            self.permission_response=e.response
            return False

        login_url=url_for('user.login')

        #logged in check
        if self.login_required:
            if not current_user.is_authenticated():
                #if self.method!='modal':
                #    login_url=url_for('user.login',next=request.url)
                self.permission_response=redirect(login_url)
                self.remember_modal=True
                self.redirect_in_modal=True
                if self.method=='html':
                    session['login_url']=request.url
                return False

        #admin check
        if self.admin_required:
            if not current_user.admin:
                self.permission_response=redirect(login_url)
                return False
        #ACL check
        if self.item_user:
            failed=False
            try:
                if not self.item_user == current_user:
                    failed=True
            except AttributeError:
                failed=True
            if failed:
                raise PermissionDeniedException(error="Permission denied")

        return True


    def setEnv(self):
        method=request.args.get('method','html')
        self.method=method
        self.context=dict()
        self.context['method']=method
        self.context['extend_with']={
            'modal':'modal_template.html'
        }.get(method,self.extend_with)

    def prepare(self,*k,**kk):
        self.context['display_login_box']=True
        self.context['title']=self.title
        self.context['keywords']=self.keywords
        self.context['description']=self.description
        self.context['tracker']=self.tracker
        if session.get('error'):
            self.context['errors']=[session['error']]
            del session['error']
        self.context['page_header']=self.page_header

        self.navigation=[]

        #create navigation panel
        if self.with_navigation:
            self.navigation.append(html.a(app.config.get('BASE_TITLE'),href="/"))

        self.context['navigation']=self.render_navigation
        self.context['with_navigation']=self.with_navigation


    def get(self,*k,**kk):
        """
        Default response, plain template
        :param k:
        :param kk:
        :return:
        """
        return render_template(self.template,**self.context)

    def post(self,*k,**kk):
        return Response("") #by default return empty page on Post if Post not defined

    def render_navigation(self):
        if self.with_navigation:
            return " >> ".join(self.navigation)


def action(post_method):
    """
    Decorator for forcing post method to check csrf
    :param post_method: function
    :return: function
    """
    def check_csrf(self,*args,**kwargs):
        if session.get('csrf')==request.form.get('csrf') and request.form.get('csrf'):
            return post_method(self,*args,**kwargs)
        else:
            raise PermissionDeniedException(error="Permission denied")
    return check_csrf
