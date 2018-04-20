#!/usr/bin/env python

#CS 331 
#Assignment 1
#Uninformed and Informed Search
#April 20, 2018
#Audrianna Rock
#Tarren Engberg


import sys
import string
import Queue
import os.path
import operator


# Define the Node class
class Node:
	def __init__(self, nodeID, bankState, parentID): #constructor
		self.nodeID = nodeID
		self.parentID = parentID
		self.state = bankState

def CopyState(state):
	copiedState = []
	copiedState.append(state[0])
	copiedState.append(state[1])
	copiedState.append(state[2])

	return copiedState

#take the parent id of a node, and find it in the node list
#return that parent node
def getParentNode(parentId):
	global nodeList
	for node in nodeList:
		if(node.nodeID == parentId):
			return node

#write the result to output
#if solutionStates is None, then write no solution
#otherwise use what you're given with solutionStates
def writeToOutput(solutionStates):
	global expandedNodesCount
	if(".txt" in outputFile):
		writeFile = open(outputFile, "w+")
	else:
		writeFile = open(outputFile + ".txt", "w+")
	
	if(solutionStates == None):
		print "No solution found.\n"
		writeFile.write("No solution found.\r\n")
	else:
		print "solution found"
		writeFile.write("Solution States \r\n")
		for state in solutionStates:
			writeFile.write("%s\n" %state)
			print state

		writeFile.write("Number of nodes expanded: %d\r\n" % expandedNodesCount)				
	writeFile.close()
	exit()

#Takes in the lastmost node that has the same state as the goal
#Retrieves the Parent States and creates the path from the parent to the goal state.
#returns a list of the states from root to goal
def solution(nodeSolution):
	results = []
	results.append(nodeSolution.state)
	parentID = nodeSolution.parentID

	#go until we've added the root node
	while(not(parentID == -1)):
		#find the next node in our list based on our parent

		nextNode = getParentNode(parentID)
		
		#add that node to our results
		results.append(nextNode.state)
		#set our new parent node
		parentID = nextNode.parentID
	

	print "this is the final solution item"
	print results
	print "now in correct order"
	print list(reversed((results)))
	

	#return our list in reverse so the first item is our root
	return list(reversed((results)))

#IE InitializeFrontier
#read in the input from the command line
#Declares mode, output file, initializes stateHistory and expanded Nodes count. sets goalBankStates global.
# retrieves input from command line. does error checking. opens and retrieves data from given files. turns retrieved data into a list. Removes the newline character from the end of each list. then creates a list item that contains the state of both banks (goalBankStates and initialBankStates)
#returns the initialBankStates
#TESTED
def getInput():
	global mode, outputFile, stateHistory, goalBankStates, nodeList, currentNodeIndex

	currentNodeIndex = 0
	stateHistory = []
	nodeList = []

	arguments = len(sys.argv)

	#if we don't have correct # of arguments, then exit.
	if arguments != 5:
		print 'Incorrect number of arguments received. Expected 4 additional arguments. Recieved ', (arguments - 1), '\n'
		print 'I accept parameters as follows. <Initial State> <Goal State> <Mode> <Output File>. \nI am now exiting.\n'
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

	#convert string to int since python is stupid
	leftBankGoal[0] = int(leftBankGoal[0])
	leftBankGoal[1] = int(leftBankGoal[1])
	leftBankGoal[2] = int(leftBankGoal[2])

	rightBankGoal[0] = int(rightBankGoal[0])
	rightBankGoal[1] = int(rightBankGoal[1])
	rightBankGoal[2] = int(rightBankGoal[2])

	leftBankInitial[0] = int(leftBankInitial[0])
	leftBankInitial[1] = int(leftBankInitial[1])
	leftBankInitial[2] = int(leftBankInitial[2])

	rightBankInitial[0] = int(rightBankInitial[0])
	rightBankInitial[1] = int(rightBankInitial[1])
	rightBankInitial[2] = int(rightBankInitial[2])
	

	goalBankStates = [leftBankGoal, rightBankGoal]
	initialBankState = [leftBankInitial, rightBankInitial]

	initialNode = Node(currentNodeIndex, initialBankState, -1)
	nodeList.append(initialNode)
	stateHistory.append(initialNode.state)

	currentNodeIndex += 1

	#check if this nodes state is the goal state. 
	if(initialNode.state == goalBankStates):
		result = solution(initialNode)
		writeToOutput(result)#this will exit the program

	#verify we have correct modes
	if (str(mode) == "bfs" or
	    str(mode) == "dfs" or
	    str(mode) == "iddfs" or
	    str(mode) == "astar"):
		
		return initialNode

	else:
		print str(mode), 'is not an acceptable mode. Please use bfs, dfs, iddfs, or astar. Exiting.'
		exit()

