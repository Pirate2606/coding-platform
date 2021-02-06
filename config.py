import os

basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = "supersekrit"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_OAUTH_CLIENT_ID = "YOUR_CLIENT_ID"
    GOOGLE_OAUTH_CLIENT_SECRET = "YOUR_CLIENT_SECRET"

class SendMail(object):
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'YOUR_EMAIL'
    MAIL_PASSWORD= 'GENERATE_PASSWORD_FOR_APP'
    MAIL_DEFAULT_SENDER = 'YOUR_EMAIL'
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False
