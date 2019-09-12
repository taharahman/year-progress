import os
import keys # Python file with Twitter credentials.
import math
import tweepy
import logging
import pendulum

# Calculate the current year progress
dt = pendulum.now()
year_days = 366 if dt.is_leap_year() else 365
passed_days = dt.timetuple().tm_yday
progress = math.floor((passed_days / year_days) * 100)

# Directory of the 'progress.txt' file
directory = os.path.join(sys.path[0], "progress.txt") 

# Initialize Tweepy API
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Reads the last recorded year progress percentage
f = open(directory, "r")
output = f.readline()
f.close()

if progress != int(output):

	# Create progress bar for the tweet
	status = ""
	for x in range(1, 16):
		if progress >= x * (100 / 15):
			status += "▓"
		else:
			status += "░"
	status += " " + str(progress) + "%"

	# Send tweet
	api.update_status(status)

	# Store current year progress in the progress.txt file
	f = open(directory, "w")
	f.write("{}".format(progress))
	f.close()

	# Update profile name and bio when new year starts
	year = str(dt.year)
	if progress == 100:
		api.update_profile(
			name = "Year Progress (" + year + ")", 
			description = "Progress bar of " + year + ".")

	logger.info("Updated: " + progress + "%")