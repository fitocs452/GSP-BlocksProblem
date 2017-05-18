class State:
    """
    Clase estado, muy tecnicamente es un conjunto de TrueSentence
    """

    def __init__(self, trueSentenceList, groundTermList):
        self.trueSentenceList = list(trueSentenceList)
        self.groundTermList = list(groundTermList)
        self.prevState = None
        self.prevAction = None
        self.prevAssignments = None
        self.prevPrintData = ''
        self.depth = 0
        self.heuristicValue = 0
        # print(trueSentenceList)
        # print(groundTermList)

    def tracePath(self):
        """
        Retorna {
            outputString: Acciones a seguir en orden para resolver problema
            stateList: Lista de las acciones seguidas para resolver problema
        }
        """

        pathList = []
        current = self

        while current:
            pathList.append(current)
            current = current.prevState

        pathList.reverse()

        retStr = ''
        for state in pathList:
            retStr += state.prevPrintData + '\n'

        retDict = dict()
        retDict['outputString'] = retStr.strip()
        retDict['stateList'] = pathList

        return retDict

    def addTrueSentence(self, trueSentence):
        """
        Agregar una trueSentence
        """

        for arg in trueSentence.argList:
            if arg.isVariable():
                return

        for arg in trueSentence.argList:
            alreadyPresent = False
            for selfArg in self.groundTermList:
                if arg == selfArg:
                    alreadyPresent = True
                    break
            if not alreadyPresent:
                self.groundTermList.append(arg)

        self.trueSentenceList.append(trueSentence)

    def removeTrueSentence(self, trueSentenceArg):
        """
        Elimina todas las trueSentence iguales
        """

        self.trueSentenceList = [
            trueSentence for trueSentence in self.trueSentenceList
            if not trueSentence == trueSentenceArg
        ]

    def hasTrueSentences(self, trueSentenceList):
        """
        Verifica si el estado contiene todas las TrueSentence
        """

        for newSentence in trueSentenceList:
            isPresent = False
            for selfSentence in self.trueSentenceList:
                if selfSentence == newSentence:
                    isPresent = True
                    break
            if not isPresent:
                return False

        return True

    def isGoalState(self, goalState, inHeuristicMode=False):
        """
        Verifica si el estado es el goalState
        """

        if not inHeuristicMode:
            return goalState == self
        else:
            return self.hasTrueSentences(goalState.trueSentenceList)

    def __eq__(self, other):
        """
        Igualdad: Lista de TrueSentence iguales
        """

        return cmpListNoOrder(self.trueSentenceList, other.trueSentenceList)

    def __ne__(self, other):
        """
        Desigualdad: !Igualdad
        """

        return not self.__eq__(other)

    def __str__(self):
        toString = ''

        for trueSentence in self.trueSentenceList:
            toString += str(trueSentence) + ' \n'

        toString += 'Previous Action : ' + self.prevPrintData + '\n' \
            + str(self.prevAction)
        return toString

    def getNextStates(self, actionList, inHeuristicMode=False):
        """
        Retorna todos los posibles nuevos estados (Cada nuevo estado se genera
        a partir de la aplicacion de una accion)
        """

        retList = []

        for action in actionList:
            retList.extend(
                action.getStatesOnApplication(self, inHeuristicMode)
            )

        return retList


def cmpListNoOrder(first, second):
    """
    "Deep" compares two lists. Returns `True` of they are equal, and
    `False` otherwise.
    Order of elements in the lists does not matter.
    """

    if not len(first) == len(second):
        return False

    dupFirst = list(first)
    dupSecond = list(second)

    for item in dupFirst:
        exists = False
        itemInList = None
        for other in dupSecond:
            if item == other:
                exists = True
                itemInList = other
                break

        if not exists:
            return False

        dupSecond.remove(itemInList)

    return True
