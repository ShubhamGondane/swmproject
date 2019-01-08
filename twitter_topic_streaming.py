from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
#import MySQLdb
import time
import json
import tweepy
import sys
import csv
import pickle
import pandas as pd
from geopy.geocoders import Nominatim
import html
import unicodedata
import re

config = {}
exec(open("config.py").read(),config)



#consumer key, consumer secret, access token, access secret.
ckey='5p2WckrbwyLtr7alF5IM3hBEh' 
csecret='WwlYsyZxjJogXliCuuSr2dFUBWMkKfuxAXyg4cwE6yquR0GumP'
atoken='917571341263421440-UlutpHMfww1QdFuJvANfn8rUE26hmKp'  
asecret='fCaM6qhY13gxYIOR6CDVuIhRGzVz3TIcjTP1Lqw7Gvyt9'

twitter_consumer_key = '5p2WckrbwyLtr7alF5IM3hBEh'  
twitter_consumer_secret = 'WwlYsyZxjJogXliCuuSr2dFUBWMkKfuxAXyg4cwE6yquR0GumP'  
twitter_access_token = '917571341263421440-UlutpHMfww1QdFuJvANfn8rUE26hmKp'  
twitter_access_secret = 'fCaM6qhY13gxYIOR6CDVuIhRGzVz3TIcjTP1Lqw7Gvyt9'


csvfile = open('outfile_topic.csv', "w+")
csvwriter = csv.writer(csvfile)
row = [ "user", "text"]
csvwriter.writerow(row)

fp=open("pickled_topics.pickle","rb")
topics = pickle.load(fp)
fp.close() #topic and count tuple

keywords = []
for i in range(len(topics)):
    keywords.append(topics[i][0])

class listener(StreamListener):
    

    def on_data(self, data):
        all_data = json.loads(data)
        if "text" in all_data.keys():
            tweet = all_data["text"]
            text=tweet
            #text = result.text
            #text = text.encode('iso-8859-1', 'replace')
            #text=text.decode("utf-8", "ignore")
            #text = text.encode('ascii', 'replace')
            #text=text.decode("utf-8", "ignore")
            #text=text.encode("windows-1252")
            #text=text.decode("utf-8", "ignore")
            #text=text.decode("cp1252")
            text=unicodedata.normalize('NFKD',text).encode('ascii','ignore')
            text=text.decode("cp1252", "ignore")

            text=html.unescape(text)
            text = re.sub(r'http\S+', " ",text)
            text = re.sub(r'RT @([^\s:]+)', " ",text)
            text = re.sub(r'(?:@[\w_]+)'," ",text)
            
            username = all_data["user"]["screen_name"]
            row = [username, text]
            csvwriter.writerow(row)
            '''
            c.execute("INSERT INTO taula (time, username, tweet) VALUES (%s,%s,%s)",
                (time.time(), username, tweet))


            conn.commit()
            '''
            print(text)
            
            return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track = keywords, languages=['en'])