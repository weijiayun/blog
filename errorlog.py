#!/opt/Apps/local/Python/anaconda/bin/python2.7
from flaskr import app
from config import MAIL_PASSWORD,MAIL_SERVER,MAIL_PORT,MAIL_USERNAME,ADMINS

def ErrorMail():
    if not app.debug:
        import logging
        from logging.handlers import SMTPHandler
        credentials=None
        if MAIL_USERNAME or MAIL_PASSWORD:
            credentials=(MAIL_USERNAME,MAIL_PASSWORD)
        mail_handler = SMTPHandler(MAIL_PORT,
                                   'no-reply@' + MAIL_SERVER,
                                   ADMINS, 'microblg failture',credentials)
        from logging import Formatter
        mail_handler.setFormatter(Formatter('''

Messagetype:        %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
'''))
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

def ErrorLog():
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('tmp/Jiayunblog.log', 'a', 1 * 1024 * 1024, 10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('microblog startup')