# Copyright 2020 NeonKitty Industries
# JK this is GNU GPL, use as you feel fit to
import sys
import json
import threading
from twython import Twython

#CONSTANTS
KEYS_FILEPATH = "secrets/AppKeys.json"
APP_KEY_NAME= "APP_KEY"
APP_SECRET_NAME = "APP_SECRET"
FURSQUARED_USER_ID = "1327655468"

print("----------------------------------------------------------")
print("Resistance Alarm v0.1")
print("Exit with Ctrl+C (or whatever break is on your cmd)")
print("")
print("initalizing...")

#load up app keys
try:
    with open(KEYS_FILEPATH) as f:
        keysJson = json.load(f)
except FileNotFoundError:
    print("ERROR: Key File not found: Did you move it to the secrets folder like the readme said to?")
    sys.exit()

error = False
if keysJson[APP_KEY_NAME] == "<APP_KEY_HERE>":
    print("ERROR: No {} set: update the json file in {}".format(APP_KEY_NAME, KEYS_FILEPATH))
    error = True
if keysJson[APP_SECRET_NAME] == "<APP_SECRET_HERE>":
    print("ERROR: No {} set: update the json file in {}".format(APP_SECRET_NAME, KEYS_FILEPATH))
    error = True
if error:
    sys.exit()

print("loading app keys... good.")

#get twitter oauth key
appKey = keysJson[APP_KEY_NAME]
appSecret = keysJson[APP_SECRET_NAME]
twitter = Twython(appKey, appSecret, oauth_version=2)
accessToken = twitter.obtain_access_token()
print("getting twitter access token... good.")

twitter = Twython(appKey, access_token=accessToken)
appKey = ""
appSecret = ""
accessToken = ""
print("clearing sensitive data... good.")

#search for fursquared tweets
#get the current tweet's id to know when tweets are actually new
maxId = 0
tweets = twitter.get_user_timeline(user_id=FURSQUARED_USER_ID,count=1)
tweet = tweets[0]
maxId = tweet["id"]
print("initializing twitter link... good.")
print("")
print("Currently alerting for tweets/replies/rt's from user ID {}".format(FURSQUARED_USER_ID))
print("last tweet occurred at {}".format(tweet["created_at"]))
print("----------------------------------------------------------")

# ------------------------------
# functions
# ------------------------------
#AAAAAAAAAAAAAAAAAHHHHHHHHHHH
def yell():
    print("NEW TWEET NEW TWEET")

#Every second, fetch the last two tweets. If any of them are new, yell.
def huntForNewTweets():
    global maxId
    newTweet = False
    tweets = twitter.get_user_timeline(user_id=FURSQUARED_USER_ID,count=1,since_id=maxId)
    for tweet in tweets:
        if tweet["id"] > maxId:
            newTweet = True

    if newTweet:
        yell()
        maxId = tweet["id"]
    else:
        print("nothing")

    threading.Timer(1.5, huntForNewTweets).start()




huntForNewTweets()
