import json
import os

def enumerater():

	micrographs = os.listdir('data/crops_new')
	micrographs.sort()

	i = 0
	j = 0
	cropped = {}
	for micrograph in micrographs:
		path = 'data/crops_new/{}'.format(micrograph)
		if j==0:
			i+=1
		micrograph_id = '{}-{}'.format(i,(os.path.splitext(micrograph)[0]).split('-')[-1])  
		j = (j+1)%4
		cropped[micrograph_id] = path
	with open('data/cropped_new/micrographs.json', 'w') as f:
			json.dump(cropped, f)