# Flask-Starter

Structure of Flask project easily used both for small and big apps. Includes great communication layer, between APP and client.

##Zen##

I see a lot of questions from Flask beginners, how to add some content to every page.  
How to write in DRY style in Flask, etc, etc.

But the point is, that most of people do it with function-based Views.  
Well, actualy nothing wrong with it, you can decorate them, you can add pre-request and after-request handles. But common, this is a mess.  
Is not it better to just add `login_required=True` to class definition of View and `admin_required` to class definition of AdminPage View instead of messing around with decorators?

So in my opinion in most cases View should be the extension of some Base View. This does not mean that you cannot use simple function-based view when you need.

Plus, the Flask framework itself and its documentation is great, but it does not provide a whole overview of a well structured project.

##Installation

To test this on live you will need:

1) Python, preferably 2.7, not tested with prior versions.  
2) virtualenv  

a) Create new virtual env anywhere (but better not inside project itself) `virtualenv starter-env`  
b) Activate it `source starter-env/bin/activate`  
c) Install dependencies: `pip install -r requirements.txt`  
d) Copy settings_default.py to settings.py  
e) Run server: `python runserver.py`  


Server will be started on localhost:8080 port, to adjust it modify runserver.py
###Live demo
Also, you can view some examples at http://flask-starter-demo.tigranet.com

###Dependencies
**Babel** used by forms and lately i18n support will be explained.  
**Pygments** used for syntax highlight , so if you dont need it you can remove supplied Main blueprint and uninstall pygments with pip


## Overview

So, as been told, One View to Rule Them All.  
Too bad, __OVtRTA__ sucks as a name

### Structure

Flask-Starter utilizes Flask blueprints.   
You can use blueprints as separate applications, attach a blueprint to a specific subdomain, etc.  
But you also can use blueprints for grouping logic.  
For example: User blueprint for all user-related tasks and models.

#### File Structure
On top-level of project there are settings files and runserver.py, it is also a good place to put production starter for gunicorn or other WSGI server.

**settings.py** is a base settings file.  
**settings_production.py** can extend/overwrite settings defined in first one.  
To load **settings_production.py** you should specify it's path in enviroenment variable specified in **settings.py**  
For example, by default in **settings.py**
`ENVIRONMENT_CONFIG_VAR="STARTER_CONFIG"`  
So by running   
`export STARTER_CONFIG="/path/to/settings_production.py"`
before `python runserver.py` this settings file also will be loaded.  
On production I advise to use `supervisor` and with it you can just specify 
`environment=STARTER_CONFIG="/path/to/settings_production.py"` inside task definition

##### Folders/Files
**/core** stores base View and other additional functions, the idea that everything can be done without touching /core, but you for sure can if you want, it is also one of the reasons, why I don't want to put this Starter to pypi, it is not module, it is not library. It is Starter-project which you can modify however you want  
  
- **/static** used for storing static files  
- **/media** usualy used for user-uploaded files  
- **/main** Blueprint with demos. You can just disable it   in **blueprints.py**
- **/user** Blueprint with user, good place to start on expanding model and registration.  
- **/templates** Store your templates here
- **views.py** Default View, inhereted from core/View  
Use this file as start point to create your generic view  
- **blueprints.py** A place to load blueprints.  

#####Templates

Jinja2 Templates inheritance, another great thing.  
Take a look on index.html and modal_template.html
 
The View class decides which one to use as starting point via the **extends_with** attribute.  
Want to use some other template as starting point for a View and its child Views? Just change this attribute on any level.

	class AdminPage(MainPage):
		extend_with="admin_page.html"
		admin_required=True

(your User class should have **.admin** attribute or property for this to work)

Inside template always use 
`{% extends extend_with %}` in the beginning of .html file so you always can easily change parent template.

##### JS, CSS
Bootstrap, jQuery and require.js included inside this Starter project, as well as examples.

You can take a look on examples (live page) by following this link:
**<http://flask-starter-demo.tigranet.com>**

The core over there is RemoteModal and Requests integrated with Flask-Starter itself.   
JS still requires some refactoring, but well, it works and very easy to use.  
Meanwhile refer to this page or to the code for how-to-use.

You also can email me for questions or ask at stackoverflow with flask or flask-starter tags.  
This documentation will be expanded as soon as possible base on your questions 

##### Core View 

Has different attributes, for controlling behaviour, display style and other.  
Meanwhile please refer to it's definition, it's documented somehow.

Just some of available attributes for class definition: 
 
- **login_required** bool, view required login
- **track** bool, default True, tracking for page  
**Definition of tracking:**  every View has access to `RequestTracker` which stores the current and previous locations in session. They can be accessed by `self.tracker.current`, `self.tracker.referrer` and `self.tracker.prev_referrer` inside view. This has various usages. More documentation on this matter will come later. BTW, if `track=False` self.tracker.current actually refers to last tracked url, not current one.

- **template** template to display for this View without need to redefine `def get`  
So minimal Class will look like this
***

	class SimplePage(MainPage):
		template="simple_page.html"

And if you want to add some functional and add something to context of it - yet again, no need to redefine get:

	class SimplePage(MainPage):
		template="simple_page.html"
		page_header="My Cool Simple Page"
		def prepare(*k,**kk	):
			self.context['some_data']="data comes here"
			super(SimplePage,self).prepare(*k,*kk)
			
But if you want…you can, still simple. All the magic done on inner level, so if page will be requested as Modal -> it will be shown as modal.


	class SimplePage(MainPage):
		template="simple_page.html"
		page_header="My Cool Simple Page"
		def get(*k,**kk	):
			self.context['some_data']="data comes here"
			return render_template(self.template,**self.context)

**Another example of core View usage.  **  
It is often useful to set title, keywords, description to the page.

You can easily set it in your prepare (or get, or post) method:

	def setMetatada(self,title=None,keywords=None,description=None,description_append=False,title_append_base=True,title_append_current=False,keywords_append_current=True):
        """
        :param title:  New title
        :param keywords: New keywords
        :param description: New Description
        :param description_append: Should description be appended to base one?
        :param title_append_base:  Should title be appended to base one?
        :param title_append_current: Should title be appended to current one?
        :param keywords_append_current: Should keywords be appended to current one?
        
        
### more to come…

You also can email [Me](mailto:tigrawap@gmail.com) for questions or ask at stackoverflow with flask or flask-starter tags.    
This documentation will be expanded as soon as possible and will incorporate your questions.

