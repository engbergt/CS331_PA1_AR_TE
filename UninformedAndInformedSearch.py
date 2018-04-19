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

#IE InitializeFrontier
#read in the input from the command line
def getInput():
	global mode, outputFile, leftBankState, rightBankState, leftBankGoal, rightBankGoal
	global leftBankInitial, rightBankInitial
	global expandedNodesCount, stateHistory

	expandedNodesCount = 0
	stateHistory = []
	stateHistory.Append([leftBankInitial, rightBankInitial])

	arguments = len(sys.argv)
	bfs = 'bfs'
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


	#set our initials and goal states
	leftBankInitial = initialState.readline().split(",")
	rightBankInitial = initialState.readline().split(",")

	#removal of newline character on last element
	leftBankInitial[-1] = leftBankInitial[-1].strip()
	rightBankInitial[-1] = rightBankInitial[-1].strip()


	leftBankState = leftBankInitial
	rightBankState = rightBankInitial

	leftBankGoal = goalState.readline().split(",")
	rightBankGoal = goalState.readline().split(",")
	
	#removal of newline character on last element
	leftBankGoal[-1] = leftBankGoal[-1].strip()
	rightBankGoal[-1] = rightBankGoal[-1].strip()

	initialState.close()
	goalState.close()

	#verify we have correct modes
	if (str(mode) == "bfs" or
	    str(mode) == "dfs" or
	    str(mode) == "iddfs" or
	    str(mode) == "astar"):
		return
	else:
		print str(mode), 'is not an acceptable mode. Please use bfs, dfs, iddfs, or astar. Exiting.'
		exit()

