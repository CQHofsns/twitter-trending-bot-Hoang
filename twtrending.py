"""
Created on Thu Feb 17 17:35:46 2022

@author: chuqu
"""

#from asyncio.windows_events import NULL
from fileinput import filename
#from msilib.schema import RemoveFile
#from numpy import result_type
#from base64 import encode
#from encodings import utf_8
#from fileinput import filename
import string
import tweepy
import json
import configparser
import pandas as pd
from datetime import date
from datetime import timedelta
import time
import re
import os

#API Keys and Tokens
config = configparser.RawConfigParser()
config.read('key.cfg')
consumer_key = config.get('API','key')
consumer_secret = config.get('API','secret')
access_token = config.get('API','token')
access_token_secret = config.get('API','tokensecret')

#Authorization and Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit= True)
#Get Trends
def get_trends(api,loc):
    #:returns: A dictionary of trending search results
    #Object that has location's latitude and longtitude.
    trends = api.get_place_trends(loc)
    return trends[0]["trends"]
def extract_hashtags(trends):
    """Extracts the hashtags from the trending search results.
    :param trends: A list of trending search results.
    :returns: A lisselft of hashtags.
    """
    hashtags = [trend["name"] for trend in trends if '#' in trend["name"]]
    return hashtags
def get_n_tweets(api, hashtags, n, lang=None):
    for status in tweepy.Cursor(
        api.search_tweets,
        q=hashtags,
        lang=lang
    ).items(n):
        print(f"https://twitter.com/i/web/status/{status.id}")
def printtweetdata(n, ith_tweet):
    print()
    print(f"Username:{ith_tweet[0]}")
    print(f"Tweet Text:{ith_tweet[1]}")
def scrape(query, date_since, numtweet):
    date_today = date.today()
    date_yes = date.today() - timedelta(days = 1)
    query = words + " until:{} since:{}".format(date_today,date_yes)
    tweets = tweepy.Cursor(
        api.search_tweets,
        query,
        lang="en",
        since_id=date_since,
        result_type='popular',
        tweet_mode='extended').items(numtweet)
    list_tweets = [tweet for tweet in tweets]
    #counter to maintain Tweet Count
    i=1
    #iterating over each tweet in the list for extracting information about each tweet
    for tweet in list_tweets:
        username = tweet.user.screen_name
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
            text = text.replace('\n', ' ')
            text = text.replace(',','')
    #appending all the extracted information in the Dictionary
        db['hashtag'].append(words)
        db['username'].append(username)
        db['text'].append(text)
    #Function call to print tweet data on screen
    #printtweetdata(i, ith_tweet)
    i = i+1
    """print("------------------------")
    print(db)
    print("------------------------")"""
    return db
def demoji(text):
    emoji_pattern  = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002500-\U00002BEF"  # chinese char
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                u"\U0001f926-\U0001f937"
                                u"\u2640-\u2642"
                                u"\u200d"
                                u"\u23cf"
                                u"\u23e9"
                                u"\u231a"
                                u"\ufe0f"  # dingbats
                                u"\u3030"
                                "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r'', text)    
if __name__ == '__main__':
    inventory ={}  
    c=[]
    db = {'hashtag': [], 'username':[] , 'text':[], }
    loc = "23424977"
    trends = get_trends(api, loc)
    #trends =extract_hashtags(trends)
    with open("get_trends.json","w") as fp:
        fp.write(json.dumps(trends, indent=4))
        for i in range(0,10,1):
            if trends[i]['name'] not in c:
                c.append(trends[i]['name'])
    print("top 10 trending hashtags at", loc, ":" ,c)
    date_since = date.today() - timedelta(days = 1)
    for words in c :
        #date_since = "20220307"
        numtweet = 10
        db = scrape(words, date_since, numtweet) 
    df = pd.DataFrame.from_dict(db)
    timestr = date_since.strftime("%Y%m%d")
    fullname = os.path.join("data", timestr+"tweetsfromtrending#s.csv")
    #file = open("C:\Users\chuqu\Documents\Internship_project\Twitter_Sentiment_Analysis\thử nghiệm\data")
    df.to_csv(fullname, index=False, mode="w+", encoding = 'utf-8')
    
         
                  
                
        

