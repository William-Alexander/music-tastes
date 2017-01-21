'''
So the idea is that if we take out all of the characters except for the 
alphabet, numbers, and spaces, we can compare things more easily since
different sites use different encodings and aren't always consistent with
punctuation.
'''
def strip_chars(my_str):
	"""
	Removes all annoying characters and articles, ya dig?

	w.r.t remove_articles: every rule requires a precident, right? Pitchfork
	and Needle Drop differ sometimes in how they use articles, so I just get
	rid of 'em all.

	IT'S NOT PERFECT unfortunately but whatever it's conservative.
	"""
	my_str = my_str.lower()
	def remove_articles(my_str):
		s = ["a", "an", "and", "the", "&"]
		return ' '.join(filter(lambda w: not w in s, my_str.split()))
	my_str = remove_articles(my_str)
	regex = re.compile('[^a-z0-9\'\- ]')
	return regex.sub('', my_str)