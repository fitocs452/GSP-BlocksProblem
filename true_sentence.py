import random
from proposition import PropositionTypes


class TrueSentence:
    """
    Es una clase que representa un predicado
    """

    def __init__(self, propositionType, argList, isNegation=False):
        self.propositionType = propositionType
        self.argList = list(argList)
        self.isNegation = isNegation
        self.truthValue = False

    def __eq__(self, other):
        """
        Evaluamos la igualdad:
            - Proposicion (OnTable ....)
            - Si esta negado el predicado
            - Lista de argumentos
        """

        return self.propositionType == other.propositionType \
            and self.isNegation == other.isNegation \
            and cmpListWithOrder(self.argList, other.argList)

    def __ne__(self, other):
        """
        Desigualdad: !Igualdad
        """

        return not self.__eq__(other)

    def __str__(self):
        toString = ''

        if self.isNegation:
            toString += '~'

        toString += '('
        toString += self.propositionType

        for arg in self.argList:
            toString += ' '
            toString += str(arg)
        toString = toString.strip()
        toString += ') '

        return toString

    def getNewGoals(self, currState, actionList):
        """
        Devolvemos los siguientes pasos a resolver:
            - Predicados
            - Accion para que se cumpla (No aplicada todavia)
            - Argumentos (Assignments)
            - Estado actual
            - Lista de acciones de bloques
        """

        pickAction = actionList[0]
        unstackAction = actionList[1]
        releaseAction = actionList[2]
        stackAction = actionList[3]

        retDict = {}
        assignments = {}

        possibleAssignments = list(currState.groundTermList)
        if self.propositionType == PropositionTypes.ON:
            nextAction = stackAction
        elif self.propositionType == PropositionTypes.ONTABLE:
            nextAction = releaseAction
        elif self.propositionType == PropositionTypes.EMPTY:
            nextAction = releaseAction
        elif self.propositionType == PropositionTypes.HOLD:
            checkSentence = TrueSentence(PropositionTypes.ONTABLE, self.argList, False)
            if currState.hasTrueSentences([checkSentence]):
                nextAction = pickAction
            else:
                nextAction = unstackAction
        elif self.propositionType == PropositionTypes.CLEAR:
            checkSentence = TrueSentence(PropositionTypes.HOLD, self.argList, False)
            if currState.hasTrueSentences([checkSentence]):
                nextAction = releaseAction
            else:
                nextAction = unstackAction
        else:
            return None

        for trueSentence in nextAction.effectList:
            if trueSentence.propositionType == self.propositionType \
                    and self.isNegation == trueSentence.isNegation:
                for ii in range(len(self.argList)):
                    assignments[trueSentence.argList[ii].value] = self.argList[ii]
                if nextAction == unstackAction:
                    if self.propositionType == PropositionTypes.HOLD:
                        for terminal in possibleAssignments:
                            checkSentence = TrueSentence(PropositionTypes.ON, [self.argList[0], terminal], False)
                            if currState.hasTrueSentences([checkSentence]):
                                possibleAssignments = [terminal]
                                break
                    elif self.propositionType == PropositionTypes.CLEAR:
                        for terminal in possibleAssignments:
                            checkSentence = TrueSentence(PropositionTypes.ON, [terminal, self.argList[0]], False)
                            if currState.hasTrueSentences([checkSentence]):
                                possibleAssignments = [terminal]
                                break
                    else:
                        return None
                elif self.propositionType == PropositionTypes.EMPTY:
                    for terminal in possibleAssignments:
                            checkSentence = TrueSentence(PropositionTypes.HOLD, [terminal], False)
                            if currState.hasTrueSentences([checkSentence]):
                                possibleAssignments = [terminal]
                                break

                break

        retDict['action'] = nextAction

        for arg in nextAction.variableTermList:
            if not assignments.has_key(arg.value):
                if len(possibleAssignments) == 0:
                    break
                randomIndex = random.randrange(0, len(possibleAssignments))
                assignments[arg.value] = possibleAssignments[randomIndex]
                possibleAssignments.pop(randomIndex)

        retDict['assignments'] = assignments

        retTrueList = []
        for trueSentence in nextAction.preconditionList:
            assignedSentence = TrueSentence(trueSentence.propositionType, \
                    trueSentence.argList, trueSentence.isNegation)
            newArgList = []
            for arg in assignedSentence.argList:
                if arg.isVariable():
                    newArgList.append(assignments[arg.value])
                else:
                    newArgList.append(arg)
            assignedSentence.argList = newArgList
            retTrueList.append(assignedSentence)

        retDict['trueSentenceList'] = retTrueList

        print('**********************************')
        print("*** Siguiente estado ***")
        # print("State:")
        # print(currState)
        # print("Input:")
        # print(self)
        printDict(retDict)

        return retDict


def printDict(currentDict):
    """
    Prints a dictionary properly.
    """

    for key in currentDict.keys():
        print(str(key) + ': ')
        if type(currentDict[key]) is list:
            printList(currentDict[key])
        elif type(currentDict[key]) is dict:
            printDict(currentDict[key])
        else:
            print(str(currentDict[key]))

        print("")


def cmpListWithOrder(first, second):
    """
    "Deep" compares two lists. Returns `True` of they are equal, and
    `False` otherwise.
    Order of elements in the lists matters.
    """

    if not len(first) == len(second):
        return False

    dupFirst = list(first)
    dupSecond = list(second)

    for ii, item in enumerate(dupFirst):
        if item != dupSecond[ii]:
            return False

    return True


def printList(currentList):
    """
    Prints a list properly.
    """

    for item in currentList:
        if type(item) is list:
            printList(item)
        elif type(item) is dict:
            printDict(item)
        else:
            print(item)

    print("")
