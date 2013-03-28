__author__ = 'tigra'

from flask.helpers import json
from flask.wrappers import Response

__author__ = 'tigra'

def response_error(error):
    return Response(json.dumps({
        'status':0,
        'message':error,
        'call':False
    }))

def response_redirect(redirect_to=None,in_modal=False,remember_modal=False,redirect_on_close=None):
    out_dict={
            'status':5,
            'redirect_to':redirect_to,
            'call':False,
            'in_modal':in_modal,
            'remember_modal':remember_modal
        }
    if redirect_on_close:
        out_dict['redirect_on_close']=redirect_on_close

    return Response(json.dumps(out_dict))

def response_ok(data=None,message=None,force_modal=False):
    if message is not None:
        status=2
    else:
        status=1
    return Response(json.dumps({
            'status':status,
            'data':data,
            'message':message,
            'call':True,
            'force_modal':force_modal
        }))

def response_request_confirmation(message=None,confirmation_url=None,post=None):
    """
    Confirmation is always must be post

    @param message:
    @param confirmation_url:
    @return:
    """
    return Response(json.dumps({
        'status':4,
        'message':message,
        'confirmation_url':confirmation_url,
        'call':False,
        "post":True
    }))
