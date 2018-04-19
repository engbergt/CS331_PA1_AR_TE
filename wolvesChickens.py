import sys
import csv
import importlib

import astar
import iddfs


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


# Define the Node class
class Node:
	def __init__(): #constructor
		self.nodeID = nodeID
		self.nodeType = nodeType
		self.parentNodeId = parentNodeId
		self.leftBankList = []
		self.rightBankList = []
		self.childrenIDsList = []


# Make the inital node from the users files.

initialNode = Node()

initialNode.nodeID = 0
initialNode.nodeType = 'initial'
initialNode.parentNodeID = -1
initialNode.leftBankList = copy.deepcopy(initalLeftBank)
initialNode.rightBankList = copy.deepcopy(initialRightBank)


# example stuffss 
# lilnode = Node(3,"c1", 0)
# lilnode.leftBankList.append(2)
# lilnode.leftBankList.append(7)
# print(lilnode.leftBankList[1])


# Output an file with the name of the 4th user argument.
outPutText1 = "Here is output line 1\n"
outPutText2 = "Here is output line 2\n"

writeFile = open(outputFileName + ".txt", "w+")
writeFile.write(outPutText1)
writeFile.write(outPutText2)
writeFile.close()