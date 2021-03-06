"""
config.py

Configurations in a single file

To use DevelopmentConfig, in terminal cli:
$ export APP_SETTINGS="config.DevelopmentConfig"
"""

import os
from dotenv import load_dotenv

load_dotenv

# base configuration
class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    

# product config
class ProductionConfig(Config):
    Env = "production" # actually the default of flask
    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL')

# dev config
class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False   
    DATABASE_URL = "sqlite:///db.sqlite3"

# test config
class TestingConfig(Config):
    TESTING=True

