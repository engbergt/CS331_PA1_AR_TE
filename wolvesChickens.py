import sys
import csv
import importlib

import astar


# Grab the user arguments
initialStateFileName = "tests/" + sys.argv[1]
goalStateFileName = "tests/" + sys.argv[2]
modeRequested = sys.argv[3]
outputFileName = sys.argv[4]

# Initialize arrays for the file info to be placed for easy access.
initalLeftBank = []
initialRightBank = []

goalLeftBank = []
goalRightBank = []

with open(initialStateFileName) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    initalLeftBank = next(csvReader)
    initialRightBank = next(csvReader)
    csvDataFile.close()

with open(goalStateFileName) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    goalLeftBank = next(csvReader)
    goalRightBank = next(csvReader)
    csvDataFile.close()



outPutText1 = "Here is output line 1\n"
outPutText2 = "Here is output line 2\n"

writeFile = open("output.txt","w+")
writeFile.write(outPutText1)
writeFile.write(outPutText2)
writeFile.close()