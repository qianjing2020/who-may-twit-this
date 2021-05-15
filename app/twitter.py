""" app/twitter.py
Retrieve tweets and users then create embeddings and populate DB"""

from os import getenv
import tweepy
import spacy
from .models import DB, User, Tweet

TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = getenv("TWITTER_API_SECRET")
TWITTER_AUTH =  tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

# nlp model
nlp = spacy.load('my_model')
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

# add user to db 
def add_or_update_user(username):
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username) # get or create
        DB.session.add(db_user) # updated DB user table

        # get 200 tweets
        tweets = twitter_user.timeline(
            count=200, 
            exclude_replies=True, 
            include_rts=False, # exclude retwitt
            tweet_mode="extended"
        ) 

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # add each tweet into tweet table
        for tweet in tweets:
            vectorized_tweet =vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, 
            text=tweet.full_text,
            vect=vectorized_tweet)
            
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
        
        DB.session.commit()
    
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e


"""
flask shell
from app.twitter import add_or_update_user
add_or_update_user('nasa')
"""