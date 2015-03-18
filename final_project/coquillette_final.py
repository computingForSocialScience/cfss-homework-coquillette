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
#getSentiment()


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
#getFreq()


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









"""
import matplotlib.dates as mdates

def showFormattedDateDistribution():
    dates = matplotlib.dates.date2num(Tweet_Time)
    plt.hist(dates, bins=10)
    plt.title('Date Distribution Histogram')
    plt.xlabel('Date of Tweet')
    plt.ylabel('Frequency')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    #plt.plot(x,y)
    plt.gcf().autofmt_xdate()
    plt.grid(True)
    plt.draw
    plt.savefig('updatehistogram.png')
showFormattedDateDistribution()

def showDateDistribution():
    cur.execute('''SELECT created from tweets''')
    timestamp = cur.fetchall()
    print timestamp
    #timelist = [list(i) for i in timestamp]
    #timelist = [(i) for i in timestamp]
    timelist = [str(i) for i in timestamp]
    datelist = []
    for time in timelist:
        date = time.split(' ', 1)[0]
        timecreated = time.split(' ', 1)[1]
        update = date.split("(u'", 1)[1]
        update.replace("'", "")
        datelist.append(update)
        #counts = [count for count, _, _ in retweets]
    print datelist
    #dts = map(datetime.datetime.fromtimestamp,s)
    #fds = dates.date2num(dts)
    #hfmt = dates.DateFormatter('%y/%m/%d')

    plt.hist(datelist, bins=10)
    plt.title('Date Distribution Histogram')
    plt.xlabel('Date of Tweet')
    plt.ylabel('Frequency')
    #plt.show
    plt.grid(True)
    plt.draw
    plt.savefig('datehistogram.png')
showDateDistribution()



def showDateDistribution:
    dateDistribution = []
    timeDistribution = []
    for date in Tweet_created:
        splitdate = Tweet_created
        print splitdate.split(' ')
        date = splitdate[0]
        time = splitdate[1]
        dateDistribution.append(date)
        timeDistribution.append(time)
    plt.hist(dateDistribution, bins=100, color='b')
    plt.title('Date Distribution Histogram')
    plt.xlabel('Date of Tweet')
    plt.ylabel('Frequency')
    plt.show

def showTimeDistribution:
    plt.hist(timeDistribution, bins=100, color='b')
    plt.title('Time Distribution Histogram')
    plt.xlabel('Time of Tweet')
    plt.ylabel('Frequency')
    plt.show

def plotRetweetHistogram():
    #counts = [count for count, _, _ in retweets]
    cur.execute('''SELECT retweetCount from counts''')
    counts = cur.fetchall()
    plt.hist(counts)
    plt.title("Retweets")
    plt.xlabel('Bins (number of times retweeted)')
    plt.ylabel('Number of tweets in bin')
    plt.grid(True)
    plt.draw
    plt.savefig('retweethistogram.png')
plotRetweetHistogram()
"""


"""
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def TweetWordCloud():
    
# Read the whole text.
    #cur.execute('''SELECT tweet from tweets''')
    d = path.dirname(__file__)
    data = ' '.join(Tweet_Corpus)
    f = open('tweets.txt', 'w')
    f.write(data)
    f.close()
    text = open(path.join(d, 'tweets.txt')).read()
    wordcloud = WordCloud(width=1000, height=1000, font_path='/usr/share/fonts/verdana.ttf')
    wordcloud = WordCloud().generate(text)
# Open a plot of the generated image.
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    plt.savefig('wordcloud.png')
TweetWordCloud()


from os import path
from wordcloud import WordCloud, STOPWORDS
from scipy.misc import imread

def TweetWordCloud():
    d = path.dirname(__file__)

    #cur.execute('''SELECT tweet from tweets''')
#cur.execute('''SELECT hashtags from tweets''')
#cur.execute('''SELECT userMentions from tweets''')
    #data = cur.fetchall()
    #text = [count for count, _, _ in data]
    #print data
    text = ' '.join(Tweet_Corpus)
    print text
    twitter_mask = imread(path.join(d, 'twitter_mask.png'))
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=1800, height=1400, mask=twitter_mask, font_path='usr/share/fonts/verdana.ttf')
    wordcloud.generate(text)
    wordcloud.to_file(path.join(d, "masked_wordcloud.png"))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.imshow(twitter_mask, cmap=plt.cm.gray)
    plt.savefig(d, 'twitter_wordcloud_masked.png', dpi=300)
    plt.show()
TweetWordCloud()

cur.close()

"""




"""

from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from scipy.misc import imread

d = path.dirname(__file__)

cur.execute('''SELECT tweet from tweets''')
cur.execute('''SELECT hashtags from tweets''')
cur.execute('''SELECT userMentions from tweets''')
text = cur.fetchall()
twitter_mask = imread(d, 'twitter_mask.png', flatten=True)
wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=1800, height=1400, mask=twitter_mask).generate(text)
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig(d, 'twitter_wordcloud_masked.png', dpi=300)
plt.show()

cur.close()
"""
"""* A measure of word frequency within each of the corpuses (using stopwords 
to eliminate grammatical forms). Previous research indicates that online 
activist efforts generate more engagement (operationalized on social media 
as likes and retweets) when their content uses inclusive language such as 
"we", "us", "our" and when their content contains certain activist-
specific terminology ("protest", "petition", "rally", "activist") (Potts 
et al., 2014). 

* A valuecount for 'imgur', 'bit.ly', or 'http' strings in the tweet corpus.
I hypothesize that tweets that contain a photo or a link to the product will 
be more effective at generating retweets and posts from other users and thus 
will be correlated with overall success of the movement. You're gonna want to pull these outof text-- doesn't seem like they get into url field

* A list containing tuples of usernames, number of tweets from that user in 
the corpus, and the user's number of followers.

* A histogram of times of day/days of the week that tweets in each corpus are 
posted.

Revising: What should it be able to do?
- SELECT * FROM users
- SELECT * from tweets
- wordcloud of other hashtags?
- wordcloud of user_mentions?
- most popular tweets-- graph favorited/retweeted
- most popular users-- graph followers/statuses
- maybe show list of all user_mentions, would be neat if I could pull first image search for each
- histogram of days of week/times of day
- valuecount for urls 
- nltk - how many words do people make with their 140 characters? frequency distribution of words, bigrams/trigrams
- sentiment analysis using vaderSentiment"""

#http://adilmoujahid.com/posts/2014/07/twitter-analytics/
#http://stackoverflow.com/questions/25895321/how-to-extract-hashtags-from-tweepy-using-tweepy-cursor-and-api-search
#https://github.com/amueller/word_cloud
"""Name: Cath0516
Screen-name: 2724Cab
Tweet created: 2015-03-09 15:34:58
Tweet: really @target? why is women's shave gel .27 more? #notbuyingit #target http://t.co/Nr5ldVEmSn
Retweeted: False
Favorited: False
Followers: 19
Statuses: 10
Friends: 94
Location: Cleveland, Ohio
Time-zone: None
Geo: None
Tweet ID: 574956550923681792
Hashtags: [{u'indices': [51, 63], u'text': u'notbuyingit'}, {u'indices': [64, 71], u'text': u'target'}]
User Mentions: [{u'id': 89084561, u'indices': [7, 14], u'id_str': u'89084561', u'screen_name': u'Target', u'name': u'Target'}]
Urls: []"""
