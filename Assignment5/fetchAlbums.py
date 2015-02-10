import requests
from datetime import datetime

def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url = 'https://api.spotify.com/v1/artists/' + artist_id + '/albums?market=US&album_type=album'
    req = requests.get(url)
    #print url
    if not req.ok:
    	print "Error in Request"
    req.json()
    myjson = req.json()
    get_items = myjson.get('items')
    album_id_list = []
    for i in range(len(get_items)):
    	get_album = get_items[i]
    	get_id = get_album['id']
    	album_id_list.append(get_id)
    return album_id_list

#artist_id = '6olE6TJLqED3rqDCT0FyPh'
#fetchAlbumIds(artist_id)

def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    url = 'https://api.spotify.com/v1/albums/' + album_id
    req = requests.get(url)
    #print url
    if not req.ok:
    	print "Error in Request"
    req.json()
    myjson = req.json()
    artist_info = myjson.get('artists')
    get_artist_id = artist_info[0]['id']
    get_album_id = album_id
    get_name = myjson.get('name')
    get_date = myjson.get('release_date')
    get_year = get_date[0:4]
    get_popularity = myjson.get('popularity')
    keys = ['artist_id', 'album_id', 'name', 'year', 'popularity']
    values = [get_artist_id, get_album_id, get_name, get_year, get_popularity]
    album_dict = dict(zip(keys,values))
    return album_dict
    
#album_id = '14VVqBoDw1SxoNLW3Cj3mN'
#fetchAlbumInfo(album_id)