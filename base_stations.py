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

print("[" + datetime.datetime.now().time().isoformat("seconds") + "]" + \
	" twitter client created, entering main loop")

polls = 60 # keeps track of polls per hour
POLLS_PER_HOUR = 60 # how many times to check an hour
while True:
	print("[" + datetime.datetime.now().time().isoformat("seconds") + "]" + \
		" checking status of base stations")

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
	print("[" + datetime.datetime.now().time().isoformat("seconds") + "]" \
		+ " result was " + finder.search(text).group(1))
	timestamp = datetime.datetime.now().time().isoformat("seconds")
	tweet = status + " as of " + timestamp
	try:
		# only tweet "no" if it's been an hour since the last one
		if status == "no" and polls == POLLS_PER_HOUR:
			acct.create_tweet(text=tweet)
			polls = 0
		# if hasn't been hour, increase interval
		elif status == "no":
			polls += 1
		# tweet "YES!" every 10 min if applies, reset intervals if necessary
		elif polls % 10 == 0:
			acct.create_tweet(tweet=text)
			polls = 0
		else:
			polls += 1
		print("[" + datetime.datetime.now().time().isoformat("seconds") + \
			"] status update successful")
	except tweepy.errors.Forbidden:
		acct.create_tweet(text="status unknown as of " + timestamp)
		print("[" + datetime.datetime.now().time().isoformat("seconds") + \
			"] status update failed")
	
	time.sleep(60) # check every minute