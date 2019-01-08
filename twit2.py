import tweepy
import sys
import csv
import pandas as pd
from geopy.geocoders import Nominatim

config = {}
exec(open("config.py").read(),config)

#Finds latitude and longitude by entering city name
def findLocation():
    geolocator = Nominatim()
    currentLocation = input("Enter the location: ")
    location = geolocator.geocode(currentLocation)
    return(location.latitude, location.longitude)

latitude,longitude = findLocation()

auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
auth.set_access_token(config["access_key"], config["access_secret"])

api = tweepy.API(auth)
last_id = None
max_range = 1
num_results = 50
result_count = 0
last_id = None
radius = 1

query = [status for status in tweepy.Cursor(api.search, q="", geocode="%f,%f,%dkm" % (latitude, longitude, radius), count=100, max_id=None).items()]
csvfile = open('outfile.csv', "w+")
csvwriter = csv.writer(csvfile)

row = [ "user", "text", "latitude", "longitude" ]
csvwriter.writerow(row)

while result_count <  num_results:
    for result in query:
        if result.geo:
            user = result.user.screen_name
            text = result.text
            text = text.encode('ascii', 'replace')
            text=text.decode("utf-8", "ignore")
            #text = text.decode('unicode_escape').encode('ascii','ignore')
            #text = str(text).decode('utf-8')
            current_latitude = result.geo["coordinates"][0]
            current_longitude = result.geo["coordinates"][1]

            row = [ user, text, current_latitude, current_longitude ]
            csvwriter.writerow(row)
            result_count += 1
        last_id = result.id

print ("Got %d results" % result_count)


csvfile.close()

print ("Written to %s" % 'outfile')

tweets_df=pd.read_csv('outfile.csv')
tweet_dict={k: list(v) for k,v in tweets_df.groupby('user')['text']}
#tweet_dict1=list(tweets_df.set_index('user').to_dict().values())
#print(tweet_dict)
