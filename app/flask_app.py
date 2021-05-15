# app/flask_app.py
from operator import add
from os import getenv
from flask import Flask, render_template
from .models import DB, User
from .twitter import add_or_update_user

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initiate database
    DB.init_app(app)

    @app.route('/')
    def root():
        add_or_update_user('elonmusk')
        add_or_update_user('nasa')
        
        users = User.query.all()  # query the user table
        return render_template('templates/base.html', title='home', users=users)
        # "Hello, who-may-have-twitted-this!"
    
    @app.route('/update')
    def update():
        add_or_update_user('elonmusk')
        add_or_update_user('nasa')
        return render_template('base.html', title='home', users=User.query.all())

    @app.route('/reset')
    def update():
        DB.drop_all()
        DB.create_all()
        
        return render_template('base.html', title='home') 

    return app