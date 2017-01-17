import urllib2
from bs4 import BeautifulSoup
import time

start_url = "http://www.theneedledrop.com/articles/?tag=6%2F10"

site_prefix = "http://www.theneedledrop.com"
all_entries = []
url = start_url
last_page = False
hdr = {'User-Agent': 'your music nerd friend, Will :)'}

while not last_page:
	req = urllib2.Request(url, headers=hdr)
	html = urllib2.urlopen(req).read()
	soup = BeautifulSoup(html, "html.parser")

	page_entries = soup.find_all("h1", class_="entry-title")

	for album in page_entries:
		all_entries.append(album.a.get_text())
		print album.a.get_text()

	older = soup.find_all("div", class_="older")
	#print older

	if older:
		url = site_prefix + older[0].a["href"]
		time.sleep(1) 
	else:
		last_page = True

print len(all_entries)




