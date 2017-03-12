'''
Gets all the information from Pitchfork to accompany the ratings put
out by the Needle Drop. Returns the same list as the Needle Drop, 
except with Pitchfork's ratings (-1 if the album isn't found)
'''

from bs4 import BeautifulSoup
from useful_funcs import *
import requests
import unidecode

def scrape_pitchfork(artist, album):
	"""
	Returns Pitchfork's rating of the album if found, else returns -1
	"""
	base_url = "http://pitchfork.com"
	url = base_url + "/search/?query=" + fix_album(album) 
	headers = {'user-agent': 'Your friend, Will.'}
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.text, "html.parser")

	# Step 2: grab the correct one, and go to that page!
	reviews = soup.find_all("div", class_="review")

	if len(reviews) == 0:
		return -1
	else:
		# Probably a silly way to do this, but this is where an exact
		# match will be saved, if we find it. If there's more than one
		# exact match, that'll be silly.
		big_ol_div = ""

		for review in reviews:
			pitchfork_album = review.find(class_="title").text.lower()
			pitchfork_album = unidecode.unidecode(pitchfork_album)
			pitchfork_artist = review.find(class_="artist-list").text.lower()
			pitchfork_artist = unidecode.unidecode(pitchfork_artist)
			needledrop_album = album.lower()
			needledrop_artist = artist.lower()
			# Both the album and the artist have to match. We're picky!
			if (strip_chars(pitchfork_album) == strip_chars(needledrop_album) and
				strip_chars(pitchfork_artist) == strip_chars(needledrop_artist)):
				big_ol_div = review
				break
		if big_ol_div is "":
			# We didn't find anything? That's fine, goodbye!
			return -1

		relative_url = big_ol_div.find(class_="album-link")["href"]

		url = base_url + relative_url
		r = requests.get(url, headers=headers)
		soup = BeautifulSoup(r.text, "html.parser")

		# Step 3: Grab dat score
		score = soup.find(class_="score").string
		return float(score)

needledrop = get_albums()

with open('pitchfork.txt', 'w') as f:
	for datum in needledrop:
		artist, album = datum
		score = scrape_pitchfork(artist, album)

		new_datum = artist + " ::: " + album + " ::: " + str(score)
		print new_datum

		f.write(new_datum + '\n')
