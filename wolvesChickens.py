import sys
import csv
import importlib

import astar
import iddfs


# Grab the user arguments
initialStateFileName = sys.argv[1]
goalStateFileName = sys.argv[2]
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


# Define the Node class
class Node:
	def __init__(self, nodeID, nodeType, parentNodeId): #constructor
		self.nodeID = nodeID
		self.nodeType = nodeType
		self.parentNodeId = parentNodeId
		self.leftBankList = []
		self.rightBankList = []
		self.childrenIDsList = []


# Make the inital node from the users files data.
initialNode = Node(0, 'initial', -1)

initialNode.leftBankList = list(initalLeftBank)
initialNode.rightBankList = list(initialRightBank)


# Make the goal node from the users files data.
goalNode = Node(-1, 'goal', -2)

goalNode.leftBankList = list(goalLeftBank)
goalNode.rightBankList = list(goalRightBank)


# Start adding nodes and check each one, until the goal is reached.





# Output a file with the name of the 4th user argument.
outPutText1 = "Here is output line 1\n"
outPutText2 = "Here is output line 2\n"

writeFile = open(outputFileName + ".txt", "w+")
writeFile.write(outPutText1)
writeFile.write(outPutText2)
writeFile.close()