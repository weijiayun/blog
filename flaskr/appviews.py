#!/opt/Apps/local/Python/anaconda/bin/python2.7

import re,os,shutil
from flask import redirect,request,\
    session,url_for,g,abort,render_template,flash
from flaskr import models,db,app,re_email_str,re_number,re_password_str,re_uppercase
from flaskr import lm
from .forms import LoginForm,SearchForm
from flask.ext.login import current_user,login_user,login_required
from datetime import datetime
from email import follow_notification

def uniqueMail(newemail):
    user=models.User.query.filter_by(email=newemail).first()
    if user!=None:
        return False
    return True
@app.before_first_request
def before_first_request():
    session['logged_in']=False
@app.before_request
def befort_request():
    g.search_form=SearchForm()
    g.user=models.User(nickname="",password="",email="")
    g.user=current_user
    g.user.last_seen=datetime.utcnow()

@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@app.route('/search',methods=['POST'])
@login_required
def search():
    if request.method=="POST":
        if session.get('logged_in'):
            return redirect(url_for('search_results', query=request.form['search']))
    return redirect(url_for('index'))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    g.title='Search results'.format(query)
    results=models.Post.query.whoosh_search(query,app.config['MAX_SEARCH_RESULTS']).all()
    return render_template('search_results.html',
                           query=query,
                           results=results,
                           providers=app.config['OPENID_PROVIDERS']
                           )

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
@login_required
def index(page = 1):
    g.search_form=SearchForm()
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    g.title = "Microblog"#.format(g.user.nickname)
    items_per_page = g.user.get_items_per_page()
    totalpages = g.user.get_followed_posts_count()
    totalpages = int((totalpages + items_per_page - 1) / items_per_page)
    cur =g.user.get_followed_posts(page=page)
    return render_template('index.html',
                           posts=cur,
                           totalpages = totalpages,
                           crtpage = page,
                           providers=app.config['OPENID_PROVIDERS']
                           )