#Determines if a boat is heading to the left or not.
def headingLeft(rightState):

	if(operator.eq(rightState,1)):
		return True
	else:
		return False

#Takes in a Node. 
#Determines if the action is an appropriate one.
#Checks that we only move the chicken if there is one to move
#Checks that we won't kill the chickens by taking one of them away
#Checks that it won't die when going to the new side
#Returns the calculated child node.
def actionOneChicken(expandingNode):
	global mode, outputFile, stateHistory, goalBankStates, nodeList, currentNodeIndex

	print "one chicken"

	leftStateResult = CopyState(expandingNode.state[0])
	leftState = CopyState(expandingNode.state[0])
	rightStateResult = CopyState(expandingNode.state[1])
	rightState = CopyState(expandingNode.state[1])

	headLeft = headingLeft(rightState[2])

	if(headLeft):
		print "go left"
		if((operator.ge(rightState[0],1)) and #removing a chicken is valid as there is at least 1 to move
			(
				(operator.eq((rightState[1] + leftState[1]),0)) or #we have no wolves at all, so moving chickens is fine
				(
					(operator.ge((leftState[0] + 1), leftState[1])) and #there isn't more wolves than chickens where we are going
					(
						(operator.ge((rightState[0] - 1), rightState[1])) or #there isn't more wolves than chickens now that the chicken have left
						(operator.eq((rightState[0] - 1), 0))  #there isn't going to be any chickens there
					)
				)
			) 
		  ):
			
			leftStateResult[0] = leftState[0] + 1
			leftStateResult[2] = 1
		 
			rightStateResult[0] = rightState[0] - 1
			rightStateResult[2] = 0

			print leftState, "->",leftStateResult
			print rightState, "->",rightStateResult

		else:
			print "can't do"
			print leftState
			print rightState
			return None#short circuit so we don't save something we shouldn't
	else:
		print "go right"
		
		if((operator.ge(leftState[0],1)) and #removing a chicken is valid as there is at least 1 to move
			(
				(operator.eq((rightState[1] + leftState[1]),0)) or #we have no wolves at all, so moving chickens is fine
				(
					(operator.ge((rightState[0] + 1), rightState[1])) and #there isn't more wolves than chickens where we are going
					(
						(operator.ge((leftState[0] - 1), leftState[1])) or #there isn't more wolves than chickens now that the chicken have left
						(operator.eq((leftState[0] - 1), 0))  #there isn't going to be any chickens there
					)
				)
			) 
		  ):
			
			leftStateResult[0] = leftState[0] -1
			leftStateResult[2] = 0
		
			rightStateResult[0] = rightState[0] + 1
			rightStateResult[2] = 1

			print leftState, "->",leftStateResult
			print rightState, "->",rightStateResult
		else:
			print "can't do"
			print leftState
			print rightState
			return None #short circuit so we don't save something we shouldn't

	state = [leftStateResult, rightStateResult]
	
	#if we'e already evaluated, short circuit
	if(isInStateHistory(state)):
		print "child was in state. Can't do"
		return None
	else:
		
		newNode = Node(currentNodeIndex, state, expandingNode.nodeID)
		currentNodeIndex += 1
		
		return newNode

