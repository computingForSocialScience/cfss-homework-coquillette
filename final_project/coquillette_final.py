import tweepy
import pymysql
from flask import Flask, render_template, request, redirect, url_for
from Access import API_Key, API_Secret, Access_Token, Access_Secret
import sys
import os
app = Flask(__name__)
dbname="tweets"
host="localhost"
user="root"
passwd="AN1ceSl1ceofPy"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')
cur = db.cursor()
maketableusers = """CREATE TABLE IF NOT EXISTS users (name VARCHAR(255), followers INTEGER, statuses INTEGER, friendsCount INTEGER, location VARCHAR(255));""" 
maketabletweets = """CREATE TABLE IF NOT EXISTS tweets (tweet VARCHAR (255), created VARCHAR(255), retweeted VARCHAR(255), favorited VARCHAR(255), tweetID VARCHAR(500), hashtags VARCHAR(500), userMentions VARCHAR(500), urls VARCHAR(500));"""
maketablecounts = """CREATE TABLE IF NOT EXISTS counts (name VARCHAR(255), tweet VARCHAR(255), retweetCount INTEGER, favoriteCount INTEGER);"""
maketablesentiment = """CREATE TABLE IF NOT EXISTS sentiment (tweet_text VARCHAR(255), sentiment VARCHAR(255));"""
maketablenltkdb = """CREATE TABLE IF NOT EXISTS nltkdb (term VARCHAR(255), frequency VARCHAR(255));"""
cur.execute(maketableusers)
cur.execute(maketabletweets)
cur.execute(maketablecounts)
cur.execute(maketablesentiment)
cur.execute(maketablenltkdb)

ckey = API_Key
csecret = API_Secret 
atoken = Access_Token 
asecret = Access_Secret 

#def getTweets():
OAUTH_KEYS = {'consumer_key':ckey, 'consumer_secret':csecret,
    'access_token_key':atoken, 'access_token_secret':asecret}
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth)

