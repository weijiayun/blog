#!/opt/Apps/local/Python/anaconda/bin/python2.7
from flaskr import db
from hashlib import md5
import sys
from flaskr import app
from imageprocess import reduce
if sys.version_info>=(3,0):
    enable_search=False
else:
    enable_search=True
    import flask.ext.whooshalchemy as whooshalchemy

ROLE_USER=0
ROLE_ADMIN=1
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
rejecters=db.Table('rejecters',
                   db.Column('rejecter_id', db.Integer, db.ForeignKey('user.id')),
                   db.Column('rejected_id', db.Integer, db.ForeignKey('user.id'))
                   )
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64))
    email = db.Column(db.String(120), index = True, unique = True)
    password=db.Column(db.String(20))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    items_per_page = db.Column(db.Integer,default=4)
    avatarPath = db.Column(db.String(140),
                           default='/home/weijiayun/PycharmProjects/blog/flaskr/static/useravatar/lena.png')

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='byuser', lazy='dynamic')
    likes = db.relationship('Like', backref='byuser', lazy='dynamic')
    followed = db.relationship('User',
        secondary = followers,
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id),
        backref = db.backref('followers', lazy = 'dynamic'),
        lazy = 'dynamic')
    rejected = db.relationship('User',
        secondary = rejecters,
        primaryjoin = (rejecters.c.rejecter_id == id),
        secondaryjoin = (rejecters.c.rejected_id == id),
        backref = db.backref('rejecters', lazy = 'dynamic'),
        lazy = 'dynamic')
    def get_items_per_page(self):
        return self.items_per_page

    def avatar(self,size):
        return reduce(self.id,self.avatarPath,size,size)[0]

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) #python 2
        except NameError:
            return str(self.id)#python 3

    def follow(self,user):#if user has been followed by self,return None
        if not self.is_following(user):
            self.followed.append(user)
            return self
    def unfollow(self,user):#if user is not followed by self ,return None
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id==user.id).count()>0

    def Followeds(self):
        return self.followed.filter(followers.c.followed_id!=self.id).all()
    def cntFolloweds(self):
        return self.followed.filter(followers.c.followed_id!=self.id).count()
    def Followers(self):
        return self.followers.filter(followers.c.follower_id!=self.id).all()
    def cntFollowers(self):
        return self.followers.filter(followers.c.follower_id!=self.id).count()
    def reject(self,user):
        if self.is_following(user):
            if not self.is_rejecting(user):
                self.rejected.append(user)
                return self
    def unreject(self,user):
        if self.is_following(user):
            if self.is_rejecting(user):
                self.rejected.remove(user)
                return self

    def is_rejecting(self,user):
        return self.rejected.filter(rejecters.c.rejected_id==user.id).count()>0

    def get_followed_posts_count(self):
        form1 = db.session.query(Post).join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        form2 = db.session.query(Post.id).join(rejecters, (rejecters.c.rejected_id == Post.user_id)).filter(
            rejecters.c.rejecter_id == self.id)
        count = form1.filter(~Post.id.in_(form2)) \
            .order_by(Post.timestamp.desc()).count()
        return count

    def get_followed_posts(self,page):
        form1 = db.session.query(Post).join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        form2 = db.session.query(Post.id).join(rejecters, (rejecters.c.rejected_id == Post.user_id)).filter(
            rejecters.c.rejecter_id == self.id)
        form3 = form1.filter(~Post.id.in_(form2)) \
            .order_by(Post.timestamp.desc())
        form4 = form3.offset((page-1)*self.items_per_page).limit(self.items_per_page).all()
        return form4


    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(1400))
    timestamp = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='topost', lazy='dynamic')
    likes = db.relationship('Like', backref='topost', lazy='dynamic')
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def OutLikers(self):
        likes=self.likes.order_by(Like.timestamp.desc()).all()
        return (i.byuser for i in likes)

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment %r>' % (self.body)
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_like=db.Column(db.Boolean(False))
    timestamp = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Like %r>' % (self.is_like)

if enable_search:
    whooshalchemy.whoosh_index(app,Post)


