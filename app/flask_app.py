"""app/flask_app.py"""

import os
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user
from .predict import predict_twitter

def create_app():
    """
    The main function brings everything together
    """
    app = Flask(__name__) # __name__: current path module
    app.config.from_object(os.environ['APP_SETTINGS'])
    
    DB.init_app(app) # initiate database


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