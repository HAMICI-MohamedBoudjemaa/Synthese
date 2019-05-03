# code for streaming twitter to a mongo db
# for Python 3 and will support emoji characters (utf8mb4)
# based on the Python 2 code
# supplied by http://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
# for further information on how to use python 3, twitter's api, and


from connnexionMongo import collection
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import datetime

import json

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
            #tweet_id = all_data['id_str']  # The Tweet ID from Twitter in string format
            tweet = all_data["text"]
            created_at = all_data["created_at"]
            retweeted = all_data["retweeted"]
            username = all_data["user"]["screen_name"]
            user_tz = all_data["user"]["time_zone"]
            user_location = all_data["user"]["location"]
            user_coordinates = all_data["coordinates"]
            followers = all_data['user']['followers_count']  # The number of followers the Tweet author has
            hashtags = all_data['entities']['hashtags']  # Any hashtags used in the Tweet

            # Convert the timestamp string given by Twitter to a date object called "created". This is more easily manipulated in MongoDB.
            created = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')

            # if coordinates are not present store blank value
            # otherwise get the coordinates.coordinates value
            if user_coordinates is None:
                final_coordinates = user_coordinates
            else:
                final_coordinates = str(all_data["coordinates"]["coordinates"])

            #created = datetime.datetime.strptime(created_at)
            tweetts = {'username': username, 'followers': followers, 'tweet': tweet,
                       'hashtags': hashtags, 'userTimeZone':user_tz, 'userLocation':user_location, 'retweeted':retweeted, 'created':created}
            print((tweetts))
            collection.save(tweetts);
            return True
        else:
            return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

# create stream and filter on a searchterm
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["booba"],languages=["fr"], stall_warnings=True)