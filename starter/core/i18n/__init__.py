from flask.ext.babel import gettext

__author__ = 'tigra'

def _(string,**variables):
    return gettext(string,**variables)


def __(string):
    """
    just to make record of translations
    """
    return string