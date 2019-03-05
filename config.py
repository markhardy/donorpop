import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
basedir = os.path.abspath(os.path.dirname(__file__))


#############################################################
#   class Config                                            #
#                                                           #
#   Configurations common to all other Config sub-classes.  #
#   This is a superclass inherited by other Config types.   #
#############################################################
class Config:
    #   NOTE: Any environ.gets must be input in quotes

    #   Set value in console or it will default
    SECRET_KEY = os.environ.get('SECRET_KEY') or "A66056504F1301826"

    #   Commit to database after each query/action
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    #   Email configuration
    FLASKY_MAIL_SUBJECT_PREFIX = 'DonorPop'
    FLASKY_MAIL_SENDER = 'DonorPop Admin <mark@mangosring.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    UPLOAD_FOLDER = "C:\Users\Mark Awesome\Desktop\Flask\Hellowold\github\hub\uploads"
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
    SSL_DISABLE = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = "sub5.mail.dreamhost.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "mark@mangosring.com" #os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = "A66056504" #os.environ.get('MAIL_PASSWORD')
    
    #   Change to os.environ.get before deploying
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://mwhardy1985:A66056504a!@hardydb.cr19zma8gn4h.us-east-1.rds.amazonaws.com/hardydb.cr19zma8gn4h.us-east-1.rds.amazonaws.com:3306"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:A66056504@127.0.0.1/attendance_dev" #For local db
    
class TestingConfig(Config):
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://mwhardy1985:A66056504a!@hardydb.cr19zma8gn4h.us-east-1.rds.amazonaws.com/hardydb.cr19zma8gn4h.us-east-1.rds.amazonaws.com:3306"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:A66056504@127.0.0.1/attendance_test"

class ProductionConfig(Config):
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://mwhardy1985:A66056504a!@hardydb.cr19zma8gn4h.us-east-1.rds.amazonaws.com/hardydb.cr19zma8gn4h.us-east-1.rds.amazonaws.com:3306"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                                'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class HerokuConfig(Config):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stdderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)
        SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'heroku' : HerokuConfig,

    'default' : DevelopmentConfig
}

