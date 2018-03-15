import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load file containing twitter api keys/tokens 
    """
    with open(filename) as f:
        items = f.readline().strip().split(',')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    values = loadkeys(twitter_auth_filename)

    auth = tweepy.OAuthHandler(values[0],values[1])
    auth.set_access_token(values[2], values[3])

    return tweepy.API(auth)


def fetch_tweets(api, name):
    """
    Given a screen name obtain 100 most recent tweets for the user. Then use 
    vaderSentiment library to determine sentiment score of each tweet
    """

    top_100 = [tweet for tweet in tweepy.Cursor(api.user_timeline, id = name).items(100)]
    vader_obj = SentimentIntensityAnalyzer()
    tweets_list = []

    for twt in top_100:
        tweet = dict()
        tweet['id'] = twt.id
        tweet['created'] = (twt.created_at).date()
        tweet['retweeted'] = twt.retweet_count
        tweet['text'] = (twt.text).replace('\n', ' ')
        tweet['hashtags'] = [item['text'] for item in twt.entities['hashtags']]
        tweet['urls'] = [item['expanded_url'] for item in twt.entities['urls']]
        tweet['mentions'] = [item['screen_name'] for item in twt.entities['user_mentions']]
        tweet['score'] = vader_obj.polarity_scores((twt.text).replace('\n', ' '))['compound']

        tweets_list.append(tweet)

    return {'user':name, 'count':len(top_100), 'tweets':tweets_list}


def fetch_following(api,name):
    """
    Given a screen name obtain list followers of the user with their user info
    """

    friends = [fr for fr in tweepy.Cursor(api.friends_ids, id = name).items()]
    friends_list = []

    for frd in friends:
        friend = {}
        user = api.get_user(frd)

        friend['name'] = user.name
        friend['screen_name'] = user.screen_name
        friend['followers'] = user.followers_count
        friend['created'] = (user.created_at).date()
        friend['image'] = user.profile_image_url

        friends_list.append(friend)

    return friends_list


