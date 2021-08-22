import os
import sys
import math
import tweepy
import pendulum

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Calculate the current year progress
dt = pendulum.now("UTC")
year_days = 366 if dt.is_leap_year() else 365
passed_days = dt.timetuple().tm_yday
progress = math.floor((passed_days / year_days) * 100)

# Directory of the 'progress.txt' file
directory = os.path.join(sys.path[0], "progress.txt")

# Read the year progress that was last recoFrded
f = open(directory, "r")
output = f.readline()
f.close()

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

    # Store current year progress in the progress.txt file
    f = open(directory, "w")
    f.write("{}".format(progress))
    f.close()

    # Update profile when new year starts
    if progress == 100:
        year = str(dt.year)
        api.update_profile(
            name="Year Progress (" + year + ")",
            description="Progress bar of " + year + ".")
