#import urllib2
import requests
from bs4 import BeautifulSoup
import time

start_url = "http://www.theneedledrop.com/articles/?tag=6%2F10"

site_prefix = "http://www.theneedledrop.com"
all_entries = []
url = start_url
last_page = False
hdr = {'User-Agent': 'your music nerd friend, Will :)'}

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
		all_entries.append(album.a.get_text())
		print album.a.get_text()

	#older = soup.find_all("div", class_="older")
	older = soup.find(class_="older")

	if older.string:
		url = site_prefix + older.a["href"]
		time.sleep(1) 
	else:
		last_page = True

print len(all_entries)




