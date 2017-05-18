#!/usr/bin/python
# -*- coding: utf-8 -*-

# Adolfo Morales 13014

from __future__ import print_function
import sys
import time
import random

from arg_types import ArgTypes
from arg import Arg
from world_actions import getActions
from state import State
from true_sentence import TrueSentence


def gsp(startState, goalState, actionList):
    stack = []
    currentState = State(startState.trueSentenceList, startState.groundTermList)
    planList = []

    stack.append(goalState.trueSentenceList)
    for trueSentence in goalState.trueSentenceList:
        stack.append([trueSentence])

    while len(stack) > 0:
        print(str(len(planList)).zfill(3), end="\r")
        poppedElement = stack.pop()

        if type(poppedElement) is list:

            if not currentState.hasTrueSentences(poppedElement):

                if len(poppedElement) > 1:
                    stack.append(poppedElement)
                    random.shuffle(poppedElement)
                    for trueSentence in poppedElement:
                        stack.append([trueSentence])

                # Acciones relevantes
                else:
                    newGoalsData = poppedElement[0].getNewGoals(currentState, actionList)

                    if newGoalsData == None:
                        stack = []
                        currentState = State(startState.trueSentenceList, startState.groundTermList)
                        planList = []
                        stack.append(goalState.trueSentenceList)
                        for trueSentence in goalState.trueSentenceList:
                            stack.append([trueSentence])

                        continue

                    actionDict = dict()
                    actionDict['action'] = newGoalsData['action']
                    actionDict['assignments'] = newGoalsData['assignments']
                    stack.append(actionDict)
                    stack.append(newGoalsData['trueSentenceList'])

                    for trueSentence in newGoalsData['trueSentenceList']:
                        stack.append([trueSentence])
        else:
            action = poppedElement['action']
            assignments = poppedElement['assignments']
            currentState = action.getStateOnActionUtil(currentState, assignments)
            planList.append(poppedElement)

    return planList


def readFile(fileName):
    """
    Returns a dictionary with initial state, final state and
    the "mode" of operation as read from the `fileName` file.
    Keys in dictionary are:
    'planner', 'initState', 'goalState'.
    """

    retDict = {}

    with open(fileName) as inFile:
        lines = inFile.readlines()
        lines = [line.strip() for line in lines]

        try:
            numberBlocks = int(lines[0])
        except ValueError:
            print('Please tell me the number of blocks!')
            return None
        completeBlockList = []
        for i in range(1, numberBlocks + 1):
            completeBlockList.append(Arg(ArgTypes.TERMINAL, i, False))

        if not lines[1] == 'initial':
            print("Don't know from where the initial state starts!")
            return None

        # Definimos nuestro primer estado vacio
        initState = State([], [])
        words = lines[2].split()
        argList = []
        propositionType = None
        for word in words:
            if word[0] == '(':
                argList = []
                propositionType = word.strip('(')
            else:
                try:
                    argList.append(completeBlockList[int(word.strip(')')) - 1])
                except:
                    print("Sorry! Can't read the file!")
                    return None
            if word[-1] == ')':
                initState.addTrueSentence(TrueSentence(propositionType.strip(')'), argList))

        retDict['initState'] = initState

        if not lines[3] == 'goal':
            print("Don't know from where the goal state starts!")
            return None

        goalState = State([], [])
        words = lines[4].split()
        argList = []
        propositionType = None
        isNegation = False
        for word in words:
            if word[0] == '~':
                isNegation = True
                word = word.strip('~')

            if word[0] == '(':
                argList = []
                propositionType = word.strip('(')
            else:
                try:
                    argList.append(completeBlockList[int(word.strip(')')) - 1])
                except:
                    print("Sorry! Can't read the file!")
                    return None
            if word[-1] == ')':
                goalState.addTrueSentence(TrueSentence(propositionType.strip(')'), argList, isNegation))
                isNegation = False

        retDict['goalState'] = goalState
        return retDict


def writeFile(fileName, numActions, outputString):
    """
    Writes `outputString` to the given file.
    `fileName` is the pathname of the file to write to.
    """

    fileName = fileName.replace("tests/", "output/")
    f = open(fileName, 'w')
    f.write(str(numActions) + '\n')
    f.write(outputString)
    f.close()

    return fileName


def main():
    """
    Take input argument (a file name), and write soduko solutions
    to a file.
    """

    if len(sys.argv) < 2:
        print('Invalid/insufficient arguments!')
    else:
        actionList = getActions()
        fileName = str(sys.argv[1])
        readData = readFile(fileName)
        outputString = ''
        numActions = 0

        initTime = time.time()

        gspPlanList = gsp(readData['initState'], readData['goalState'], actionList)
        for stage in gspPlanList:
            action = stage['action']
            assignments = stage['assignments']
            argListString = ''
            for arg in action.argList:
                argListString += ' ' + str(assignments[arg])
            outputString += '(' + action.name + argListString + ')' + '\n'
        numActions = len(gspPlanList)

        duration = time.time() - initTime

        if len(outputString) > 0:
            fileName = writeFile(fileName[:-4] + '_out.txt', numActions, outputString)
        else:
            print('Error in searching for a plan: no output from planner!')

        print('\r..........................................................')
        print('Planner: GPS')
        print('Time: ' + str(duration))
        print('Plan length: ' + str(numActions))
        print('Output written to: "' + str(fileName[:-4] + '_out.txt"'))
        print('..........................................................')

    return


main()
