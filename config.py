#!/opt/Apps/local/Python/anaconda/bin/python2.7
import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
WHOOSH_BASE=os.path.join(basedir,'search.db')
MAX_SEARCH_RESULTS=50
OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    {'name':'SJTU','url':'http://www.sjtu.edu.cn'},
    {'name':'Wechat','url':'http://www.wechat.com'}
    ]
SQLALCHEMY_TRACK_MODIFICATIONS=True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database/flaskr.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'database/db_repository')
################################
MAIL_SERVER='smtp.qq.com'
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USE_SSL=True
MAIL_USERNAME='294311951'
MAIL_PASSWORD='fangliuqiao520'
ADMINS=['jiayun.wei@foxmail.com']
