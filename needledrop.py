'''
Gets information from the Needle Drop website, puts it into one file
with each line of format "artist - album - score"
'''

from bs4 import BeautifulSoup
import unidecode
import requests
import time 

site_prefix = "http://www.theneedledrop.com"
all_entries = []
file_name = "needledrop.txt"
f = open(file_name, 'w')
headers = {'user-agent': 'Your friend, Will.'}

for i in xrange(0, 11):
	def init_start_url(rating):
		return ("http://www.theneedledrop.com/articles/?tag=" + 
				str(rating) + "%2F10")

	start_url = init_start_url(i)

	url = start_url
	last_page = False

	while not last_page:
		r = requests.get(url, headers=headers)
		soup = BeautifulSoup(r.text, "html.parser")

		# Check to see if we've been sending too many requests
		# If so, just wait a second and try again! :)
		if soup.title.string == "429 Too Many Requests":
			time.sleep(1)
			continue

		page_entries = soup.find_all("h1", class_="entry-title")

		for album in page_entries:
			text_entry = str(unidecode.unidecode(album.a.get_text()))
			# Fuck the complicated ones
			text_split = text_entry.split(" - ")
			if len(text_split) > 2:
				print "fuck all y\'all"
				continue
			# Add in delimeters that won't be mistaken for other shit
			text_entry = text_split[0] + " ::: " + text_split[0] + " ::: " + str(i)
			f.write(text_entry + "\n")
			print text_entry

		older = soup.find(class_="older")

		if older is not None and older.string:
			url = site_prefix + older.a["href"]
			time.sleep(0.5) 
		else:
			last_page = True

f.close()
