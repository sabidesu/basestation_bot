# use date of tweet so that tweet isn't repetitive?
import tweepy # needed for interacting w/ twitter
import urllib.request # used to download website
import re # used to find necessary part of website
import datetime # used for making tweets unique
import time # used for pausing program
import credentials as creds # contains twitter dev acct creds

# helper function for grabbing time
def current_time():
	return datetime.datetime.now().time().isoformat("seconds")

# function for printing and writing the status to txt file
def write_status(status):
	print(status)
	f = open("bot_status.txt", "a") # create file for bot status
	f.write(status)
	f.close()

# create twitter client
acct = tweepy.Client(creds.BEARER_TOKEN, creds.CONSUMER_KEY, \
	creds.CONSUMER_SECRET, creds.ACCESS_KEY, creds.ACCESS_SECRET)

write_status(f"[{current_time()}] twitter client created, entering main loop")

polls = 60 # keeps track of polls per hour
POLLS_PER_HOUR = 60 # how many times to check an hour
while True:
	print(f"[{current_time()}] polls = {polls}")
	print(f"[{current_time()}] checking status of base stations")

	try:
		# parse website for information
		url = "https://store.steampowered.com/valveindex"
		s = urllib.request.urlopen(url)
		text = s.read().decode("utf-8").replace("\r\n", "").replace("\t", "") \
			.replace(" ", "")
		regex = r"\$149.00<\/div><divclass=\"btn_addtocart\"><spanclass=\".*" \
			+ r"\"><span>(.*)<\/span>(<\/div>){4,}"
		finder = re.compile(regex)
		if (not finder.search(text).group(1)):
			write_status(f"[{current_time()}] WARNING: couldn't get status")

		# generate tweet based on found info
		status = "no" if finder.search(text).group(1) == "OutofStock" else "YES!"
		print(f"[{current_time()}] result was {finder.search(text).group(1)}")
		timestamp = current_time()
		tweet = f"{status} as of {timestamp}"

		# tweet "YES!" every 10 min if applies, reset intervals if necessary
		if status == "YES!" and polls % 10 == 0:
			acct.create_tweet(tweet=text)
			print(f"[{current_time()}] status update successful")
	# if unable to parse website for some reason, log error and wait
	except urllib.error.URLError as e:
		write_status(f"[{current_time()}] ERROR: {e}") 
	except urllib.error.HTTPError as e:
		write_status(f"[{current_time()}] ERROR: {e}") 
	except tweepy.errors.Forbidden as e:
		write_status(f"[{current_time()}] ERROR: couldn't send tweet, {e}")
	except e:
		write_status(f"[{current_time()}] ERROR: another error occurred, {e}")
	
	polls = 1 if polls % POLLS_PER_HOUR == 0 else polls + 1
	time.sleep(3600 / POLLS_PER_HOUR) # check every minute