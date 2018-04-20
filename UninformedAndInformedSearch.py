#!/usr/bin/env python

#CS 331 
#Assignment 1
#Uninformed and Informed Search
#April 20, 2018
#Audrianna Rock
#Tarren ....TODO


import sys
import string
import Queue
import os.path
import operator


# Define the Node class
class Node:
	def __init__(self, nodeID, bankState, parentNodeId): #constructor
		self.nodeID = nodeID
		self.parentNodeId = parentNodeId
		self.state = bankState
		self.childrenIDsList = []

def childNode(state,parent):
#IE InitializeFrontier
#read in the input from the command line
#Declares mode, output file, initializes stateHistory and expanded Nodes count. sets goalBankStates global.
# retrieves input from command line. does error checking. opens and retrieves data from given files. turns retrieved data into a list. Removes the newline character from the end of each list. then creates a list item that contains the state of both banks (goalBankStates and initialBankStates)
#returns the initialBankStates
def getInput():
	global mode, outputFile 
	global expandedNodesCount, stateHistory, goalBankStates

	expandedNodesCount = 0
	stateHistory = []

	arguments = len(sys.argv)
	
	#if we don't have correct # of arguments, then exit.
	if arguments != 5:
		print 'Incorrect number of arguments received. Expected 4 additional arguments. Recieved ', (arguments - 1) ,'. Exiting.'
		exit()

	#set arguments to more readable names
	initialStateFile = sys.argv[1] 
	goalStateFile = sys.argv[2]
	mode = sys.argv[3]
	outputFile = sys.argv[4]
	
	#check that we actually have this file
	if os.path.isfile(initialStateFile):
		initialState = open(initialStateFile, 'r')
	else:
		print initialStateFile, ' is not a file. Exiting.'
		exit()

	if os.path.isfile(goalStateFile):
		goalState = open(goalStateFile, 'r')
	else:
		print goalStateFile, ' is not a file. Exiting.'
		exit()

	#turn read data into a list item
	#set our initials and goal states
	leftBankInitial = initialState.readline().split(",")
	rightBankInitial = initialState.readline().split(",")

	#removal of newline character on last element
	leftBankInitial[-1] = leftBankInitial[-1].strip()
	rightBankInitial[-1] = rightBankInitial[-1].strip()

	leftBankGoal = goalState.readline().split(",")
	rightBankGoal = goalState.readline().split(",")
	
	#removal of newline character on last element
	leftBankGoal[-1] = leftBankGoal[-1].strip()
	rightBankGoal[-1] = rightBankGoal[-1].strip()

	initialState.close()
	goalState.close()


	goalBankStates = [leftBankGoal, rightBankGoal]
	initialBankStates = [leftBankInitial, rightBankInitial]
	#TODO CREATE THE INITIAL NODE
	#initialNode = Node(0, 'initial', -1)

	#verify we have correct modes
	if (str(mode) == "bfs" or
	    str(mode) == "dfs" or
	    str(mode) == "iddfs" or
	    str(mode) == "astar"):
		
		return initialBankStates

	else:
		print str(mode), 'is not an acceptable mode. Please use bfs, dfs, iddfs, or astar. Exiting.'
		exit()

def actionOneChicken(expandingNode):
	leftState = expandingNode.state[0]
	rightState = expandingNode.state[1]

	if(rightState[2] == 1):
		headLeft = True
	else: 
		headLeft = False

def actionTwoChicken(expandingNode):
	leftState = expandingNode.state[0]
	rightState = expandingNode.state[1]

	if(rightState[2] == 1):
		headLeft = True
	else: 
		headLeft = False

def actionOneWolf(expandingNode):
	leftState = expandingNode.state[0]
	rightState = expandingNode.state[1]

	if(rightState[2] == 1):
		headLeft = True
	else: 
		headLeft = False

def actionOneWolfOneChicken(expandingNode):
	leftState = expandingNode.state[0]
	rightState = expandingNode.state[1]

	if(rightState[2] == 1):
		headLeft = True
	else: 
		headLeft = False

def actionTwoWolf(expandingNode):
	leftState = expandingNode.state[0]
	rightState = expandingNode.state[1]

	if(rightState[2] == 1):
		headLeft = True
	else: 
		headLeft = False