#Takes in a Node. 
#Determines if the action is an appropriate one.
#Checks that we only move the two chickens if there are two to move
#Checks that they won't die when going to the new side
#Checks that we won't kill the chickens by taking two of them away
#Returns the calculated child node.
def actionTwoChicken(expandingNode):
	global mode, outputFile, stateHistory, goalBankStates, nodeList, currentNodeIndex

	print "two chicken"
	leftStateResult = CopyState(expandingNode.state[0])
	leftState = CopyState(expandingNode.state[0])
	rightStateResult = CopyState(expandingNode.state[1])
	rightState = CopyState(expandingNode.state[1])

	headLeft = headingLeft(rightState[2])

	if(headLeft):
		print "go left"
		if((operator.ge(rightState[0],2)) and #removing a chicken is valid as there is at least 2 to move
			(
				(operator.eq((rightState[1] + leftState[1]),0)) or #we have no wolves at all, so moving chickens is fine
				(
					(operator.ge((leftState[0] + 2), leftState[1])) and #there isn't more wolves than chickens where we are going
					(
						(operator.ge((rightState[0] - 2), rightState[1])) or #there isn't more wolves than chickens now that the chicken have left
						(operator.eq((rightState[0] - 2), 0))  #there isn't going to be any chickens there
					)
				)
			) 
		  ):
			
			leftStateResult[0] = leftState[0] + 2
			leftStateResult[2] = 1
			 
			rightStateResult[0] = rightState[0] - 2
			rightStateResult[2] = 0
			print leftState, "->",leftStateResult
			print rightState, "->",rightStateResult
		else:
			print "can't do"
			print leftState
			print rightState
			return None #short circuit so we don't save something we shouldn't
	else:
		print "go right"

		if((operator.ge(leftState[0],2)) and #removing a chicken is valid as there is at least 2 to move
			(
				(operator.eq((rightState[1] + leftState[1]),0)) or #we have no wolves at all, so moving chickens is fine
				(
					(operator.ge((rightState[0] + 2), rightState[1])) and #there isn't more wolves than chickens where we are going
					(
						(operator.ge((leftState[0] - 2), leftState[1])) or #there isn't more wolves than chickens now that the chicken have left
						(operator.eq((leftState[0] - 2), 0))  #there isn't going to be any chickens there
					)
				)
			) 
		  ): 

			leftStateResult[0] = leftState[0] - 2
			leftStateResult[2] = 0
			 
			rightStateResult[0] = rightState[0] + 2
			rightStateResult[2] = 1
			print leftState, "->",leftStateResult
			print rightState, "->",rightStateResult

		else:
			print "can't do"
			print leftState
			print rightState
			
			return None #short circuit so we don't save something we shouldn't

	state = [leftStateResult, rightStateResult]
			
	#if we'e already evaluated, short circuit
	if(isInStateHistory(state)):
		print "child was in state. Can't do"
		return None
	else:
		
		newNode = Node(currentNodeIndex, state, expandingNode.nodeID)
		currentNodeIndex += 1
		
		return newNode

#Takes in a Node. 
#Determines if the action is an appropriate one.
#Checks that we only move a wolf if there is one to move
#Checks that we won't kill the chickens by adding another wolf to the other side.
#Returns the calculated child node.
def actionOneWolf(expandingNode):
	global mode, outputFile, stateHistory, goalBankStates, nodeList, currentNodeIndex
	print "one wolf"
	
	leftStateResult = CopyState(expandingNode.state[0])
	leftState = CopyState(expandingNode.state[0])
	rightStateResult = CopyState(expandingNode.state[1])
	rightState = CopyState(expandingNode.state[1])

	headLeft = headingLeft(rightState[2])

	if(headLeft):
		print "go left"

		if((operator.ge(rightState[1],1)) and #removing a wolf is valid as there is at least 1 to move
			(
				(operator.eq(leftState[0],0)) or #we don't have any chickens on that side.
				(operator.le((leftState[1] + 1), leftState[0])) #moving the wolves to the left side, won't outweigh the chickens.
			) 
		  ): 

			leftStateResult[1] = leftState[1] + 1
			leftStateResult[2] = 1
			 
			rightStateResult[1] = rightState[1] - 1
			rightStateResult[2] = 0
			print leftState, "->",leftStateResult
			print rightState, "->",rightStateResult
		else:
			print "can't do"
			print leftState
			print rightState

			return None #short circuit so we don't save something we shouldn't
	else:
		print "go right"
		if((operator.ge(leftState[1],1)) and #removing a wolf is valid as there is at least 1 to move
			(
				(operator.eq(rightState[0],0)) or #we don't have any chickens on that side
				(operator.le((rightState[1] + 1), rightState[0])) #moving the wolves to the left side, won't outweigh the chickens.
			) 
		  ): 

			leftStateResult[1] = leftState[1] - 1
			leftStateResult[2] = 0
			 
			rightStateResult[1] = rightState[1] + 1
			rightStateResult[2] = 1
			print leftState, "->",leftStateResult
			print rightState, "->",rightStateResult
		else:
			print leftState
			print rightState
			print "can't do"
			return None#short circuit so we don't save something we shouldn't

	state = [leftStateResult, rightStateResult]
			
	#if we'e already evaluated, short circuit
	if(isInStateHistory(state)):
		print "child was in state. Can't do"
		return None
	else:
		newNode = Node(currentNodeIndex, state, expandingNode.nodeID)
		currentNodeIndex += 1
		
		return newNode

