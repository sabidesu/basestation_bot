# use date of tweet so that tweet isn't repetitive?
import tweepy # needed for interacting w/ twitter
import urllib.request # used to download website
import re # used to find necessary part of website
import datetime # used for making tweets unique
import time # used for pausing program
import credentials as creds # contains twitter dev acct creds

# create twitter client
acct = tweepy.Client(creds.BEARER_TOKEN, creds.CONSUMER_KEY, \
	creds.CONSUMER_SECRET, creds.ACCESS_KEY, creds.ACCESS_SECRET)

intervals = 0 # keeps track of how many tweets
while True:
	# parse website for information
	url = "https://store.steampowered.com/valveindex"
	s = urllib.request.urlopen(url)
	text = s.read().decode("utf-8").replace("\r\n", "").replace("\t", "") \
		.replace(" ", "")
	regex = r"\$149.00<\/div><divclass=\"btn_addtocart\"><spanclass=\".*\">" \
		+ "<span>(.*)<\/span>(<\/div>){4,}"
	finder = re.compile(regex)

	# generate tweet based on found info
	status = "no" if finder.search(text).group(1) == "OutofStock" else "YES!"
	timestamp = datetime.datetime.now().time().isoformat("seconds")
	tweet = status + " as of " + timestamp
	try:
		# only tweet "no" if it's been an hour since the last one
		if status == "no" and intervals == 4:
			acct.create_tweet(text=tweet)
			intervals = 0
		# if hasn't been hour, increase interval
		elif status == "no":
			intervals += 1
		# tweet "YES!" whenever applies, reset intervals if necessary
		else:
			acct.create_tweet(tweet=text)
			intervals = 0 if intervals == 4 else intervals + 1
	except tweepy.errors.Forbidden:
		acct.create_tweet(text="status unknown as of " + timestamp)
	
	time.sleep(900) # only tweet at max every 15 minutes