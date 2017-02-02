import twitter
import praw
from time import sleep
import re
import html

def removeURL(status):
    return(re.sub(r"https://t.co\S+", "", status))
        
twitterApi = twitter.Api(consumer_key="CONSUMER_KEY",
                         consumer_secret="CONSUMER_SECRET",
                         access_token_key="ACCESS_TOKEN_KEY",
                         access_token_secret="ACCESS_TOKEN_SECRET")
redditApi = praw.Reddit(client_id='CLIENT_ID',
                        client_secret="CLIENT_SECRET", 
                        password='PASSWORD',
                        user_agent='USER_AGENT',
                        username='USERNAME')

subreddit = redditApi.subreddit("SUBREDDIT")

statuses = twitterApi.GetUserTimeline(screen_name="SCREEN_NAME",
                                      count=1,
                                      exclude_replies=True,
                                      include_rts=False)
oldStatuses = statuses

while (True):
    if (oldStatuses == statuses):
        sleep(60)
        statuses = twitterApi.GetUserTimeline(screen_name="SCREEN_NAME",
                                              count=1,
                                              exclude_replies=True,
                                              include_rts=False)
        continue
    oldStatuses = statuses
    subreddit.submit(title=html.unescape(removeURL(statuses[0].text)), 
                     url="https://twitter.com/SCREEN_NAME/status/" + str(statuses[0].id), 
                     send_replies=False)
    sleep(60)
    statuses = twitterApi.GetUserTimeline(screen_name="SCREEN_NAME",
                                          count=1,
                                          exclude_replies=True,
                                          include_rts=False)

    
