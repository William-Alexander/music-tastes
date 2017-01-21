from useful_funcs import strip_chars
import urllib2

'''
Fuck it, let's make this a separate file. I should be doing this 
with all the different sites anyhow.

Unfortunately, Sputnik doesn't really use very well-formatted html. There
aren't any real classes, ids, etc... so here's what we'll do: On an artist's
page, we'll look for the "bold" tag with the proper album title in it. BS 
makes it easy to grab every tag of a single type. The subsequent "bold" tag
contains the score.
'''

def scrape_sputnik():
	"""
	Uses the masterfile to generate a list of artists and corresponding
	albums, and then searches for each one on Sputnik. Returns dict
	of albums and corresponding score.
	"""

	with open('masterfile.txt') as f:
		content = f.readlines()

	artist_dict = {}

	content = [x.strip("\n") for x in content]

	for item in content:
		artist, album = item.split(" - ")
		artist_dict[artist] = album

	return 0