#do one of five actions 
#    Put one chicken in the boat
#    Put two chickens in the boat
#    Put one wolf in the boat
#    Put one wolf and one chicken in the boat
#    Put two wolves in the boat 
#adds nodes to the fifo if the node is acceptable.
#determines if the new node would cause chicken death.
def expandBfs(nodeToExpand):


	#if boat is on the right side, we are heading left
	if(rightState[2] == 1):
		headLeft = True

	#1CM = 1 chicken moved
	#put one chicken in the boat
	leftState1CM = leftState
	rightState1CM = rightState

	if(headLeft):
		if(gt(rightState[0], 0) and 
		   ge((rightState[0] - 1), rightState[1])) and #if we remove a chicken from the right side, will the chickens left live?
		   ge(leftState[0] + 1, leftState[1]): #will we have an OK number of chickens on the left side as well?
			
			leftState1CM[0] = leftState[0] + 1
			leftState1CM[2] = 1
		 
			rightState1CM[0] = rightState[0] - 1
			rightState1CM[2] = 0

			state = [leftState1CM, rightState1CM]
			FIFO.put(state)

	else:
		if(gt(leftState[0],0) and
		   ge((leftState[0] - 1), leftState[1])) and #if we remove a chicken from the left side, will the chickens remaining survive
		   ge((rightState[0] + 1), rightState[1]): #will there be enough chickens on the right side for our chickens to survive?
			
			leftState1CM[0] = leftState[0] -1
			leftState1CM[2] = 0
		
			rightState1CM[0] = rightState[0] + 1
			rightState1CM[2] = 1

			state = [leftState1CM, rightState1CM]
			FIFO.put(state)


	#2CM = 2 chickens moved
	#put two chickens in the boat
	leftState2CM = leftState
	rightState2CM = rightState

	if(headLeft):
		if(gt(rightState[0],1) and
		   ge((rightState[0] - 2), rightState[1])) and #if we remove 2 chickens from the right side, will the remaining chickens survive?
		   ge((leftState[0] + 2), leftState[1]): #do we have enough chickens in order to survive being moved to this side?
			
			leftState2CM[0] = leftState[0] + 2
			leftState2CM[2] = 1
			 
			rightState2CM[0] = rightState[0] - 2
			rightState2CM[2] = 0

			state = [leftState2CM, rightState2CM]
			FIFO.put(state)
	else:
		if(gt(leftState[0],1) and
		   ge((leftState[0] - 2), leftState[1])) and #if we remove 2 chickens from the left side, will the remaining chickens surivie
		   ge((rightState[0] + 2), rightState[1]): #do we have enough chickens in order to survive the right side

			leftState2CM[0] = leftState[0] - 2
			leftState2CM[2] = 0
			 
			rightState2CM[0] = rightState[0] + 2
			rightState2CM[2] = 1

			state = [leftState2CM, rightState2CM]
			FIFO.put(state)

	#1WM = 1 wolf moved
	#put one wolf in the boat
	leftState1WM = leftState
	rightState1WM = rightState	

	if(headLeft):
		if(gt(rightState[1],0) and
		   le((leftState[1] + 1), leftState[0])): #by adding another wolf to the left side, do we outweight the chickens?

			leftState1WM[1] = leftState[1] + 1
			leftState1WM[2] = 1
			 
			rightState1WM[1] = rightState[1] - 1
			rightState1WM[2] = 0

			state = [leftState1WM, rightState1WM]
			FIFO.put(state)

	else:
		if(gt(leftState[1],0) and
		   le((rightState[1] + 1), rightState[0])): #by adding another wolf to the right bank, do we outweight the chickens?

			leftState1WM[1] = leftState[1] - 1
			leftState1WM[2] = 0
			 
			rightState1WM[1] = rightState[1] + 1
			rightState1WM[2] = 1

			state = [leftState1WM, rightState1WM]
			FIFO.put(state)

	#1CWM = 1 chicken and 1 wolf moved
	#put one wolf and one chicken in the boat
	leftState1CWM = leftState
	rightState1CWM = rightState
	
	if(headLeft):
		if(gt(rightState[0],0) and gt(rightState[1],0) and
		   ge((leftState[0] + 1), (leftState[1] + 1))): #if there are more wolves than chickens on the left side now, then goodbye chicken added

			leftState1CWM[0] = leftState[0] + 1
			leftState1CWM[1] = leftState[1] + 1
			leftState1CWM[2] = 1
			 
			rightState1CWM[0] = rightState[0] - 1
			rightState1CWM[1] = rightState[1] - 1
			rightState1CWM[2] = 0

			state = [leftState1CWM, rightState1CWM]
			FIFO.put(state)

	else:
		if(gt(leftState[0],0) and gt(leftState[1],0) and
		   ge((rightState[0] + 1), (rightState[1] + 1))):#if there are more wolves than chickens on the left side now, then goodbye chicken added

			leftState1CWM[0] = leftState[0] - 1
			leftState1CWM[1] = leftState[1] - 1
			leftState1CWM[2] = 0
			 
			rightState1CWM[0] = rightState[0] + 1
			rightState1CWM[1] = rightState[1] + 1
			rightState1CWM[2] = 1

			state = [leftState1CWM, rightState1CWM]
			FIFO.put(state)


	#put two wolves in the boat
	#2WM = 2 wolves moved
	leftState2WM = leftState
	rightState2WM = rightState
	
	if(headLeft):
		if(gt(rightState[1],1) and 
		   le((leftState[1] + 2), leftState[0])): #by adding two wolves to the left side, do wolves then outweigh chickens?

			leftState2WM[1] = leftState[1] + 2
			leftState2WM[2] = 1
			 
			rightState2WM[1] = rightState[1] - 2
			rightState2WM[2] = 0

			state = [leftState2WM, rightState2WM]
			FIFO.put(state)

	else:
		if(gt(leftState,1) and 
		   le((rightState[1] + 2), rightState[0])): #by adding two wolves to the right side, do wolves outweight chickens?			

			leftState2WM[1] = leftState[1] - 2
			leftState2WM[2] = 0
			 
			rightState2WM[1] = rightState[1] + 2
			rightState2WM[2] = 1

			state = [leftState2WM, rightState2WM]
			FIFO.put(state)

	return

