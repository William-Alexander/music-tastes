import scraper

num_ratings = {}

for i in xrange(11):
	num = scraper.scrape_needledrop(i)
	num_ratings[i] = num

print num_ratings