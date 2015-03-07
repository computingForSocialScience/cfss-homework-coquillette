import requests
import sys
import pandas as pd
import numpy as np 
import itertools

def getRelatedArtists(artistID):
	url = 'https://api.spotify.com/v1/artists/' + artistID + '/related-artists'
	req = requests.get(url)
	if req.ok == False: 
		print "Error in getRelatedArtists Request"
	req.json()
	myjson = req.json()
	get_artists = myjson.get('artists')
	related_artist_list = []
	for i in range(len(get_artists)):
		get_related = get_artists[i]
		get_id = get_related['id']
		related_artist_list.append(get_id)
	return related_artist_list

#artist_id = '6olE6TJLqED3rqDCT0FyPh'
#getRelatedArtists(artist_id)

def getDepthEdges(artistID, depth):
	tuple_artist_list = []
	tuple_artist_list_check = []
	related_ids = []
	related_ids.append(artistID)
	for i in range(depth):
		for ids in related_ids:
			depth_artist_list = getRelatedArtists(ids)
			for artist in depth_artist_list:
				tupl = (ids, artist)
				tuple_artist_list.append(tupl)
		related_ids = depth_artist_list
	for tupl in tuple_artist_list:
		if tupl not in tuple_artist_list_check:
			tuple_artist_list_check.append(tupl)
	return tuple_artist_list_check
	#remove_duplicates_list = tuple_artist_list
	#set(remove_duplicates_list)
	#list(set(remove_duplicates_list))
	#return(remove_duplicates_list)

	"""x = depth_artist_list
	remove_duplicates_list = list(set(itertools.combinations(x, depth)))
	return remove_duplicates_list"""

	"""for tupl in tuple_artist_list_main:
	if tupl not in tuple_artist_list_check:
			tuple_artist_list_check.append(tupl)
	return tuple_artist_list_check"""

def getEdgeList(artistID, depth):
	depthEdges = getDepthEdges(artistID, depth)
	edge_list_df = pd.DataFrame(depthEdges)
	return edge_list_df

def writeEdgeList(artistID, depth, filename):
	save_edgeList = getEdgeList(artistID, depth)
	saved_csv_file = save_edgeList.to_csv(filename, index = False, header = ['artist', 'related_artist'])

#writeEdgeList('6olE6TJLqED3rqDCT0FyPh', 2, 'edgelist.csv')