#write the result to output
def writeToOutput(solutionFound, solutionStates):
	if(".txt" in outputFile):
		writeFile = open(outputFile, "w+")
	else:
		writeFile = open(outputFile + ".txt", "w+")
	
	if(solutionFound == False):
		print "No solution found.\n"
		writeFile.write("No solution found.\n")
	else:
		writeFile.write("Solution Found \n")
		writeFile.write("Solution States: \n" + solutionStates + "\n")
		writeFile.write("Number of nodes expanded: " + expandedNodesCount + "\n")				
	writeFile.close()
	exit()

#checks to see if we've had this state in the past or not
def isInStateHistory(state):
	if(state in stateHistory):
		return True
	else:
		return False

#TODO define
def solution(nodeSolution):
	return

#Breadth-First Search
#FIFO Queue
#Expand all nodes @ a given depth before any nodes at the next level are expanded
def bfs(nodeToExpand):

	#verify that this is putting these in as a pair
	while(solutionFound is False):
		#no solution was found
		if(FIFO.Empty):
			writeToOutput(False) #will exit
		else:
			nodeToExpand = FIFO.get()

			#check if this nodes state is the goal state. 
			if(nodeToExpand.state == goalBankStates):
				#if its the goal state. Append it to a last in first out.
				return solution(nodeToExpand)
				#TODO need to somehow return the entire thing up the line for the successful nodes
			else:
				#checks if the nodes state is already in our history
				haveExpanded = isInStateHistory(nodeToExpand.state)
				#go in if not expanded
				if(haveExpanded == False):	
					stateHistory.Append(nodeToExpand.state) #add to history
					expandedNodesCount += 1

					expandBfs(nodeToExpand)


				
#Depth-First Search
#LIFO Queue
#Expands the deepest node in the current fringe of the search tree
def dfs():



	return

#Iterative Deepening Depth First
#Do Depth First with depth limit, iterate up depth limit until a goal is found.
#Merge of depth and breadth
def iddfs():

	return


def astar():


	return

#LIFO and FIFO made global. Initialized at beginning of program. Each have initial state added to them.
#ResultLIFO made as would give us the order print out needed (if we can add to it correctly that is)
#State gotten by input
def main():
	global solutionFound, FIFO, LIFO, currentNodeIndex

	currentNodeIndex = 0
	solutionFound = False
	LIFO = LifoQueue()
	resultLifo = LifoQueue()
	FIFO = Queue()
	#state is the initial starting states of the Left bank and Right bank
	firstNode = getInput()

	FIFO.put(firstNode)
	LIFO.put(firstNode)

	if(mode == "bfs"):
		bfs(firstNode)
	elif(mode == "dfs"):
		dfs(firstNode)
	elif(mode == "iddfs"):
		iddfs(firstNode)
	else: #astar
		astar(firstNode)

main()
