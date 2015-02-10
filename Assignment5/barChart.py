import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    """Reads data from artists.csv and albums.csv, extracts 
    information needed for bar chart from each file, 
    creates a list of artist names,and creates a dictionary
    of albums produced during given decades"""
    f_artists = open('artists.csv') #opens artists.csv file
    f_albums = open('albums.csv')  #opens albums.csv file

    artists_rows = csv.reader(f_artists) #reads rows from artists.csv and creates variable to stand in for those rows of information
    albums_rows = csv.reader(f_albums) #reads rows from albums.csv and creates variable to stand in for those rows of information

    artists_header = artists_rows.next() #ignores the first row, which is the header, and moves on to next item in artists_rows
    albums_header = albums_rows.next() #ignores the first row, which is the header, and moves on to the next item in albums_rows

    artist_names = [] #creates a blank list of artist names
    
    decades = range(1900,2020, 10) #sets range of decades from 1900-2020 in ten year increments
    decade_dict = {} #creates blank dictionary to be filled
    for decade in decades:
        decade_dict[decade] = 0 #dictionary keys are equal to the decades, set values equal to zero
    
    for artist_row in artists_rows: #for each row in artists_rows, sets variable "artist_row" equal to the four variables listed in row
        if not artist_row: #skips for loop for data that doesn't appear in artists_rows
            continue
        artist_id,name,followers, popularity = artist_row 
        artist_names.append(name) #appends artist name to list artist_names

    for album_row  in albums_rows: #for each row in albums_rows, sets variable "album_row" equal to five variables listed in row
        if not album_row: #skips for loop for data that does appear in albums_rows
            continue
        artist_id, album_id, album_name, year, popularity = album_row
        for decade in decades:
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)): #if the year of the album is within a particular decade-- after 1990, say, but before 2000
                decade_dict[decade] += 1 #add one to the number of albums from that decade to the value in the decade dictionary
                break

    x_values = decades #x-values are equal to decades
    y_values = [decade_dict[d] for d in decades] #y-values are equal to counts of albums in the decades
    return x_values, y_values, artist_names #returns x_values, y_values, and list of artist_names

def plotBarChart():
    """Plots bar chart using x_vals, y_vals, and artist_names generated in getBarChartData function"""
    x_vals, y_vals, artist_names = getBarChartData() #pulls x and y values and artists names list from previously defined function
    fig , ax = plt.subplots(1,1) #creates a figure with one subplot
    ax.bar(x_vals, y_vals, width=10) #plots x and y values
    ax.set_xlabel('decades') #labels the x axis 'decades'
    ax.set_ylabel('number of albums') #labels the y axis 'number of albums'
    ax.set_title('Totals for ' + ', '.join(artist_names)) #sets title as 'Totals for __', filling in the artist names from the artist_names list
    plt.show() #shows the bar chart


    
