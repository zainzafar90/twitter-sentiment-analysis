from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

import twitter_client
import analyzer
import pandas as pd
import numpy as np
import json

class Sentiment(Resource):
     def get(self, query):
        tc = twitter_client.TwitterClient()
        tweet_analyzer = analyzer.TweetAnalyzer()
        tweets = tc.get_tweets(query, 10)
        df = tweet_analyzer.tweets_to_data_frame(tweets)
        df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
        return df.reset_index().to_json(orient='records'), 200

api.add_resource(Sentiment, "/sentiment/<string:query>")

app.run(debug=True)