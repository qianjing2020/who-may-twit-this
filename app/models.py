""" 
app/models.py
SQLAlchemy User and Tweet models for out database
"""
from flask_sqlalchemy import SQLAlchemy


# create a DB Object from SQLAlchemy class
DB = SQLAlchemy()

# Create a table user
class User(DB.Model):
    """Create a table called user with SQlAlchemy, inheriting from DB.Model class.
    """
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(50), unique=True)
    newest_tweet_id = DB.Column(DB.BigInteger)
    
    def __repr__(self):
        return "<User: {}>".format(self.name)

# Create a Tweet table
class Tweet(DB.Model):
    """Creat a table called tweet that keeps track of Tweets for each user"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # allows for text and links
    vect = DB.Column(DB.PickleType, nullable=False) # converted text vectors are stored as pickle

    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)  # each tweet must have a user_id, note the user (lowercase) is the table we defined using User class
    
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))  # backref stored a Tweet object under User_object.tweet
    
    def __repr__(self):
        return "<Tweet: {}>".format(self.text)

# def insert_example_users():
#     user1 =  User(id=1, name='April Ferguson')
#     user2 = User(id=2, name='May Mulligan')
#     DB.session.add(user1)
#     DB.session.add(user2)
#     DB.session.commit()

"""
To create all talbes, in flask shell:
~~~
from app.models import DB
DB.create_all()
~~~
"""

