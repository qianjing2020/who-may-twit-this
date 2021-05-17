"""app/flask_app.py"""

import os
from flask import Flask, render_template, request
from twitcomp.models import DB, User
from twitcomp.twitter import add_or_update_user
from twitcomp.predict import predict_twitter
import commands

def create_app():
    
    app = Flask(__name__) # __name__: current path module

    env_configuration = os.environ['APP_SETTINGS']
    app.config.from_object(env_configuration)
    """
    For heroku deploy. Accordingly, add config var through CLI: $ heroku config:set APP_SETTINGS:config.ProductionConfig
    """
    # print(app.config)  # shows the dictionary of configuration

    DB.init_app(app) # register database with flask app

    # commands.init_app(app) # register commands with flask app
 
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()        
        return render_template('base.html', title='Database reset done.') 

    @app.route('/')
    def root():   
        users = User.query.all() 
        return render_template('base.html', title='Prediction', users=users)

    # page show added/updated user    
    @app.route('/user', methods=["POST"])
    @app.route('/user/<name>', methods=["GET"])
    def user(name=None, message=''):
        # we either take name that was passed in or we pull it
        # from our request.values which would be accessed through the
        # user submission
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} Succesfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = "********* Error adding {}: {}".format(name, e)
            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)

    # The comparison result page
    @app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values["user1"]])

        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            # prediction returns a 0 or 1
            prediction = predict_twitter(
                user0, user1, request.values["tweet_text"])

            message = "'{}' is more likely to be said by {} than {}!".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('prediction.html', title="Prediction", message=message)


    return app