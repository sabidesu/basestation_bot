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

print(f"[{datetime.datetime.now().time().isoformat('seconds')}]" + \
	" twitter client created, entering main loop")

polls = 60 # keeps track of polls per hour
POLLS_PER_HOUR = 60 # how many times to check an hour
while True:
	print(f"[{datetime.datetime.now().time().isoformat('seconds')}]" + \
		f" polls = {polls}")
	print(f"[{datetime.datetime.now().time().isoformat('seconds')}]" + \
		" checking status of base stations")

	# parse website for information
	url = "https://store.steampowered.com/valveindex"
	s = urllib.request.urlopen(url)
	text = s.read().decode("utf-8").replace("\r\n", "").replace("\t", "") \
		.replace(" ", "")
	regex = r"\$149.00<\/div><divclass=\"btn_addtocart\"><spanclass=\".*\">" \
		+ "<span>(.*)<\/span>(<\/div>){4,}"
	finder = re.compile(regex)
	if (not finder.search(text).group(1)):
		acct.create_tweet("couldn't get status as of" \
			+ f"{datetime.datetime.now().time().isoformat('seconds')}")
		print(f"[{datetime.datetime.now().time().isoformat('seconds')}]" \
			+ " couldn't get status")

	# generate tweet based on found info
	status = "no" if finder.search(text).group(1) == "OutofStock" else "YES!"
	print(f"[{datetime.datetime.now().time().isoformat('seconds')}]" \
		+ f" result was {finder.search(text).group(1)}")
	timestamp = datetime.datetime.now().time().isoformat("seconds")
	tweet = f"{status} as of {timestamp}"
	try:
		# tweet "YES!" every 10 min if applies, reset intervals if necessary
		if status == "YES!" and polls % 10 == 0:
			acct.create_tweet(tweet=text)
			polls = 1 if polls % POLLS_PER_HOUR == 0 else polls + 1
			print(f"[{datetime.datetime.now().time().isoformat('seconds')}]" \
				+ " status update successful")
		else:
			polls = 1 if polls % POLLS_PER_HOUR == 0 else polls + 1
	except tweepy.errors.Forbidden:
		acct.create_tweet(text=f"status unknown as of {timestamp}")
		print(f"[{datetime.datetime.now().time().isoformat('seconds')}]" \
			+ " status update failed")
	
	time.sleep(3600 / POLLS_PER_HOUR) # check every minute