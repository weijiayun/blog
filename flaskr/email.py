#!/opt/Apps/local/Python/anaconda/bin/python2.7
from flask.ext.mail import Message
from flaskr import mail,app
from flask import render_template
from config import ADMINS
def send_email(subject,sender,recipients,text_body,html_body):
    msg=Message(subject,sender=sender,recipients=recipients)
    msg.body=text_body
    msg.html=html_body
    mail.send(msg)

def follow_notification(followed,follower):
    send_email('[microblog] {} is now following you'.format(follower.nickname),
               ADMINS[0],
               [followed.email],
               render_template("follower_email.txt",user=followed,follower=follower),
               render_template("follower_email.txt",user=followed,follower=follower))

