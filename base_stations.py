# use date of tweet so that tweet isn't repetitive?
import tweepy # needed for interacting w/ twitter
import urllib.request # used to download website
import re # used to find necessary part of website
import credentials as creds # contains twitter dev acct creds

acct = tweepy.Client(creds.BEARER_TOKEN, creds.CONSUMER_KEY, creds.CONSUMER_SECRET, creds.ACCESS_KEY, creds.ACCESS_SECRET)
try:
	print(acct.create_tweet(text="test tweet #1"))
except tweepy.errors.Forbidden:
	print("tweet failed to send")