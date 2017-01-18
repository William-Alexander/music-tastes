import sys
import requests
from bs4 import BeautifulSoup
import time

def scrape_needledrop(rating):
	def init_start_url(rating):
		return ("http://www.theneedledrop.com/articles/?tag=" + 
				str(rating) + "%2F10")

	start_url = init_start_url(rating)

	site_prefix = "http://www.theneedledrop.com"
	all_entries = []
	url = start_url
	last_page = False

	file_name = "needledrop" + str(rating) + ".txt"
	f = open(file_name, 'w')

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
			f.write((album.a.get_text().encode('ascii', 'ignore')) + "\n")

		older = soup.find(class_="older")

		if older is not None and older.string:
			url = site_prefix + older.a["href"]
			time.sleep(0.5) 
		else:
			last_page = True

	f.close()
	return len(all_entries)




