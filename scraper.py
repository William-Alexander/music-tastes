import sys
import urllib2
import requests
import re
from bs4 import BeautifulSoup
import time
from useful_funcs import strip_chars

'''
Should grab every album from the Needle Drop site and 
associate it with a rating like "my_album - 5"
'''
def scrape_needledrop():

	site_prefix = "http://www.theneedledrop.com"
	all_entries = []
	file_name = "needledrop.txt"
	f = open(file_name, 'w')

	# Range of potential ratings
	for i in xrange(0, 11):
		def init_start_url(rating):
			return ("http://www.theneedledrop.com/articles/?tag=" + 
					str(rating) + "%2F10")

		start_url = init_start_url(i)

		url = start_url
		last_page = False

		while not last_page:
			r = requests.get(url)
			soup = BeautifulSoup(r.text, "html.parser")

			# Check to see if we've been sending too many requests
			# If so, just wait a second and try again! :)
			if soup.title.string == "429 Too Many Requests":
				time.sleep(1)
				continue

			page_entries = soup.find_all("h1", class_="entry-title")

			for album in page_entries:
				# So we want to get rid of the artist name, assuming
				# that album names are pretty unique.
				txt_entry = album.a.get_text()
				txt_entry = txt_entry.split("- ", 1)[1]	
				txt_entry += " - " + str(i)
				print txt_entry
				f.write((txt_entry.encode('ascii', 'ignore')) + "\n")

			older = soup.find(class_="older")

			if older is not None and older.string:
				url = site_prefix + older.a["href"]
				time.sleep(0.5) 
			else:
				last_page = True

	f.close()
'''
This one is different from above: Needle Drop is used as 
reference, so only albums present there will be looked for
on other sites.

This function will simply take an album and return the
rating!

We have to use urllib2 here because Pitchfork kept 403'ing
me when I didn't have a lil message to accompany it.
'''
def scrape_pitchfork(album):

	# Let's be courteous :)
	time.sleep(2)

	def fix_album(album):
		album = strip_chars(album)
		return album.replace(" ", "%20")

	# Step 1: Look for the review using the search function.
	base_url = "http://pitchfork.com"
	url = base_url + "/search/?query="  + fix_album(album) 
	hdr = {'User-Agent': 'Hi Pitchfork, sorry about all the requests, I\'ll be done asap! -Will :)'}
	req = urllib2.Request(url, headers=hdr)
	html = urllib2.urlopen(req).read()
	soup = BeautifulSoup(html, "html.parser")

	# Step 2: grab the correct one, and go to that page!
	reviews = soup.find_all("div", class_="review")

	if len(reviews) <= 0:
		return -1
	else:
		# Shit, I need to grab the correct one. The first isn't
		# always right. Basically I'm going to strip all non-char
		# characters except for spaces, which (judging by my limited
		# searching on Pitchfork) will mostly work! :)

		# Initializing it for giggles.
		big_ol_div = ""

		# Let's use enumerate b/c I need to know where in the array it is
		for review in reviews:
			pitchfork_name = review.find(class_="title").string.lower()
			needledrop_name = album.lower()
			if strip_chars(pitchfork_name) == strip_chars(needledrop_name):
				big_ol_div = review
		if big_ol_div is "":
			#big_ol_div = reviews[0]

			# I prefer to get less data points that are more likely to be
			# correct, so let's be careful yah? :)
			return -1
		relative_url = big_ol_div.find(class_="album-link")["href"]

		url2 = base_url + relative_url
		req = urllib2.Request(url2, headers=hdr)
		html = urllib2.urlopen(req).read()
		soup = BeautifulSoup(html, "html.parser")

		# Step 3: Grab dat score
		score = soup.find(class_="score").string
		return float(score)


'''
# Let's get a list of the Needle Drop albums
with open("needledrop.txt") as f:
	content = f.readlines()
content = [x.strip("\n") for x in content]
content = [x.split(" - ")[0] for x in content]

# Now, let's get all the album reviews we can, and write them
# to the pitchfork.txt file.

with open("pitchfork.txt", 'w') as f:
	for album in content:
		album_score = scrape_pitchfork(album)

		if album_score == -1:
			print album + " - " + str(album_score) + " " + strip_chars(album)
		else:
			print album + " - " + str(album_score)

		f.write(album + " - " + str(album_score) + "\n")
'''