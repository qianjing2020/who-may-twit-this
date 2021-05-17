"""
app/predict.py
Predict which user is more likely to twit a tweet of input text.
"""
import numpy as np
from sklearn import linear_model
from twitcomp.models import User
from twitcomp.twitter import vectorize_tweet

def predict_twitter(user0_name, user1_name, hypo_tweet_text):
    """
    Determine and returns which user is more likely to say a given tweet

    Example run: predict_user("elonmusk", "jackblack", "Tesla cars go vroom")
    Returns a 0 (user0_name: "elonmusk") or a 1 (user1_name: "jackblack")
    """
    # Grabbing user from our DB
    # The user we want to compare has to be in our DB
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()

    # Grabbing tweet vectors from each tweet for each user
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Vertically stack tweet_vects to get one np array, this is our x
    vects = np.vstack([user0_vects, user1_vects])
    # Stack lables, this is our y
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    # fit a logistic regression model 
    log_reg = linear_model.LogisticRegression().fit(vects, labels)

    # prepare the input hypothetical tweet for prediction 
    input_tweet_vect = vectorize_tweet(hypo_tweet_text)
    label_pred = log_reg.predict(input_tweet_vect.reshape(1, -1))

    return label_pred
