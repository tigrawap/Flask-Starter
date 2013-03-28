"""
Use export STARTER_CONFIG=settings_production.py for production server
Change STARTER to any name your prefer
"""
ENVIRONMENT_CONFIG_VAR="STARTER_CONFIG"

#App settings
#Change it for your application!!!
SECRET_KEY="ASDFJB234;LDSKDSFbjkl234908cxLDKGDFJadsf,m,23lkjd"

#Server settings
BASE_PATH='/Users/tigra/Development/flask/flask-starter/flask-starter/'
LOCAL_SERVER=True
STATIC_URL="/static"
BASE_URL="http://localhost:8080/"

#content settings
SHOW_SOCIAL_BUTTONS=False
BASE_TITLE="Flask Starter App by Tigra"
BASE_KEYWORDS="python, flask, starter"
BASE_DESCRIPTION="Very cool and simple flask starter package"