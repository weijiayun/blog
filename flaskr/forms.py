#!/opt/Apps/local/Python/anaconda/bin/python2.7
from flask.ext.wtf import Form
from wtforms import BooleanField,StringField,TextAreaField,IntegerField
from wtforms.validators import DataRequired,Length

class LoginForm(Form):
    remember_me=BooleanField('remember_me',default=False)

class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    items_per_page = IntegerField('items_per_page',validators=[DataRequired()])
class PostForm(Form):
    post_title = StringField('post_title', validators=[DataRequired()])
    post_body = StringField('post_post', validators=[DataRequired()])
class SearchForm(Form):
    search = StringField('search',validators=[DataRequired()])
