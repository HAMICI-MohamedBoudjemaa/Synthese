import datetime
import json

import tweepy
from retrying import retry
from tweepy import OAuthHandler

from connnexionMongo import *
from functionUtile import clean_text
from gestion_logging import log_message
from requeteMongo import *

# Twitter consumer key, consumer secret, access token, access secret
ckey = "N4CogFTAcgyNxyuM8jvyrgmH7"
csecret = "UPsquIqzXdjdD6TLRFp9vf3pU0LRfeOanuxpqwO9tJ3emATshO"
atoken = "1070779812330041344-1NgUQko3NliICcTZVKgd9m0yEzDtcY"
asecret = "pdUZKSTVpSMSLwbpOWM09GjP75MtjXShBD7ocjAOAnrr5"

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

"""
Recuperer les tendances 
"""
def getTrend():
    try:
        trends1 = api.trends_place(615702)  ### id de Paris
        data = trends1[0]
        trends = data['trends']
        names = [trend['name'] for trend in trends]
    except (KeyboardInterrupt, SystemExit):
        log_message('Erreur recupération des tendances ', 'error')
        raise
    return names
"""
recuperer les elements du tweets
"""
@retry
def getElementTweet(trend):
    #-filter:retweets : supprimer les retweets
    #new_search = trend + '-filter:retweets',
    data_array = []
    for page in tweepy.Cursor(api.search, q=trend + ' -filter:retweets', count=100, tweet_mode='extended',lang="fr").pages(10):
        for res in page:
            json_str = json.dumps(res._json)
            data_json = json.loads(json_str)
            tendance = trend

            #Tweet info
            tweet_id = data_json['id_str']
            tweet_text = clean_text(data_json['full_text'])
            hashtags = data_json['entities']['hashtags']
            retweet_count = data_json['retweet_count']
            created_at = data_json['created_at']
            favorite_count = data_json['favorite_count']  # like tweet
            retweeted = data_json['retweeted']

            #Info user
            user_id = data_json['user']['id']
            username = clean_text(data_json['user']['name'])
            screen_name = clean_text(data_json['user']['screen_name'])
            followers = data_json['user']['followers_count']
            description = data_json['user']['description']
            userLocation = data_json['user']['location']

            created = datetime.datetime.strptime(str(created_at), '%a %b %d %H:%M:%S %z %Y')

            data = {
                    'tendance': tendance,
                    'tweet_id':tweet_id,
                    'user_id': user_id,
                    'username': username,
                    'screen_name': screen_name,
                    'followers': followers,
                    'description': description,
                    'tweet_text': tweet_text,
                    'hashtags': hashtags,
                    'userLocation': userLocation,
                    'retweet_count': retweet_count,
                    'favorite_count':favorite_count,
                    'retweeted':retweeted,
                    'created': created
                    }
            #log_message(data, 'info')
            if findIfTweetIdExist(tweet_id) > 0:
                log_message(data,"warn")
                updateTweets(tweet_id,followers, retweet_count, favorite_count)
            else:
                log_message(data, 'info')
                data_array.append(data)
    return data_array


"""
Enreistre les données dans la base mongo
"""
def saveCollectionMongo(data):
    tweets.insert_many(data)

def collect_tweet():
    #log_message(getTrend(), 'warn')
    tr = getTrend()
    tendances = getAllTrend() + getTrend()
    for trend in tendances:
        data = getElementTweet(trend)
        if len(data) != 0:
            saveCollectionMongo(data)
            if findIfEventExist(trend) > 0:
                log_message("Cet evenement est déjà en base", "error")
            else:
                event = {'tendance':trend, 'description':'', 'lieu': '', 'date': '', 'status':False, 'flux_rss':'', 'tweets_representatifs':''}
                events.save(event)
        else:
            log_message("[***************tweet déjà existant]***************", "error")


if __name__ == '__main__':
    collect_tweet()

