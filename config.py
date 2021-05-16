import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TWITTER_API_KEY=os.environ.get(TWITTER_API_KEY)
    TWITTER_API_SECRET=os.environ.get(TWITTER_API_SECRET)
    DATABASE_URL="sqlite:///db.sqlite3"

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///local_database.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

