import twitter
import praw
from time import sleep
import re
import HTMLParser
import os
from os.path import join, dirname
from dotenv import load_dotenv
import threading

load_dotenv(join(dirname(__file__), '.env'))

def setInterval(func, sec):
    def funcWrapper():
        setInterval(func, sec) 
        func()  
    t = threading.Timer(sec, funcWrapper)
    t.start()
    return t

def removeURL(status):
    return(re.sub(r"https://t.co\S+", "", status))

try:
  twitterApi = twitter.Api(
    consumer_key=os.environ['CONSUMER_KEY'],
    consumer_secret=os.environ['CONSUMER_SECRET'],
    access_token_key=os.environ['ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['ACCESS_TOKEN_SECRET']
  )
  reddit = praw.Reddit(
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'], 
    password=os.environ['PASSWORD'],
    user_agent='twitter-to-reddit by /u/twitterToRedditBot',
    username=os.environ['USERNAME']
  )
except KeyError:
  print('Error! Please include the relevant authentication as environment variables')
  exit()
  
account = raw_input('Hi! What account would you like to monitor?\n')
subreddit = raw_input('What subreddit would you like to post to?\n')

print('\nMonitoring: @' + account)
print('Posting to: r/' + subreddit + '\n')

tweets = []

def checkTweets():
  global tweets

  print('Checking for new tweets...')
  newTweets = twitterApi.GetUserTimeline(
    screen_name=account,
    count=5,
    exclude_replies=True,
    include_rts=False
  )
  
  if (newTweets != tweets):
    tweets = newTweets
    reddit.subreddit(subreddit).submit(
      title=HTMLParser.HTMLParser().unescape(removeURL(tweets[0].text)),
      url='https://twitter.com/' + account + '/status/' + str(tweets[0].id),
      send_replies=False
    )
    print('New tweet! Posted to r/' + subreddit + '\n')

setInterval(checkTweets, 300)  