#Takes in a Node. 
#Determines if the action is an appropriate one.
#Checks that we only move a wolf if there is one to move
#Checks that we only move a chicken if there is one to move
#Checks that we won't kill the chickens by adding another wolf to the other side.
#Returns the calculated child node.
def actionOneWolfOneChicken(expandingNode):
	global mode, outputFile, stateHistory, goalBankStates, nodeList, currentNodeIndex
	print "One Chicken One Wolf"

	leftStateResult = CopyState(expandingNode.state[0])
	leftState = CopyState(expandingNode.state[0])
	rightStateResult = CopyState(expandingNode.state[1])
	rightState = CopyState(expandingNode.state[1])

	headLeft = headingLeft(rightState[2])

	if(headLeft):
		print "go left"
		if( (operator.ge(rightState[0],1)) and  #do we have one chicken to even remove from the left side?
			(operator.ge(rightState[1],1)) and  #do we have one wolf to even remove from the left side?
			(operator.le((leftState[1] + 1), (leftState[0] + 1))) #there remains more chickens than wolves on the right side
		  ):
			leftStateResult[0] = leftState[0] + 1
			leftStateResult[1] = leftState[1] + 1
			leftStateResult[2] = 1
			 
			rightStateResult[0] = rightState[0] - 1
			rightStateResult[1] = rightState[1] - 1
			rightStateResult[2] = 0
			print leftState, "->",leftStateResult
			print rightState, "->",rightStateResult
		else:
			print "Can't do"

			print leftState
			print rightState
			
			return None #short circuit so we don't save something we shouldn't
	else:
		print "go right"
		if( (operator.ge(leftState[0],1)) and  #do we have one chicken to even remove from the left side?
			(operator.ge(leftState[1],1)) and  #do we have one wolf to even remove from the left side?
			(operator.le((rightState[1] + 1), (rightState[0] + 1))) #there remains more chickens than wolves on the right side
		  ):

			leftStateResult[0] = leftState[0] - 1
			leftStateResult[1] = leftState[1] - 1
			leftStateResult[2] = 0
			 
			rightStateResult[0] = rightState[0] + 1
			rightStateResult[1] = rightState[1] + 1
			rightStateResult[2] = 1
			print leftState, "->",leftStateResult
			print rightState, "->",rightStateResult
			
		else:
			print "Can't do"

			print leftState
			print rightState
			
			return None #short circuit so we don't save something we shouldn't

	state = [leftStateResult, rightStateResult]
			
	#if we'e already evaluated, short circuit
	if(isInStateHistory(state)):
		print "child was in state. Can't do"
		return None
	else:
		newNode = Node(currentNodeIndex, state, expandingNode.nodeID)
		currentNodeIndex += 1
		
		return newNode

#Takes in a Node. 
#Determines if the action is an appropriate one.
#Checks that we only move two wolves if there are two wolves to move
#Checks that we won't kill the chickens
#Returns the calculated child node.
def actionTwoWolf(expandingNode):
	global mode, outputFile, stateHistory, goalBankStates, nodeList, currentNodeIndex
	print "2 wolf"
	leftStateResult = CopyState(expandingNode.state[0])
	leftState = CopyState(expandingNode.state[0])
	rightStateResult = CopyState(expandingNode.state[1])
	rightState = CopyState(expandingNode.state[1])


	headLeft = headingLeft(rightState[2])

	if(headLeft):

		print "go left"

		if((operator.ge(rightState[1],2)) and #removing two wolves is valid as there is at least 2 to move
			(
				(operator.eq(leftState[0],0)) or #we don't have any chickens on that side.
				(operator.le((leftState[1] + 2), leftState[0]))  #moving the wolves to the left side, won't outweigh the chickens.
			) 
		  ): 

			leftStateResult[1] = leftState[1] + 2
			leftStateResult[2] = 1
			 
			rightStateResult[1] = rightState[1] - 2
			rightStateResult[2] = 0

			print leftState, "->",leftStateResult
			print rightState, "->",rightStateResult
		else:
			print leftState
			print rightState
			print "Can't do"
			
			return None#short circuit so we don't save something we shouldn't

	else:
		print "go right"

		if((operator.gt(leftState[1],1)) and #removing two wolves is valid as there is at least 2 to move
			(
				(operator.eq(rightState[0],0)) or #we don't have any chickens on that side.
				(operator.le((rightState[1] + 2), rightState[0])) #moving the wolves to the right side, won't outweigh the chickens.
			)
		  ): 		

			leftStateResult[1] = leftState[1] - 2
			leftStateResult[2] = 0
			 
			rightStateResult[1] = rightState[1] + 2
			rightStateResult[2] = 1

			print leftState, "->",leftStateResult
			print rightState, "->",rightStateResult
		else:
			print leftState
			print rightState
			print "Can't do"

			return None#short circuit so we don't save something we shouldn't

	state = [leftStateResult, rightStateResult]
			
	#if we'e already evaluated, short circuit
	if(isInStateHistory(state)):
		print "child was in state. Can't do"
		return None
	else:
		newNode = Node(currentNodeIndex, state, expandingNode.nodeID)
		currentNodeIndex += 1
		
		return newNode

