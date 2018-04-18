import sys
import csv

# Grab the user arguments
initialStateFileName = sys.argv[1]
goalStateFileName = sys.argv[2]
modeRequested = sys.argv[3]
outputFileName = sys.argv[4]

# Grab the referenced files
initialStateFile = open(initialStateFileName)
goalStateFile = open(goalStateFileName)

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


# Read the file contents into arrays for easy access
# reader = csv.reader(initialStateFile, delimiter=',')