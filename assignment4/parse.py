import csv
import sys

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)

def get_avg_latlng(filename):
	lines = readCSV(filename)
	sum_lat = 0
	sum_lng = 0
	for i in lines:
		if (i[-3] == ""): 
			continue
		if (i[27] == "NJ"):
			continue
		sum_lat = sum_lat + float(i[-3])
		sum_lng = sum_lng + float(i[-2])

	avg_lat = sum_lat / float(len(lines) - 3)
	avg_lng = sum_lng / float(len(lines) - 3)

	print("average latitude: ", avg_lat, "average longitude: ", avg_lng)

#if __name__== '__main__':
	#get_avg_latlng("permits_hydepark.csv")



import Image
#import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

def zip_code_barchart(filename):
    lines = readCSV(filename)
    zipcodes = []
    for i in lines:
        if (i[28] == ""):
            continue
        if (i[27] == "NJ"): #Filtering out null data and NJ contractors
            continue
        else:
            zi = i[28][0:5]
        zipcode = int(zi)
        zipcodes.append(zipcode)
    
    plt.hist(zipcodes, bins=100)
    plt.title('Zipcode Histogram')
    plt.xlabel('Contractor Zipcodes')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.draw()
    plt.savefig('histogram.png')
    Image.open('histogram.png').save('histogram.jpg', 'JPEG') 

#if __name__== '__main__':
	#zip_code_barchart("permits_hydepark.csv")

if sys.argv[1] == 'latlong':
	get_avg_latlng("permits_hydepark.csv")
elif sys.argv[1] == 'hist':
	zip_code_barchart("permits_hydepark.csv")
else:
	print "You done goofed"