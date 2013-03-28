from flask import Blueprint, redirect, render_template, url_for, request, Response
from pygments.formatters.html import HtmlFormatter
from starter.core.utils.response import response_ok, response_redirect, response_request_confirmation
from starter.core.views import action
from starter.user import User
from starter.views import MainPage


__author__ = 'tigra'


main = Blueprint('main',__name__)

class IndexPage(MainPage):
    page_header = "Demos"
    template = "main.html"


class LoremIpsum(MainPage):
    page_header = "Lorem Ipsum"
    template = "demos/lorem_ipsum.html"

class LoremIpsumLoginRequired(MainPage):
    login_required = True
    page_header = "Lorem Ipsum, Login Required"
    template = "demos/lorem_ipsum.html"

class ActionRequiresPost(MainPage):
    track = False #no need to track such actions
    page_header = "Action submitted"

    def get(self,*k,**kk):
        #if came by regular link -> just redirect to current page
        return redirect(self.tracker.current)

    @action #forces csrf check
    def post(self,*k,**kk):
        if self.method=='modal':
            return render_template("demos/action_submitted.html",**self.context)
        else:
            self.context['page_header']="Submitted"
            return redirect(url_for('main.action_submitted'))

class ActionRequiresPostMessage(ActionRequiresPost):
    get=None

    @action
    def post(self,*k,**kk):
        return response_ok(message="Action submitted")


class ActionSubmitted(MainPage):
    track =False
    template = "demos/action_submitted.html"


class ActionWithConfirmation(MainPage):
    get=None

    @action
    def post(self,*k,**kk):
        if request.args.get('confirmed'):
            return response_ok(message="Item deleted")
        else:
            return response_request_confirmation(
                message="Are you sure?",
                confirmation_url=url_for('.action_with_confirmation',confirmed=1)
            )

class ActionWithConfirmationCreate(MainPage):
    template = "demos/created_item_description.html"
    page_header = "Done!"


    get=None

    @action
    def post(self,*k,**kk):
        if request.args.get('confirmed'):
            return render_template(self.template,**self.context)
        else:
            return response_request_confirmation(
                message="Are you sure? You got only one chance!",
                confirmation_url=url_for('.action_with_confirmation_create',confirmed=1,method=self.method)
            )


class PageWithLinks(MainPage):
    page_header = "Page with links"
    template = "demos/page_with_links.html"

class PageWithLinks2(MainPage):
    page_header = "Another page with links"
    template = "demos/page_with_links2.html"

class PageWithItemUser(MainPage):
    template = "demos/page_with_item_user.html"
    page_header = "By Tigra for Tigra"

    def view_level_permissions(self,*k,**kk):
        self.item_user=User("Tigra")
        return True

main.add_url_rule('/',view_func=IndexPage.as_view('index'))
main.add_url_rule('/demos/lorem_ipsum.html',view_func=LoremIpsum.as_view('lorem_ipsum'))
main.add_url_rule('/demos/lorem_ipsum_login_required.html',view_func=LoremIpsumLoginRequired.as_view('lorem_ipsum_login_required'))
main.add_url_rule('/demos/action_with_post.html',view_func=ActionRequiresPost.as_view('requires_post'))
main.add_url_rule('/demos/action_with_post_message.html',view_func=ActionRequiresPostMessage.as_view('requires_post_message'))
main.add_url_rule('/demos/action_submitted.html',view_func=ActionSubmitted.as_view('action_submitted'))
main.add_url_rule('/demos/delete',view_func=ActionWithConfirmation.as_view('action_with_confirmation'))
main.add_url_rule('/demos/roll',view_func=ActionWithConfirmationCreate.as_view('action_with_confirmation_create'))
main.add_url_rule('/demos/page_with_links',view_func=PageWithLinks.as_view('page_with_links'))
main.add_url_rule('/demos/page_with_links2',view_func=PageWithLinks2.as_view('page_with_links2'))
main.add_url_rule('/demos/page_with_item_user.html',view_func=PageWithItemUser.as_view('page_with_item_user'))