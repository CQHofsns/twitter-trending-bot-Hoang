"""
@author: chuquangnguyenhoang
"""
import tweepy
import configparser
import pandas as pd
from datetime import date
from datetime import timedelta
import operator
import os
# API Keys and Tokens
config = configparser.RawConfigParser()
config.read('key.cfg')
consumer_key = config.get('API', 'key')
consumer_secret = config.get('API', 'secret')
access_token = config.get('API', 'token')
access_token_secret = config.get('API', 'tokensecret')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
# Def


def get_trends(api, loc):
    trends = api.get_place_trends(loc)
    return trends[0]["trends"]


def printtweetdata(ith_tweet):
    print()
    print(f"Username:{ith_tweet[0]}")
    print(f"Tweet Text:{ith_tweet[1]}")


def scrape(query, date_since, numtweet):
    query = words + ' -filter:retweets'
    tweets = tweepy.Cursor(
        api.search_tweets,
        query,
        lang="en",
        since_id=date_since,
        result_type='mixed',
        tweet_mode='extended').items(numtweet)
    list_tweets = [tweet for tweet in tweets]
    i = 1
    for tweet in list_tweets:
        username = tweet.user.screen_name
        text = tweet.full_text
        text = text.replace('\n', '').replace(',', '')
        db['trendings'].append(words)
        db['username'].append(username)
        db['text'].append(text)
    i = i+1
    return db
# Main


if __name__ == '__main__':
    c = {}
    db = {'trendings': [], 'username': [], 'text': []}
    loc = "23424977"
    trends = get_trends(api, loc)
    for i in range(len(trends)):
        if trends[i]['tweet_volume'] is not None and trends[i]['name'] not in c:
            c[trends[i]['name']] = trends[i]['tweet_volume']
    d = (sorted(c.items(), key=operator.itemgetter(1), reverse=True)[0:10])
    d = {k: v for k, v in d}
    date_since = date.today() - timedelta(days=1)
    for words in d:
        numtweet = 10
        db = scrape(words, date_since, numtweet)
    df = pd.DataFrame.from_dict(db)
    timestr = date.today().strftime("%Y%m%d")
    fullname = os.path.join("data", timestr+"tweetsfromtrending#s.csv")
    df.to_csv(fullname, index=False, mode="w+", encoding='utf-8')