#do one of five actions 
#    Put one chicken in the boat
#    Put two chickens in the boat
#    Put one wolf in the boat
#    Put one wolf and one chicken in the boat
#    Put two wolves in the boat 
def action(mode, leftState, rightState):

	tempLeftState = leftState
	tempRightState = rightState

	#if boat is on the right side, we are heading left
	if(rightState[2] == 1):
		headLeft = True

	#1CM = 1 chicken moved
	#put one chicken in the boat
	leftBankState1CM = tempLeftState
	rightBankState1CM = tempRightState

	if(headLeft):
		if(gt(tempRightState[0], 0) and 
		   ge((tempRightState[0] - 1), tempRightState[1])) and #if we remove a chicken from the right side, will the chickens left live?
		   ge(tempLeftState[0] + 1, tempLeftState[1]): #will we have an OK number of chickens on the left side as well?
			
			leftBankState1CM[0] = tempLeftState[0] + 1
			leftBankState1CM[2] = 1
		 
			rightBankState1CM[0] = tempRightState[0] - 1
			rightBankState1CM[2] = 0

		else:
			#we've got nothing
			leftBankState1CM = None
			rightBankState1CM = None
	else:
		if(gt(tempLeftState[0],0) and
		   ge((tempLeftState[0] - 1), tempLeftState[1])) and #if we remove a chicken from the left side, will the chickens remaining survive
		   ge((tempRightState[0] + 1), tempRightState[1]): #will there be enough chickens on the right side for our chickens to survive?
			
			leftBankState1CM[0] = tempLeftState[0] -1
			leftBankState1CM[2] = 0
		
			rightBankState1CM[0] = tempRightState[0] + 1
			rightBankState1CM[2] = 1

		else:
			#we've got nothing
			leftBankState1CM = None
			rightBankState1CM = None

	#2CM = 2 chickens moved
	#put two chickens in the boat
	leftBankState2CM = tempLeftState
	rightBankState2CM = tempRightState

	if(headLeft):
		if(gt(tempRightState[0],1) and
		   ge((tempRightState[0] - 2), tempRightState[1])) and #if we remove 2 chickens from the right side, will the remaining chickens survive?
		   ge((tempLeftState[0] + 2), tempLeftState[1]): #do we have enough chickens in order to survive being moved to this side?
			
			leftBankState2CM[0] = tempLeftState[0] + 2
			leftBankState2CM[2] = 1
			 
			rightBankState2CM[0] = tempRightState[0] - 2
			rightBankState2CM[2] = 0

		else:
			leftBankState2CM = None
			rightBankState2CM = None
	else:
		if(gt(tempLeftState[0],1) and
		   ge((tempLeftState[0] - 2), tempLeftState[1])) and #if we remove 2 chickens from the left side, will the remaining chickens surivie
		   ge((tempRightState[0] + 2), tempRightState[1]): #do we have enough chickens in order to survive the right side

			leftBankState2CM[0] = tempLeftState[0] - 2
			leftBankState2CM[2] = 0
			 
			rightBankState2CM[0] = tempRightState[0] + 2
			rightBankState2CM[2] = 1

		else:
			leftBankState2CM = None
			rightBankState2CM = None

	#1WM = 1 wolf moved
	#put one wolf in the boat
	leftBankState1WM = tempLeftState
	rightBankState1WM = tempRightState	

	if(headLeft):
		if(gt(tempRightState[1],0) and
		   le((tempLeftState[1] + 1), tempLeftState[0])): #by adding another wolf to the left side, do we outweight the chickens?

			leftBankState1WM[1] = tempLeftState[1] + 1
			leftBankState1WM[2] = 1
			 
			rightBankState1WM[1] = tempRightState[1] - 1
			rightBankState1WM[2] = 0

		else:
			leftBankState1WM = None
			rightBankState1WM = None
	else:
		if(gt(tempLeftState[1],0) and
		   le((tempRightState[1] + 1), tempRightState[0])): #by adding another wolf to the right bank, do we outweight the chickens?

			leftBankState1WM[1] = tempLeftState[1] - 1
			leftBankState1WM[2] = 0
			 
			rightBankState1WM[1] = tempRightState[1] + 1
			rightBankState1WM[2] = 1

		else:
			leftBankState1WM = None
			rightBankState1WM = None

	#1CWM = 1 chicken and 1 wolf moved
	#put one wolf and one chicken in the boat
	leftBankState1CWM = tempLeftState
	rightBankState1CWM = tempRightState
	
	if(headLeft):
		if(gt(tempRightState[0],0) and gt(tempRightState[1],0) and
		   ge((tempLeftState[0] + 1), (tempLeftState[1] + 1))): #if there are more wolves than chickens on the left side now, then goodbye chicken added

			leftBankState1CWM[0] = tempLeftState[0] + 1
			leftBankState1CWM[1] = tempLeftState[1] + 1
			leftBankState1CWM[2] = 1
			 
			rightBankState1CWM[0] = tempRightState[0] - 1
			rightBankState1CWM[1] = tempRightState[1] - 1
			rightBankState1CWM[2] = 0

		else:
			leftBankState1CWM = None
			rightBankState1CWM = None
	else:
		if(gt(tempLeftState[0],0) and gt(tempLeftState[1],0) and
		   ge((tempRightState[0] + 1), (tempRightState[1] + 1))):#if there are more wolves than chickens on the left side now, then goodbye chicken added

			leftBankState1CWM[0] = tempLeftState[0] - 1
			leftBankState1CWM[1] = tempLeftState[1] - 1
			leftBankState1CWM[2] = 0
			 
			rightBankState1CWM[0] = tempRightState[0] + 1
			rightBankState1CWM[1] = tempRightState[1] + 1
			rightBankState1CWM[2] = 1

		else:
			leftBankState1CWM = None
			rightBankState1CWM = None

	#put two wolves in the boat
	#2WM = 2 wolves moved
	leftBankState2WM = tempLeftState
	rightBankState2WM = tempRightState
	
	if(headLeft):
		if(gt(tempRightState[1],1) and 
		   le((tempLeftState[1] + 2), tempLeftState[0])): #by adding two wolves to the left side, do wolves then outweigh chickens?

			leftBankState2WM[1] = tempLeftState[1] + 2
			leftBankState2WM[2] = 1
			 
			rightBankState2WM[1] = tempRightState[1] - 2
			rightBankState2WM[2] = 0

		else:
			leftBankState2WM = None
			rightBankState2WM = None
	else:
		if(gt(tempLeftState,1) and 
		   le((tempRightState[1] + 2), tempRightState[0])): #by adding two wolves to the right side, do wolves outweight chickens?			

			leftBankState2WM[1] = tempLeftState[1] - 2
			leftBankState2WM[2] = 0
			 
			rightBankState2WM[1] = tempRightState[1] + 2
			rightBankState2WM[2] = 1

		else:
			leftBankState2WM = None
			rightBankState2WM = None

    #TODO Add everything to either a lifo or fifo

	return

#Breadth-First Search
#FIFO Queue
#Expand all nodes @ a given depth before any nodes at the next level are expanded
def bfs():
	global fifo
	solutionFound = False

	fifo = Queue()
	fifo.put([leftBankState, rightBankState])

	#verify that this is putting these in as a pair
	while(solutionFound is False):
		if(fifo.Empty):
			print noSolution
			#TODO write to output file w/ noSolution	
			exit()
		nodeToExpand = fifo.get()


		#check if this node is the goal state. if not. continue
		#else print it
		if():
		else:
			stateHistory.Append(nodeToExpand) #add to history
#Depth-First Search
#LIFO Queue
#Expands the deepest node in the current fringe of the search tree
def dfs():
	global lifo
	global expandedNodesCount

	lifo = LifoQueue()


	return

#Iterative Deepening Depth First
#Do Depth First with depth limit, iterate up depth limit until a goal is found.
#Merge of depth and breadth
def iddfs():
	global expandedNodesCount

	return


def astar():
global expandedNodesCount


	return

def main():
	global noSolution
	noSolution = "No solution found."

	getInput()
	if(mode == "bfs"):
		bfs()
	elif(mode == "dfs"):
		dfs()
	elif(mode == "iddfs"):
		iddfs()
	else: #astar
		astar()

main()