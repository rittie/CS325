#
# Team RADZ
# 
# CS325-400
# Project #4

import sys, getopt ,math

cityList = []
cityCount = 0
matrix = []
visited = []
filename = ''
tourLength = 0

#function to calculate the Euclidean distance between two cities
def calc_dist(x1,y1,x2,y2):
	if ((x1 == x2) and (y1 == y2)):
		return 0
	else:
		#round to the nearest integer. 
		#For 0.1, put a one, then for 0.01 put 2, etc. negative values work in the other direction
		return round(math.sqrt(math.pow((x1 - x2),2) + math.pow((y1 - y2),2)),0)

#function to find the shortest path in the matrix
def find_short_path(fromCity):
	global matrix
	global visited
	global tourLength
	global cityCount
	minDist = 1000000
	tourCity = 0
	
	for toCity in range(cityCount):
		thisDist = matrix[fromCity][toCity]
		if (thisDist > 0 and thisDist < minDist):
			if (toCity not in set(visited)):
				minDist = thisDist
				tourCity = toCity

	tourLength += minDist
	return tourCity

def find_tour():
	global filename
	global cityList
	global cityCount
	global matrix
	global visited
	global tourLength
	fin = open(filename, "r")
	fout = 0
	char = ""
	str = ""
	cityPieces = []
	distance = 0
	tourCity = 0

	#first we split into giant array of words
	for word in fin.read().split(): 
		cityPieces.append(word)

	#close the file, we are done with it
	fin.close() 

	#now we sort into a 2d array with id, x, y at each index
	for x in range(0, len(cityPieces)-2, 3): 
		cityList.append((int(cityPieces[x]), int(cityPieces[x+1]), int(cityPieces[x+2])))

	#delete from start to finish on the cityPieces
	del cityPieces[:] 

	#get the count of cities
	cityCount = len(cityList)
	
	#populate the matrix
	matrix = [[calc_dist(cityList[n][1],cityList[c][1],cityList[n][2],cityList[c][2]) for n in range(cityCount)] for c in range(cityCount)]
	#print zip(*matrix)

	#go on a tour		
	tourCity = cityList[0][0]
	for c in range(cityCount):
		tourCity = find_short_path(tourCity)
		visited.append(tourCity)

	# write output to file
	filename = filename + '.tour' 

	fout = open(filename,'w')
	fout.write("%.0f\n" % tourLength) 
	for city in visited:
		fout.write("{0}\n".format(city))
	
	fout.close()

def main(argv):
	global filename

	opts, args = getopt.getopt(argv, "hf:", ["filename="])	

	for o, a in opts:
		if o == '-h':
			print 'usage: tsp.py -f <filename>'
			sys.exit()
		elif o in ("-f", "--filename"):
			filename = a
		else:
			assert False, "unhandled option"	

	find_tour()

if __name__ == '__main__':
	main(sys.argv[1:])
