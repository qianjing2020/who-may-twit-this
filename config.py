"""
config.py

Configurations in a single file

To use DevelopmentConfig, in terminal cli:
$ export APP_SETTING="config.DevelopmentConfig"
"""

import os
from dotenv import load_dotenv

load_dotenv

#basedir = os.path.abspath(os.path.dirname(__file__))

# base configuration
class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
    DATABASE_URL = "sqlite:///db.sqlite3"

# dev config
class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False    

# product config
class ProductionConfig(Config):
    Env = "production" # actually the default of flask
    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL')


# test config
class TestingConfig(Config):
    TESTING=True

