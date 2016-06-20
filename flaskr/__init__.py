from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import re
from flask.ext.mail import Mail
from momentjs import momentjs

app=Flask(__name__)
app.wsgi_app=ProxyFix(app.wsgi_app)
app.config.from_object('config')

################mail setting#####
mail=Mail(app)
######sql initialize#############
db=SQLAlchemy(app)
#############login manager######
lm=LoginManager()
lm.init_app(app)
lm.login_view='login'
################error############
import errorlog
errorlog.ErrorMail()
# #####blueprint registe###########
# from flaskr.postsviews import viewposts
# app.register_blueprint(viewposts)
##################################
re_email_str=re.compile(r'([0-9a-zA-Z][0-9a-zA-Z._]{,15}[0-9a-zA-Z])@([0-9a-zA-Z.]+)$')
re_password_str=re.compile(r'\w{6,16}')
re_uppercase=re.compile(r'[A-Z]+')
re_number=re.compile(r'[0-9]+')
###################import py pacage member
app.jinja_env.globals['momentjs']=momentjs
import appviews,forms,models,postsviews