Tweet_Corpus = []
Tweet_Time = []
for tweet in tweepy.Cursor(api.search, q=('#notbuyingit')).items(20):

    Name = tweet.author.name.encode('utf8')
    Screen_name = tweet.author.screen_name.encode('utf8')
    Tweet_created = tweet.created_at
    Tweet_text = tweet.text.encode('utf8')    
    Retweeted = tweet.retweeted
    Retweet_count = tweet.retweet_count
    Favorite_count = tweet.favorite_count
    Favorited = tweet.favorited
    Followers = tweet.user.followers_count
    Statuses = tweet.user.statuses_count
    Friends = tweet.user.friends_count
    Location = tweet.user.location.encode('utf8')
    Tweet_ID = tweet.id_str
    Hashtags = tweet.entities.get('hashtags')
    Hashtag_List = []        
    for i in range(len(Hashtags)):
        hashtag_text = Hashtags[i]['text'].encode('utf8')
        Hashtag_List.append(hashtag_text)
    midway_list = ' '.join(Hashtag_List)
    Hashtag_List = midway_list    
    User_Mentions = []
    User_Mention = tweet.entities.get('user_mentions')
    for i in range(len(User_Mentions)):
        user_mentions_names = User_Mention[i]['name'].encode('utf8')    
        User_Mentions.append(user_mentions_names)
    if User_Mentions == []:
        User_Mentions = 'N/A'
    URLs = tweet.entities.get('urls')
    for entry in URLs:
        url_text = URLs = URLs[0]['url']
        URLs = url_text
    if URLs == []:
        URLs = 'N/A'
    #URLs = url_text['url']    
    '''print Tweet_text
    print Tweet_created
    print Tweet_ID
    print Retweeted
    print Favorited
    print Hashtag_List
    print User_Mentions
    print URLs'''
    Tweet_Corpus.append(Tweet_text)
    Tweet_Time.append(Tweet_created)
    #user_sql = "INSERT INTO users (name, followers, statuses, friendsCount, location) VALUES (%s, %s, %s, %s, %s)" #% (Name, Followers, Statuses, Friends, Location)
    #tweet_sql = "INSERT INTO tweets (tweet, created, retweeted, favorited, tweetID, hashtags, userMentions, urls) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" #% (Tweet_text, Tweet_created, Retweeted, Favorited, Tweet_ID, Hashtag_List, User_Mentions, URLs)
    cur.execute("INSERT INTO users (name, followers, statuses, friendsCount, location) VALUES (%s, %s, %s, %s, %s)", (Name, Followers, Statuses, Friends, Location))
    db.commit()
    cur.execute("INSERT INTO tweets (tweet, created, retweeted, favorited, tweetID, hashtags, userMentions, urls) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (Tweet_text, Tweet_created, Retweeted, Favorited, Tweet_ID, Hashtag_List, User_Mentions, URLs))
    db.commit()
    cur.execute("INSERT INTO counts (name, tweet, retweetCount, favoriteCount) VALUES (%s, %s, %s, %s)", (Name, Tweet_text, Retweet_count, Favorite_count))


def findPowerUsers():
    cur.execute('''SELECT name, followers from users ORDER BY followers DESC''')
    powerUsers = cur.fetchall()
    return powerUsers

def findProlificUsers():
    cur.execute('''SELECT name, statuses from users ORDER BY statuses DESC''')
    prolificUsers = cur.fetchall()
    return prolificUsers

def findPopularTweets():
    cur.execute('''SELECT * from counts ORDER BY retweetCount DESC''')
    popularTweets = cur.fetchall()
    return popularTweets

import tempfile
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import dates
import numpy as np
import datetime

def plotTweetsvFollowers():
    cur.execute('''SELECT statuses from users''')
    chartstatus = cur.fetchall()
    cur.execute('''SELECT followers from users''')
    chartfollowers = cur.fetchall()
    plt.title("User Stats by Number of Statuses and Number of Followers")
    plt.plot_date(x=chartstatus, y=chartfollowers)
    plt.xlabel("Number of Tweets")
    plt.ylabel("Number of Followers")
    #plt.show()
    plt.grid(True)
    plt.draw
    f = tempfile.NamedTemporaryFile(dir='static/temp',suffix='.png',delete=False)
    plt.savefig(f)
    f.close()
    plotPng = f.name.split('/')[-1]
    #plt.savefig('histogram.png')
#plotTweetsvFollowers()

import pandas as pd

#http://stackoverflow.com/questions/1574088/plotting-time-in-python-with-matplotlib 
#http://matplotlib.org/examples/pylab_examples/date_demo_convert.html

import matplotlib.dates as mdates
def showDateDistribution():
    dates = matplotlib.dates.date2num(Tweet_Time) 
    plt.hist(dates, bins=10)
    #matplotlib.pyplot.plot_date(dates, values)
    plt.title('Date Distribution Histogram')
    plt.xlabel('Date of Tweet')
    plt.ylabel('Frequency')
    #labels = dates.num2date
    #plt.show
    plt.grid(True)
    plt.draw
    f = tempfile.NamedTemporaryFile(dir='static/temp',suffix='.png',delete=False)
    plt.savefig(f)
    f.close()
    plotPng = f.name.split('/')[-1]
    #plt.savefig('datehistogram.png')
#showDateDistribution()


from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

def getSentiment():
    for Tweet_text in Tweet_Corpus:
        vs = str(vaderSentiment(Tweet_text))
        #print Tweet_text
        #print str(vs)
        cur.execute("INSERT INTO sentiment (tweet_text, sentiment) VALUES (%s, %s)", (Tweet_text, vs))
    cur.fetchall()
    db.commit()
getSentiment()


import nltk
def getFreq():
    tokens = nltk.word_tokenize(str(Tweet_Corpus))
    text = nltk.Text(tokens)
    fdist = nltk.FreqDist(text)
    stopwords = nltk.corpus.stopwords.words('english')
    text2 = [w for w in text if w.lower() not in stopwords]
    search_terms = ['http', 't.co', 'imgur', 'bit.ly', 'tinyurl', 'twitpic']
    for term in search_terms:
        freq = fdist[term]
        cur.execute("INSERT INTO nltkdb (term, frequency) VALUES (%s, %s)", (term, freq))
    cur.fetchall()
    db.commit()
getFreq()


from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from scipy.misc import imread

def makeWordCloud():
    d = path.dirname(__file__)
    tokens = nltk.word_tokenize(str(Tweet_Corpus))
    text2 = nltk.Text(tokens)
    text1 = [w for w in text2 if w.lower() not in STOPWORDS]
    text = ' '.join(text1)
    print type(text)
    twitter_mask = imread(path.join(d, 'twitter_mask.png'), flatten=True)
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=1800, height=1400, mask=twitter_mask, font_path='Verdana.ttf')
    wordcloud.generate(text)
    plt.title('Twitter Word Cloud')
    plt.imshow(wordcloud)
    plt.axis("off")
    #plt.savefig('twitter_wordcloud_masked.png')
    f = tempfile.NamedTemporaryFile(dir='static/temp',suffix='.png',delete=False)
    plt.savefig(f)
    f.close()
    plotPng = f.name.split('/')[-1]
    #plt.savefig((d, 'twitter_wordcloud_masked.png'), dpi=300)
    plt.show()
