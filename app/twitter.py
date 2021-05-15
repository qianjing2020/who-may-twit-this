""" app/twitter.py
Retrieve tweets and users then create embeddings and populate DB
"""

from os import getenv
import tweepy
import spacy
from .models import DB, User, Tweet

TWITTER_AUTH =  tweepy.OAuthHandler(
    getenv("TWITTER_API_KEY"), 
    getenv("TWITTER_API_SECRET")
    )
TWITTER = tweepy.API(TWITTER_AUTH)

# lodas the nlp model that vectorize text
nlp = spacy.load('my_model')

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    """
    Input a username - the twitter user name after @
    Output - updating database with added/updated user
    """
    try:
        # get twitter user object
        twitter_user = TWITTER.get_user(username)
        # retrieve 200 tweets from this twitter user
        tweets = twitter_user.timeline(
            count=200, 
            exclude_replies=True, 
            include_rts=False, # exclude retwitt
            tweet_mode="extended"
        ) 
        
        # Get the most recent tweet id
        if tweets:
            newest_tweet_id = tweets[0].id
        else:
            newest_tweet_id = None
        
        # Update or add user to our DB
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username, newest_tweet_id=newest_tweet_id) 
        DB.session.add(db_user) 

        # add each tweet into tweet table
        for tweet in tweets:
            tweet_vector =vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(
                id=tweet.id,
                text=tweet.full_text,
                vect=tweet_vector,
                user_id=db_user.id
                )
            db_user.tweets.append(db_tweet) # through the backref
            DB.session.add(db_tweet)
           
    except Exception as e:
        print('***************Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()
