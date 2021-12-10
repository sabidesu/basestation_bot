import tweepy # needed for interacting w/ twitter
import urllib.request # used to download website
import re # used to find necessary part of website

CONSUMER_KEY = "Ph2AZPPaiz37s2zZINPH8SWt6"
CONSUMER_SECRET = "GHdlpOjp2dZ7qAu7GTgQ3gLokXinAUsd6z7NblbGDBLSSQQHcX"
ACCESS_KEY = "1469102662775971846-T2U0IjlcAyQHH7d2zr9o3ol1lvPwsj"
ACCESS_SECRET = "VlAKs962TaoYaSE0WRcHJwp9Vsfwydq0MkIJ937MtZrJ2"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)