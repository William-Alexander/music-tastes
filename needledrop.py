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

	# Get the website. If needledrop yells at us, try again?
	album_r = requests.get(album_url, headers=headers)
	album_soup = BeautifulSoup(album_r.text, 'html.parser')
	if album_soup.title.string == "429 Too Many Requests":
		sys.sleep(1)
		return get_genre(album_url)

	# Get all the tags.
	classes = album_soup.find("article")["class"]
	tags = [x[4:] for x in classes if x[0:4] == "tag-"]

	# For each genre, check how many of the tags contain that
	# genre name like alternative-hip-hop for hip-hop, etc...
	# These will each count. If it finds an *exact* match, tho,
	# then just stop :)

	# Honestly most of the songs will have a specific genre: judging
	# by my earlier work, only about ~50 didn't fall directly into 
	# any category.
	relevant_genres = []
	for genre in genre_list:
		for tag in tags:
			if genre == tag:
				return genre
			elif genre in tag:
				relevant_genres.append(genre)
			else:
				pass

	# Then we pick majority. In case of a tie, I'll decide myself.
	if relevant_genres:
		max_num = max(map(relevant_genres.count, relevant_genres))
		max_set = set(x for x in relevant_genres if relevant_genres.count(x) == max_num)
		if len(max_set) <= 0:
			return "no-genre"
		elif len(max_set) == 1:
			return max_set.pop()
		else:
			return str(max_set)
	return "no-genre"



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
			print text_split[1] + ' - ' + str(i) + ' - ' + genre

		older = soup.find(class_="older")

		if older is not None and older.string:
			url = site_prefix + older.a["href"]
			time.sleep(0.5) 
		else:
			last_page = True

f.close()
