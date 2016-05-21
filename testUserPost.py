#!/opt/Apps/local/Python/anaconda/bin/python2.7

from flaskr import models
from flaskr import db

    # u= flaskr.models.User(nickname='susan',email='susan@email.com')
    # db.session.add(u)
    # db.session.commit()
    # users=models.User.query.all()
    # print(users)
    # for u in users:
    #     print(u.id,u.nickname)
    # import datetime
    # u=models.User.query.get(1)
    # p=models.Post(body='my first blog',timestamp=datetime.datetime.utcnow(),author=u)
    # db.session.add(p)
    # db.session.commit()
    # p=models.Post(body='may the force be with you',timestamp=datetime.datetime.utcnow(),author=u)
    # db.session.add(p)
    # db.session.commit()
    #
    # users=models.User.query.all()
    # for u in users:
    #     db.session.delete(u)
    # posts=models.Post.query.all()
    # for p in posts:
    #     db.session.delete(p)
    # db.session.commit()
    #
    # jposts=u.posts.all()
    # print(jposts)
    # for postpiece in jposts:
    #     print postpiece.id,postpiece.author.nickname,postpiece.body
#from flask.ext.mail import Message
# from flaskr import mail,app
# from config import ADMINS
# #msg=Message('test subject',sender=ADMINS[0],recipients=ADMINS)
# msg.body='test body'
# msg.html='<b>HTML</b> body'
# with app.app_context():
#     mail.send(msg)
#