#makeWordCloud()


@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/users/')
def make_users_resp():
    cur = db.cursor()
    get_users = """SELECT * FROM users;"""
    cur.execute(get_users)
    users = cur.fetchall()
    return render_template('users.html',users=users)

@app.route('/powerusers/')
def make_powerusers_resp():
    cur = db.cursor()
    cur.execute('''SELECT name, followers from users ORDER BY followers DESC''')
    users = cur.fetchall()
    return render_template('powerusers.html',users=users)

@app.route('/prolificusers/')
def make_polificusers_resp():
    cur = db.cursor()
    cur.execute('''SELECT name, statuses from users ORDER BY statuses DESC''')
    users = cur.fetchall()
    return render_template('prolificusers.html',users=users)

@app.route('/followershistogram/')
def display_followershistogram():
    #print "display_followershistogram() called"
    #sys.stdout.flush()
    cur.execute('''SELECT statuses from users''')
    chartstatus = cur.fetchall()
    cur.execute('''SELECT followers from users''')
    chartfollowers = cur.fetchall()
    plt.title("User Stats by Number of Statuses and Number of Followers")
    plt.plot_date(x=chartstatus, y=chartfollowers)
    plt.xlabel("Number of Tweets")
    plt.ylabel("Number of Followers")
    #plt.show()
    plt.grid(True)
    #plt.draw()
    f = tempfile.NamedTemporaryFile(dir='static/temp',suffix='.png',delete=False)
    plt.savefig(f)
    f.close()
    #plotPng = f.name.split('/')[-1]
    plotPng = os.path.basename(f.name)  
    #print "f.name is ", f.name
    #print "plotPng is", plotPng
    #sys.stdout.flush()
    return(render_template('figures.html', plotPng=plotPng))

@app.route('/datehistogram/') 
def display_datehistogram():
    dates = matplotlib.dates.date2num(Tweet_Time) 
    plt.hist(dates, bins=10)
    #matplotlib.pyplot.plot_date(dates, values)
    plt.title('Date Distribution Histogram')
    plt.xlabel('Date of Tweet')
    plt.ylabel('Frequency')
    #labels = dates.num2date
    #plt.show
    plt.grid(True)
    #plt.draw
    f = tempfile.NamedTemporaryFile(dir='static/temp',suffix='.png',delete=False)
    plt.savefig(f)
    f.close()
    plotPng = os.path.basename(f.name)
    #plotPng = f.name.split('/')[-1]
    #plt.savefig('datehistogram.png')    
    return(render_template('figures.html', plotPng=plotPng))

@app.route('/wordcloud/') 
def make_wordcloud_resp():
    d = path.dirname(__file__)
    tokens = nltk.word_tokenize(str(Tweet_Corpus))
    text2 = nltk.Text(tokens)
    text1 = [w for w in text2 if w.lower() not in STOPWORDS]
    text = ' '.join(text1)
    #print type(text)
    twitter_mask = imread(path.join(d, 'twitter_mask.png'), flatten=True)
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=1800, height=1400, mask=twitter_mask, font_path='Verdana.ttf')
    wordcloud.generate(text)
    plt.title('Twitter Word Cloud')
    plt.imshow(wordcloud)
    plt.axis("off")
    #plt.savefig('twitter_wordcloud_masked.png')
    f = tempfile.NamedTemporaryFile(dir='static/temp',suffix='.png',delete=False)
    plt.savefig(f)
    f.close()
    plotPng = os.path.basename(f.name)
    #plotPng = f.name.split('/')[-1]
    #plt.savefig((d, 'twitter_wordcloud_masked.png'), dpi=300)
    #plt.show()
    return(render_template('figures.html', plotPng=plotPng))

@app.route('/tweets/')
def make_tweets_resp():
    cur = db.cursor()
    get_tweetdb = """SELECT * FROM tweets;"""
    cur.execute(get_tweetdb)
    tweets = cur.fetchall()
    return render_template('tweets.html',tweets=tweets)

@app.route('/sentiment/')
def make_sentiment_resp():
    cur = db.cursor()
    get_sentimentdb = """SELECT * FROM sentiment;"""
    cur.execute(get_sentimentdb)
    sentiment = cur.fetchall()
    return render_template('sentiment.html', sentiment=sentiment)

@app.route('/nltk/')
def make_nltk_resp():
    cur = db.cursor()
    get_NLTKdb = """SELECT * FROM nltkdb;"""
    cur.execute(get_NLTKdb)
    nltkdb = cur.fetchall()
    return render_template('frequency.html', nltkdb=nltkdb)


if __name__ == '__main__':
    app.debug=True
    app.run()