import json

import tweepy
from retrying import retry
from tweepy import OAuthHandler

from Python.connnexionMongo import tweets, events
from Python.functionUtile import clean_text
from Python.gestion_logging import log_message

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
            tweet_id = data_json['id_str']
            id_user = data_json['user']['id']
            username = clean_text(data_json['user']['name'])
            screen_name = clean_text(data_json['user']['screen_name'])
            followers = data_json['user']['followers_count']
            description = clean_text(data_json['user']['description'])
            tweet_text = clean_text(data_json['full_text'])
            hashtags = data_json['entities']['hashtags']
            retweet_count = data_json['retweet_count']
            userLocation = data_json['user']['location']
            created_at = data_json['created_at']
            #created_at = datetime.datetime.strptime(str(created_at), '%Y-%m-%d %H:%M:%S')
            data = {
                    'tendance': tendance,
                    'tweet_id':tweet_id,
                    'id_user': id_user,
                    'username': username,
                    'screen_name': screen_name,
                    'followers': followers,
                    'description': description,
                    'tweet_text': tweet_text,
                    'hashtags': hashtags,
                    'userLocation': userLocation,
                    'retweet_count': retweet_count,
                    'created': created_at
                    }
            log_message(data, 'info')
            data_array.append(data)
    return data_array


"""
Enreistre les données dans la base mongo
"""
def saveCollectionMongo(data):
    tweets.insert_many(data)

def collect_tweet():
    log_message(getTrend(), 'warn')
    tr = getTrend()
    print(len(tr))
    for trend in getTrend():
        data = getElementTweet(trend)
        saveCollectionMongo(data)

        event = {'id':trend, 'description':'', 'lieu': '', 'date': '', 'status':False}
        events.save(event)



if __name__ == '__main__':
    collect_tweet()
