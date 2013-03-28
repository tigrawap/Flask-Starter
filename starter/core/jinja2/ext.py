from jinja2 import nodes
from jinja2.ext import Extension

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_by_name

class PygmentsExtension(Extension):
    """
    A Pygments extension for use with the Jinja2 template language.
    
    Setup:
    
    import PygmentsExtension
    from jinja2 import Environment
    
    jinja2_env = Environment(extensions=[PygmentsExtension])
    
    Usage:
    
    {% code 'javascript' %}
    function foo() { console.log('bar'); }
    {% endcode %}
    """
    tags = set(['code'])
    
    def __init__(self, environment):
        super(PygmentsExtension, self).__init__(environment)
        
        # add the defaults to the environment
        environment.extend(
            pygments=self
        )
    
    def parse(self, parser):
        lineno = parser.stream.next().lineno
        
        args = []
        lang_type = parser.parse_expression()
        
        if lang_type is not None:
            args.append(lang_type)
        
        body = parser.parse_statements(['name:endcode'], drop_needle=True)
        
        return nodes.CallBlock(self.call_method('_pygmentize', args), 
                                [], [], body).set_lineno(lineno)
    
    def _pygmentize(self, lang_type, caller):
        lexer = None
        formatter = HtmlFormatter(linenos=False)
        content = caller()
        
        if lang_type is None:
            lexer = guess_lexer(content)
        else:
            lexer = get_lexer_by_name(lang_type)
        
        return highlight(content.unescape(), lexer, formatter)
