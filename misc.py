'''
Miscellaneous things that need doing!
'''

import csv

with open('pitchfork.txt') as f:
	pitchfork = f.readlines()
with open('needledrop.txt') as f:
	needledrop = f.readlines()

data_list = []
for line in zip(needledrop, pitchfork):
	needle, pitch = line
	_, _, needle_score, genre = needle.split(" ::: ")
	needle_score = float(needle_score)
	genre = genre.strip('\n')
	pitch_score = float(pitch.split(" ::: ")[2].strip('\n'))

	if pitch_score > 0:
		data_list.append((needle_score, pitch_score, genre))
	else:
		continue

with open('scores.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows(data_list)
