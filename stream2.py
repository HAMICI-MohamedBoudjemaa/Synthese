# code for streaming twitter to a mysql db
# for Python 3 and will support emoji characters (utf8mb4)
# based on the Python 2 code
# supplied by http://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
# for further information on how to use python 3, twitter's api, and
# mysql together visit: http://miningthedetails.com/blog/python/TwitterStreamsPythonMySQL/


from tweepy import Stream
import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
# import mysql.connector
# from mysql.connector import errorcode
import time
import json

# set up connection to db
# make sure to set charset to 'utf8mb4' to support emoji
# cnx = mysql.connector.connect(user='root', password='',
#                               host='localhost',
#                               database='dbname',
#                               charset='utf8mb4')
# cursor = cnx.cursor()

# Twitter consumer key, consumer secret, access token, access secret
ckey = "N4CogFTAcgyNxyuM8jvyrgmH7"
csecret = "UPsquIqzXdjdD6TLRFp9vf3pU0LRfeOanuxpqwO9tJ3emATshO"
atoken = "1070779812330041344-1NgUQko3NliICcTZVKgd9m0yEzDtcY"
asecret = "pdUZKSTVpSMSLwbpOWM09GjP75MtjXShBD7ocjAOAnrr5"


# set up stream listener
class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        # collect all desired data fields
        if 'text' in all_data:
            tweet = all_data["text"]
            created_at = all_data["created_at"]
            retweeted = all_data["retweeted"]
            username = all_data["user"]["screen_name"]
            user_tz = all_data["user"]["time_zone"]
            user_location = all_data["user"]["location"]
            user_coordinates = all_data["coordinates"]

            # if coordinates are not present store blank value
            # otherwise get the coordinates.coordinates value
            if user_coordinates is None:
                final_coordinates = user_coordinates
            else:
                final_coordinates = str(all_data["coordinates"]["coordinates"])

            # # inser values into the db
            # cursor.execute(
            #     "INSERT INTO tableName (created_at, username, tweet, coordinates, userTimeZone, userLocation, retweeted) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            #     (created_at, username, tweet, final_coordinates, user_tz, user_location, retweeted))
            # cnx.commit()

            print((username, tweet))

            return True
        else:
            return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)

last_id = None
result = True
while result:
    result = api.search(q='TPMP', count=100, tweet_mode='extended', max_id=last_id)
    for res in result:
        print(res._json['full_text'])
        print ("----------")
        # we subtract one to not have the same again.
    last_id = result[-1]._json['id'] - 1

# trends1 = api.trends_place(615702)   ### id de Paris
# # from the end of your code
# # trends1 is a list with only one element in it, which is a
# # dict which we'll put in data.
# data = trends1[0]
# # grab the trends
# trends = data['trends']
# # grab the name from each trend
# names = [trend['name'] for trend in trends]
# print(names[0])
# print(names)
#
# # create stream and filter on a searchterm
# twitterStream = Stream(auth, listener())
# twitterStream.filter(track=[names[0]],
#                  languages=["fr"], stall_warnings=True)