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

def get_genre(album_url):
	"""
	Retrieves genre of album, given that album's url
	"""
	genre_list = ["rock", "pop", "electronic", "hip-hop", "loud-rock", "other", "classic"]

	album_r = requests.get(album_url, headers=headers)
	album_soup = BeautifulSoup(album_r.text, 'html.parser')
	if album_soup.title.string == "429 Too Many Requests":
		return "no_genre_1"

	classes = album_soup.find("article")["class"]
	tags = [x[4:] for x in classes if x[0:4] == "tag-"]

	relevant_genres = []
	for genre in genre_list:
		if genre in tags:
			relevant_genres.append(genre)
	# I guess if there's multiple, just pick the first?
	if relevant_genres:
		return relevant_genres[0]
	return "no_genre_2"


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
			# Let's get the genre.
			album_url = site_prefix + album.a["href"]
			genre = get_genre(album_url)
				
			text_entry = str(unidecode.unidecode(album.a.get_text()))
			# Fuck the complicated ones
			text_split = text_entry.split(" - ")
			if len(text_split) != 2:
				print "fuck all y\'all"
				continue
			if text_split[1] == "Self-Titled":
				text_split[1] = text_split[0]
			# Add in delimeters that won't be mistaken for other shit
			text_entry = text_split[0] + " ::: " + text_split[1] + " ::: " + str(i) + " ::: " + genre
			f.write(text_entry + "\n")
			print text_entry

		older = soup.find(class_="older")

		if older is not None and older.string:
			url = site_prefix + older.a["href"]
			time.sleep(0.5) 
		else:
			last_page = True

f.close()
