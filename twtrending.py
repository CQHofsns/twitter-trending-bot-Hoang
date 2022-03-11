"""
Created on Thu Feb 17 17:35:46 2022

@author: chuqu
"""
import tweepy
import json
import configparser
import pandas as pd
from datetime import date
from datetime import timedelta
import os
#API Keys and Tokens
config = configparser.RawConfigParser()
config.read('key.cfg')
consumer_key = config.get('API','key')
consumer_secret = config.get('API','secret')
access_token = config.get('API','token')
access_token_secret = config.get('API','tokensecret')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit= True)
def get_trends(api,loc):
    trends = api.get_place_trends(loc)
    return trends[0]["trends"]
def extract_hashtags(trends):
    hashtags = [trend["name"] for trend in trends if '#' in trend["name"]]
    return hashtags
def printtweetdata(n, ith_tweet):
    print()
    print(f"Username:{ith_tweet[0]}")
    print(f"Tweet Text:{ith_tweet[1]}")
def scrape(query, date_since, numtweet):
    date_today = date.today()
    date_yes = date.today() - timedelta(days = 7)
    query = words 
    tweets = tweepy.Cursor(
        api.search_tweets,
        query,
        lang="en",
        since_id=date_since,
        result_type='mixed',
        tweet_mode='extended').items(numtweet)
    list_tweets = [tweet for tweet in tweets]
    i=1
    for tweet in list_tweets:
        username = tweet.user.screen_name
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
            text = text.replace('\n', ' ')
            text = text.replace(',','')
        db['hashtag'].append(words)
        db['username'].append(username)
        db['text'].append(text)
    i = i+1
    return db
if __name__ == '__main__':
    inventory ={}  
    c=[]
    db = {'hashtag': [], 'username':[] , 'text':[], }
    loc = "23424977"
    trends = get_trends(api, loc)
    with open("get_trends.json","w") as fp:
        fp.write(json.dumps(trends, indent=4))
        for i in range(0,10,1):
            if trends[i]['name'] not in c:
                c.append(trends[i]['name'])
    print("top 10 trending hashtags at", loc, ":" ,c)
    date_since = date.today() - timedelta(days = 1)
    for words in c :
        numtweet = 10
        db = scrape(words, date_since, numtweet) 
    df = pd.DataFrame.from_dict(db)
    print(df)
    timestr = date.today().strftime("%Y%m%d")
    fullname = os.path.join("data", timestr+"tweetsfromtrending#s.csv")
    df.to_csv(fullname, index=False, mode="w+", encoding = 'utf-8')
    
         
                  
                
        

