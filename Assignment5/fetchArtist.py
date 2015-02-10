import sys
import requests
import csv
#from bs4 import Beautiful Soup

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    base_url = 'https://api.spotify.com'
    search_url = '/v1/search?q=' 
    artist_name = name + '&type=artist' 
    url = base_url + search_url + artist_name
    #print "artist url is ", url
    req = requests.get(url)
    if not req.ok:
    	print "Error in Request"
    req.json()
    myjson = req.json()
    artist_info = myjson.get('artists')
    items_info = artist_info.get('items')
    get_id = items_info[0]
    fetch_id = get_id['id']
    return fetch_id

#artist = 'Bikini Kill'
#fetchArtistId(artist)

def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    base_url = 'https://api.spotify.com/v1/artists/'
    #artist_id = fetchArtistId(artist)
    #print artist_id
    url = base_url + str(artist_id)
    #print url
    req = requests.get(url)
    if not req.ok:
    	print "Error in Request"
    req.json()
    myjson = req.json()
    get_genre = myjson.get('genres')
    followers = myjson.get('followers')
    get_followers = followers['total']
    get_id = artist_id
    get_name = myjson.get('name')
    get_popularity = myjson.get('popularity')
    keys = ['followers', 'genres', 'id', 'name', 'popularity']
    values = [get_followers, get_genre, get_id, get_name, get_popularity]
    artist_dict = dict(zip(keys,values))
    return artist_dict

#artist = 'Bikini Kill'
#artist_id = fetchArtistId(artist)
#fetchArtistInfo(artist_id)