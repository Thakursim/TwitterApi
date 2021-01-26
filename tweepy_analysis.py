
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 
from tweepy import Cursor
from tweepy import API

import credentials
import numpy as np 
import pandas as pd 

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client    

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets  

    def get_friend_list(self, num_friends):
        friend_list = []
        for friends in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        get_home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets                          


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    # class for streaming and processing live tweets.
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles twitter authentication and the connection to the Twitter Streaming API.
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        # This line filter Twitter Streams to capture data by the keyword.
        stream.filter(track=hash_tag_list)

class TwitterListener(StreamListener):
    # This is a basic listener class that just prints received tweets to stdout. 
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try: 
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)

class TweetAnalyzer():
    # Functionality for analyzing and categoring content from tweets.        
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df

if __name__=="__main__":

    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()
    tweet_analyzer = TweetAnalyzer()
    tweets = api.user_timeline(screen_name="@IAF_MCC", count=5)
    df = tweet_analyzer.tweets_to_data_frame(tweets)

    # print(dir(tweets[0]))
    print(df.head(10))
    # print(tweets[0].id)
    #print(tweets[0].retweet_count)


