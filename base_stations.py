# use date of tweet so that tweet isn't repetitive?
import tweepy # needed for interacting w/ twitter
import urllib.request # used to download website
import re # used to find necessary part of website
import credentials as creds # contains twitter dev acct creds

# create twitter client
acct = tweepy.Client(creds.BEARER_TOKEN, creds.CONSUMER_KEY, \
	creds.CONSUMER_SECRET, creds.ACCESS_KEY, creds.ACCESS_SECRET)

# parse website for information
url = "https://store.steampowered.com/valveindex"
s = urllib.request.urlopen(url)
text = s.read().decode("utf-8").replace("\r\n", "").replace("\t", "") \
	.replace(" ", "")
regex = r"\$149.00<\/div><divclass=\"btn_addtocart\"><spanclass=\".*\">" \
	+ "<span>(.*)<\/span>(<\/div>){4,}"
finder = re.compile(regex)

# generate tweet based on information
status = "no" if finder.search(text).group(1) == "OutofStock" else "YES!"
try:
	acct.create_tweet(text="no")
except tweepy.errors.Forbidden:
	acct.create_tweet(text="status unknown")