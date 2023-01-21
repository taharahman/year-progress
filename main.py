import os
import sys
import math
import time
import tweepy

from datetime import datetime

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

os.environ["TZ"] = "UTC"
time.tzset()

# Calculate the current year progress
now = datetime.now()
start = datetime(now.year, 1, 1)
end = datetime(now.year, 12, 31, 23, 59)
progress = math.floor(((now - start) / (end - start)) * 100)

# Directory of 'progress.txt' file
directory = os.path.join(sys.path[0], "progress.txt")

# Read the last recorded year progress
with open(directory, "r") as f:
    output = f.readline()

if progress != int(output):
    # Initialize & authenticate Tweepy
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Create progress bar
    status = ""
    for x in range(1, 16):
        if progress >= x * (100 / 15):
            status += "▓"
        else:
            status += "░"
    status += " " + str(progress) + "%"

    # Push tweet
    api.update_status(status)

    # Store current progress in progress.txt
    with open(directory, "w") as f:
        f.write("{}".format(progress))

    # Update profile when new year starts
    if progress == 100:
        year = str(now.year + 1)
        api.update_profile(
            name="Year Progress (" + year + ")",
            description="Progress bar of " + year + ".")
