#!/opt/Apps/local/Python/anaconda/bin/python2.7
from flaskr import models,db
from datetime import datetime
from config import OPENID_PROVIDERS
from forms import PostForm

#all the import

from flask import redirect,request,Blueprint,\
    session,url_for,g,abort,render_template,flash

#all the strategies
viewposts=Blueprint('viewposts',__name__,
                      template_folder='templates/viewpages')

@viewposts.route('/add',methods=['GET','POST'])
def add_post():
    g.title='New status'
    if request.method=='POST':
        if len(request.form['title'])==0 or len(request.form['text'])==0:
            flash('Both Title and text cannot be empty')
            return render_template('addpost.html')
        uid=session.get('crtUser')
        u=models.User.query.get(uid)
        p=models.Post(title=request.form['title'],body=request.form['text'],timestamp=datetime.utcnow(),author=u)
        db.session.add(p)
        db.session.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('index'))
    return render_template('addpost.html',
                           providers=OPENID_PROVIDERS)