#checks to see if we've had this state in the past or not
def isInStateHistory(state):
	if(state in stateHistory):
		return True
	else:
		return False

#takes in a Node
#Determines if it is a node that exists, and if so, whose state we've already evaluated.If so, returns
#Otherwise, will see if the node is our goal state. If so, it will call the solution function
#Else it will append to our list of nodes, and add to the appropriate queue the node before returning.
def evaluateChild(actionNode):
	#checks if the nodes state is already in our history
	if(actionNode == None or isInStateHistory(actionNode.state)):
		return
	else:
		print "i'm evaluating a child"
		#check if this nodes state is the goal state. 
		if(actionNode.state == goalBankStates):
			result = solution(actionNode)
			writeToOutput(result)#this will exit the program
		else:
			nodeList.append(actionNode)
			stateHistory.append(actionNode.state)
			print "child added to state"

			if(mode == "bfs"):
				FIFO.put(actionNode)
			elif(mode == "dfs"):
				LIFO.put(actionNode)
			elif(mode == "iddfs"):
				FIFO.put(actionNode)
				LIFO.put(actionNode)
			else: #astar
				priorityQueue.put(actionNode)
	return

#Breadth-First Search
#FIFO Queue
#Expand all nodes @ a given depth before any nodes at the next level are expanded
#First node is already in the FIFO Queue.
def bfs():
	global expandedNodesCount
	expandedNodesCount = 0
	#Everything short circuits. Assuming Finite set of nodes.
	while(True): 
		if(FIFO.empty()):
			print "I ran out of items"
			writeToOutput(None) #will exit
		else:
			nodeToExpand = FIFO.get()

			expandedNodesCount += 1

			#go through each action
			oneChicken = actionOneChicken(nodeToExpand)
			evaluateChild(oneChicken)
			twoChicken = actionTwoChicken(nodeToExpand)
			evaluateChild(twoChicken)
			oneWolf = actionOneWolf(nodeToExpand)
			evaluateChild(oneWolf)
			oneWolfOneChicken = actionOneWolfOneChicken(nodeToExpand)
			evaluateChild(oneWolfOneChicken)
			twoWolf = actionTwoWolf(nodeToExpand)
			evaluateChild(twoWolf)


				
#Depth-First Search
#LIFO Queue
#Expands the deepest node in the current fringe of the search tree
#First node is already in the LIFO Queue
def dfs():
	global expandedNodesCount
	expandedNodesCount = 0
	#Everything short circuits. Assuming Finite set of nodes.
	while(True): 
		if(LIFO.empty()):
			print "I ran out of items"
			writeToOutput(None) #will exit
		else:
			nodeToExpand = LIFO.get()

			expandedNodesCount += 1

			#go through each action
			oneChicken = actionOneChicken(nodeToExpand)
			evaluateChild(oneChicken)
			twoChicken = actionTwoChicken(nodeToExpand)
			evaluateChild(twoChicken)
			oneWolf = actionOneWolf(nodeToExpand)
			evaluateChild(oneWolf)
			oneWolfOneChicken = actionOneWolfOneChicken(nodeToExpand)
			evaluateChild(oneWolfOneChicken)
			twoWolf = actionTwoWolf(nodeToExpand)
			evaluateChild(twoWolf)


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
	global priorityQueue, FIFO, LIFO

	#state is the initial starting states of the Left bank and Right bank
	firstNode = getInput()
	#tested through initial input. Works correctly.

	if(mode == "bfs"):
		FIFO = Queue.Queue(0)
		FIFO.put(firstNode)

		bfs()
	elif(mode == "dfs"):
		LIFO = Queue.LifoQueue(0)
		LIFO.put(firstNode)

		dfs()
	elif(mode == "iddfs"):
		LIFO = Queue.LifoQueue(0)
		FIFO = Queue.Queue(0)
		FIFO.put(firstNode)
		LIFO.put(firstNode)

		iddfs()
	else: #astar
		priorityQueue = Queue.PriorityQueue(0)
		priorityQueue.Put(firstNode)

		astar()

main()
