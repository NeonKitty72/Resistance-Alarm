# Copyright 2020 NeonKitty Industries
# JK this is GNU GPL, use as you feel fit to
import json
import sys
from twython import Twython

#CONSTANTS
KEYS_FILEPATH = "secrets/AppKeys.json"
APP_KEY_NAME= "APP_KEY"
APP_SECRET_NAME = "APP_SECRET"

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

#get twitter oauth key
appKey = keysJson[APP_KEY_NAME]
appSecret = keysJson[APP_SECRET_NAME]
twitter = Twython(appKey, appSecret, oauth_version=2)
accessToken = twitter.obtain_access_token()

twitter = Twython(appKey, access_token=accessToken)

#search for fursquared tweets
print(twitter.get_user_timeline(user_id="2960430183"))
