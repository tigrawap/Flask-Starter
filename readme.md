# Flask-Starter

Structer of Flask project easily used both for small and big apps. Includes great communication layer, between APP and client

##Zen##

I see a lot of questions from Flask beginners, how to add some content to every page.  
How to write in DRY style in Flask, etc ,etc

But the point is, that most of people do it with function-based Views.  
Well, actualy nothing wrong with it, you can decorate them, you can add pre-request and after-request handles. But common, this is a mess.  
Is not it better to just add `login_required=True` to class definition of View and `admin_required` to class definition of AdminPage View instead of messing around with decorators?

So in my opinion in most cases View should be the extension of some Base View. This does not mean that you cannot simple function-based view when you need.

Plus, the Flask itself and is documentation is Great, but it does not provide whole overview of project

## Overview

So, as been told, One View to Rule Them All.  
Too bad, __OVtRTA__ sucks as a name

### Structure

Flask-Starter utilizes Flask blueprints.   
You can use blueprints as sepparate applications, attach some blueprint to specific subdomain and etc.  
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
 
View class decides which one to use as starting point via **extends_with** attribute.  
Want to use some other template as starting point for View and it's child Views? Just change this attribute on any level.

	class AdminPage(MainPage):
		extend_with="admin_page.html"
		admin_required=True

(your User class should have **.admin** attribute or property for this to work)

Inside template always use 
`{% extends extend_with %}` in the beginning of .html file so you always can easily change parent template.

##### JS, CSS
Bootstrap, jQuery and require.js included inside this Starter project, as well as examples.

You can take a look on examples(live page) by following this link:
**<http://flask-starter-demo.tigranet.com>**

The core over there is RemoteModal and Requests integrated with Flask-Starter itself.   
JS still requires some refactoring, but well, it works and very easy to use.  
Meanwhile refer to this page or to code for how-to-use.