@app.route('/login',methods=['GET','POST'])
def login():
    g.title='Log In'
    error = None
    form=LoginForm()
    remember_me=False
    g.crtpage = 1
    if request.method == 'POST':
        cur=models.User.query.all()
        usersInfo = [dict(useremail=user.email, password=user.password,ID=int(user.get_id())) for user in cur]
        userlist=[]
        for foo in usersInfo:
            userlist.append(foo['useremail'])
        if request.form['email'] not in userlist:
            error='The Account Is Not Signed'
        else:
            userindex = userlist.index(request.form['email'])
            userID=usersInfo[userindex]['ID']
            user=load_user(userID)
            if request.form['password']!=usersInfo[userindex]['password']:
                error='The Password Cannot Match The Account'
            else:
                session['crtUser']=userID
                session['logged_in']=True
                remember_me = form.remember_me.data
                login_user(user,remember=remember_me)

                return redirect(url_for('index'))
    return render_template('login.html',
                           error=error,
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/logout')
def logout():
    session['logged_in']=False
    session.pop('logged_in')
    session.pop('crtUser')
    #session.pop('remember_me')
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/signup',methods=['GET','POST'])
def signup():
    tmpNickname=""
    error = None
    g.title="Sign up"
    if request.method == 'POST':
        if len(request.form['username'])==0 or len(request.form['password1'])==0 or len(request.form['password2'])==0:
            error='Those information shall not be empty'
        elif request.form['password1']!=request.form['password2']:
            error='password1 cannot match the password2'
        elif re.match(re_password_str,request.form['password1']) is None:
            error='The password length should satisfield the range [6-16]'
        elif re.search(re_uppercase,request.form['password1']) is None:
            error='The password should satisfield at least one capital letter'
        elif re.search(re_number,request.form['password1']) is None:
            error='The password should satisfield at least one digit'
        elif re.match(re_email_str,request.form['email']) is None:
            error='The email name is illegal'
        elif uniqueMail(request.form['email']):
            newuser=models.User(nickname=request.form['username'],password=request.form['password1'],email=request.form['email'])
            db.session.add(newuser)
            db.session.commit()
            db.session.add(newuser.follow(newuser))
            db.session.commit()
            flash('New account has been successfully signed up')
            return redirect(url_for('login'))
        else:
            tmpNickname=request.form['username']
            error='The email has been registered'
    return render_template('signup.html',
                           tmpNickname=tmpNickname,
                           error=error,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/follow/<email>')
@login_required
def follow(email):
    user=models.User.query.filter_by(email=email).first()
    if user is None:
        flash('User {} not found'.format(email))
        return redirect(url_for('index'))
    if user==g.user:
        flash("You can't follow yourself")
        return redirect(url_for('user',email=email,page = g.crtpage))
    u=g.user.follow(user)
    if u is None:
        flash('Cannot follow'+user.nickname+'!')
        return redirect(url_for('user',email=email,page = g.crtpage))
    db.session.add(u)
    db.session.commit()
    follow_notification(user,g.user)
    flash('You are following '+user.nickname)
    return redirect(url_for('user',email=email,page = g.crtpage))

@app.route('/unfollow/<email>')
@login_required
def unfollow(email):
    user=models.User.query.filter_by(email=email).first()
    if user is None:
        flash('User {} not found'.format(email))
        return redirect(url_for('index'))
    if user==g.user:
        flash("You can't unfollow yourself")
        return redirect(url_for('user',email=email,page = g.crtpage))
    u=g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow'+user.nickname+'!')
        return redirect(url_for('user',email=email,page = g.crtpage))
    db.session.add(u)
    db.session.commit()
    flash('You have stoped following '+user.nickname)
    return redirect(url_for('user',email=email,page = g.crtpage))

@app.route('/reject/<email>')
@login_required
def reject(email):
    user=models.User.query.filter_by(email=email).first()
    if user is None:
        flash('User {} not found'.format(email))
        return redirect(url_for('index'))
    if user==g.user:
        flash("You can't reject yourself")
        return redirect(url_for('user',email=email,page = g.crtpage))
    u=g.user.reject(user)
    if u is None:
        flash('Cannot follow'+user.nickname+'!')
        return redirect(url_for('user',email=email))
    db.session.add(u)
    db.session.commit()
    flash('You are following '+user.nickname)
    return redirect(url_for('user',email=email))

@app.route('/unreject/<email>')
@login_required
def unreject(email):
    user=models.User.query.filter_by(email=email).first()
    if user is None:
        flash('User {} not found'.format(email))
        return redirect(url_for('index'))
    if user==g.user:
        flash("You can't unfollow yourself")
        return redirect(url_for('user',email=email,page=g.crtpage))
    u=g.user.unreject(user)
    if u is None:
        flash('Cannot unfollow'+user.nickname+'!')
        return redirect(url_for('user',email=email,page=g.crtpage))
    db.session.add(u)
    db.session.commit()
    flash('You have stoped following '+user.nickname)
    return redirect(url_for('user',email=email,page=g.crtpage))

@app.route('/user/<email>/<int:page>',methods=['GET','POST'])
@login_required
def user(email,page = 1):
    u=models.User.query.filter_by(email=email).first()
    if u is None:
        flash('User {} is not found'.format(email))
        return redirect(url_for('index'))

    if u==g.user:
        g.title='My profile'
    else:
        g.title=u.nickname+"'s profile"
    items_per_page = g.user.get_items_per_page()
    totalpages = u.posts.count()
    g.crtpage = page
    totalpages = int((totalpages + items_per_page - 1) / items_per_page)
    cur = u.posts.order_by(models.Post.timestamp.desc()).offset((page-1)*items_per_page).limit(items_per_page).all()
    return render_template('user.html',
        user = u,
        posts = cur,
        crtpage = page,
        totalpages = totalpages,
        providers=app.config['OPENID_PROVIDERS'])

@app.route('/edit',methods=['GET','POST'])
@login_required
def edit():
    if request.method == 'POST':
        pic = request.files['avatarpic']
        picpath = app.config['USER_PIC_FOLDER']
        sufix = pic.filename.split('.')[-1]
        #sufix ='png'
        dirname = picpath+'/'+str(g.user.id)
        version = "1"
        if os.path.exists(dirname) and os.path.isdir(dirname):
            filelist = os.listdir(dirname)
            for f in filelist:
                if len(f.split('.')) == 3:
                    version = f.split('.')[1]
                    version =str(int(version)+1)
                    break
                else:
                    version = '1'
        filename = str(g.user.id) + '/' + str(g.user.id) + '.' + version + '.' + sufix
        g.user.avatarPath = os.path.join(picpath, filename)
        if os.path.exists(os.path.dirname(g.user.avatarPath)):
            shutil.rmtree(os.path.dirname(g.user.avatarPath))
        if not os.path.exists(os.path.dirname(g.user.avatarPath)):
            os.mkdir(os.path.dirname(g.user.avatarPath))
        pic.save(g.user.avatarPath)
        g.user.nickname=request.form['nickname']
        g.user.about_me=request.form['about_me']
        g.user.items_per_page = request.form['items_per_page']
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        g.crtpage = 1
        return redirect(url_for('user', email=g.user.email, page=g.crtpage))
    return render_template('edit.html',providers=app.config['OPENID_PROVIDERS'])

@app.route('/delelte/<postid>')
@login_required
def delpost(postid):
    post=models.Post.query.get(postid)
    if post is None:
        flash('Cannot delete ' +post.title + '!')
        return redirect(request.referrer)
    user = models.User.query.filter_by(email=post.author.email).first()
    if user is None:
        flash('User {} not found'.format(post.author.email))
        return redirect(request.referrer)
    if user == g.user:
        db.session.delete(post)
        db.session.commit()
        flash('You Have Deleted ' + post.title)
    return redirect(request.referrer)

@app.route('/addcomment/<postid>',methods=['GET','POST'])
@login_required
def addcomment(postid):
    topost = models.Post.query.get(postid)
    if request.method=="POST":
        if topost is None:
            flash(topost.title + ' is not exits!')
            return redirect(url_for('index'))
        u=models.Comment(body=request.form['comment'],byuser=g.user,topost=topost,timestamp=datetime.utcnow())
        if u is None:
            flash('Connot make a comment to {}'.format(topost.title))
            return redirect(url_for('index'))
        db.session.add(u)
        db.session.commit()
        g.title='Comment'
        return redirect(request.referrer)
    return render_template('addcomment.html',
                           post=topost,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/like/<postid>')
@login_required
def like(postid):
    post = models.Post.query.get(postid)
    if post is None:
        flash('Post {} not found'.format(post.title))
        return redirect(request.referrer)
    likers={lk.byuser.email:lk.id for lk in post.likes.all()}
    if g.user.email in likers.keys():
        db.session.delete(models.Like.query.get(likers[g.user.email]))
    else:
        lk=models.Like(is_like=True,byuser=g.user,topost=post,timestamp=datetime.utcnow())
        if lk is None:
            flash('sorry! you cannot like the post')
            return redirect(request.referrer)
        db.session.add(lk)
    db.session.commit()
    return redirect(request.referrer)
@app.route('/add',methods=['GET','POST'])
def add_post():
    g.title='New status'
    if request.method=='POST':
        if len(request.form['title'])==0 or len(request.form['text'])==0:
            flash('Title and text cannot be empty!!!')
            return redirect(request.referrer)
        uid=session.get('crtUser')
        u=models.User.query.get(uid)
        p=models.Post(title=request.form['title'],body=request.form['text'],timestamp=datetime.utcnow(),author=u)
        db.session.add(p)
        db.session.commit()
        flash('New entry was successfully posted')
        return redirect(request.referrer)
    return render_template('index.html',
                           providers=app.config['OPENID_PROVIDERS'])

#############custom http error######################
@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'),500


