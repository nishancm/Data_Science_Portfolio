
import sys
from flask import Flask, render_template
from tweetie import *
from colour import Color
from numpy import median
import os

app = Flask(__name__, template_folder=os.path.join(os.getcwd(),'templates'))

def add_color(tweets):
    """
    Provide a color gradient to represent positive (red) to negative (green) sentiment scores
    of tweets
    """
    colors = list(Color("red").range_to(Color("green"), 100))
    for t in tweets:
        score = t['score']
        bin = int(round((score+1)*100/2))
        t['color'] = colors[bin]


@app.route("/<name>")
def tweets(name):
    """
    Display the tweets for a screen name color-coded by sentiment score
    """

    tweets_obj = fetch_tweets(api, name)
    add_color(tweets_obj['tweets'])

    scores = [tweet['score'] for tweet in tweets_obj['tweets']]
    median_score = median(scores)
    urls = [tweet['urls'] for tweet in tweets_obj['tweets']]
    text = [tweet['text'] for tweet in tweets_obj['tweets']]
    colors = [tweet['color'] for tweet in tweets_obj['tweets']]

    return render_template('tweets.html', name = name, scores = scores, median_score = median_score,
                           urls = urls, text = text, colors = colors)


@app.route("/following/<name>")
def following(name):
    """
    Display the list of users followed by a screen name, sorted in
    reverse order by the number of followers of those users.
    """
    follower_obj = fetch_following(api, name)

    names = [follower['name'] for follower in follower_obj]
    screen_names = [follower['screen_name'] for follower in follower_obj]
    imageurls = [follower['image'] for follower in follower_obj]
    no_followers = [follower['followers'] for follower in follower_obj]
    created = [follower['created'] for follower in follower_obj]

    index = sorted(range(len(no_followers)), key=lambda k: no_followers[k], reverse=True)

    names  = [names[i] for i in index]
    screen_names = [screen_names[i] for i in index]
    imageurls = [imageurls[i] for i in index]
    no_followers = [no_followers[i] for i in index]
    created = [created[i] for i in index]

    return render_template('following.html', name = name, names = names,
                           screen_names = screen_names, imageurls = imageurls, no_followers = no_followers,
                           created = created)

i = sys.argv.index('server:app')
twitter_auth_filename = sys.argv[i+1]
api = authenticate(twitter_auth_filename)

#app.run(host='0.0.0.0', port=5000)