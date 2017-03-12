import re

'''
So the idea is that if we take out all of the characters except for the 
alphabet, numbers, and spaces, we can compare things more easily since
different sites use different encodings and aren't always consistent with
punctuation.
'''
def strip_chars(my_str):
	"""
	Removes all annoying characters and articles, ya dig?
	"""
	my_str = my_str.lower()
	def remove_articles(my_str):
		s = ["a", "an", "and", "the", "&"]
		return ' '.join(filter(lambda w: not w in s, my_str.split()))
	my_str = remove_articles(my_str)
	regex = re.compile('[^a-z0-9\'\- ]')
	return regex.sub('', my_str)

def get_albums(my_file="needledrop.txt"):
	"""
	Nabs all the artists and corresponding albums from the masterfile
	that contains all of the albums the Needle Drop has reviewed. To
	preserve order, I use a list.

	Does not include review scores.
	"""
	with open(my_file) as f:
		content = f.readlines()
		content = [x.strip("\n") for x in content]

	album_list = []

	for item in content:
		# Python 3 supports extended iterable unpacking, but not 2 :(
		artist, album, _, _ = item.split(" ::: ")
		album_list.append((artist, album))

	return album_list

def fix_album(album):
	"""
	Just makes the album nice and presentable to the sites.
	"""
	album = strip_chars(album)
	return album.replace(" ", "%20")