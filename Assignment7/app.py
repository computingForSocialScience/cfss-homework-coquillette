from flask import Flask, render_template, request, redirect, url_for
import pymysql
import unicodecsv

app = Flask(__name__)

import sys
import networkx as nx
import pandas as pd
import random
from io import open
from artistNetworks import getEdgeList
from analyzeNetworks import randomCentralNode, combineEdgeLists, pandasToNetworkX
from fetchArtist import *
from fetchAlbums import * 

dbname="playlists"
host="localhost"
user="root"
passwd="AN1ceSl1ceofPy"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

def createnewPlaylist(artistName):
    cur = db.cursor()
    maketableplaylists = """CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY AUTO_INCREMENT, rootArtist VARCHAR(255));""" 
    maketablesongs = """CREATE TABLE IF NOT EXISTS songs (playlistId INTEGER, songOrder INTEGER, artistName VARCHAR(255), albumName VARCHAR(255), trackName VARCHAR(255));"""
    cur.execute(maketableplaylists)
    cur.execute(maketablesongs)
    #db.commit()

    artist_names = artistName
    depth = 2 #change depth at will

    artists_id = fetchArtistId(artistName)
    edge_list = getEdgeList(artists_id,depth)

    g = pandasToNetworkX(edge_list)

    random_artists = []
    for i in range(30):
        random_artist = randomCentralNode(g)
        random_artists.append(random_artist)

    artist_names = []
    album_list = []
    for artist_id in random_artists:
        artist = fetchArtistInfo(artist_id)
        artist_name = artist['name']
        artist_names.append(artist_name)
        album_id_list = fetchAlbumIds(artist_id)
        random_album = (random.choice(album_id_list))
        random_album_info = fetchAlbumInfo(random_album) 
        random_album_name = random_album_info['name']
        tupl = (random_album_name, random_album)
        album_list.append(tupl)

    random_track_list = []
    for album in album_list:
        get_album_tracks_url = 'https://api.spotify.com/v1/albums/' + album[1] + '/tracks'
        req = requests.get(get_album_tracks_url)
        if req.ok == False: 
            print "Error in get_album_tracks_url Request"
        req.json()
        myjson = req.json()
        get_items = myjson.get('items')
        track_list = []
        for i in range(len(get_items)):
            get_track_name = get_items[i]['name']
            track_list.append(get_track_name)
            random_track = (random.choice(track_list))
        random_track_list.append(random_track)

    #playlist = """INSERT INTO playlists (id);"""
    #cur.execute(playlist)
    #db.commit()?
    get_id_number = """SELECT MAX(id) from playlists;"""
    cur.execute(get_id_number)
    playlist_id = cur.fetchall()
    playlistID = playlist_id[0][0]
    artist_name_in = """INSERT INTO playlists (rootArtist) VALUES ('%s')""" % (artistName)
    cur.execute(artist_name_in)
    #playlistID = cur.lastrowid
    #db.commit()
    for i in range(len(random_track_list)):
        Artist_Name = '"' + artist_names[i] + '"'
        Artist_Name.replace('\'', "")
        Album_Name = '"' + album_list[i][0] + '"'
        Album_Name.replace('\'', "")
        Track_Name = '"' + random_track_list[i] + '"'
        Track_Name.replace('\'', "")
        songOrder = i+1
        sql = """INSERT INTO songs (playlistId, songOrder, artistName, albumName, trackName) 
        VALUES (%s, %s, %s, %s, %s)""" % (playlistID, songOrder, Artist_Name, Album_Name, Track_Name)
        cur.execute(sql)
        db.commit()

    cur.close()

#createnewPlaylist("Sting")

@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    cur = db.cursor()
    get_playlists = """SELECT * FROM playlists;"""
    cur.execute(get_playlists)
    playlists = cur.fetchall()
    return render_template('playlists.html',playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    cur = db.cursor()
    input_playlist = playlistId
    song_request = """SELECT songOrder, artistName, albumName, trackName FROM songs WHERE playlistId = (%s)""" % (input_playlist)
    cur.execute(song_request)
    songs = cur.fetchall()
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        createnewPlaylist(artistName)
        return(redirect("/playlists/"))



if __name__ == '__main__':
    app.debug=True
    app.run()