from state import State
from true_sentence import TrueSentence


class Action:
    """
    Clase que representa una accion
    """

    def __init__(self, name, argList, preconditionList, effectList):
        self.name = name
        self.argList = argList
        self.preconditionList = list(preconditionList)
        self.effectList = list(effectList)
        self.variableTermList = []

        # Listado de argumentos en lista de precondiciones
        for precondition in preconditionList:
            for arg in precondition.argList:
                alreadyPresent = False
                for selfArg in self.variableTermList:
                    if arg == selfArg:
                        alreadyPresent = True
                        break
                if not alreadyPresent:
                    self.variableTermList.append(arg)

    def __str__(self):
        toString = 'Action : ' + self.name + '\n'
        toString += 'Pre: '
        for item in self.preconditionList:
            toString += str(item)
        toString += '\n'
        toString += 'Eff: '
        for item in self.effectList:
            toString += str(item)
        toString += '\n'

        return toString

    def getStateOnActionUtil(self, stateObject, assignments, inHeuristicMode=False):
        """
        Aplica nuestra accion al estado:
            Devuelve:
                Argumentos (Assignments)
                Nuevo estado
        """
        retState = State(stateObject.trueSentenceList,
                         stateObject.groundTermList)
        for trueSentence in self.effectList:
            newTrueSentence = \
                TrueSentence(trueSentence.propositionType, [])
            groundTermList = []
            for variable in trueSentence.argList:
                savedArg = assignments[variable.value]
                groundTermList.append(savedArg)

            newTrueSentence.argList = groundTermList
            if trueSentence.isNegation:
                if not inHeuristicMode:
                    retState.removeTrueSentence(newTrueSentence)
            else:
                retState.addTrueSentence(newTrueSentence)

        retState.prevAction = self
        retState.prevAssignments = dict(assignments)
        argListString = ''
        for arg in self.argList:
            argListString += ' ' + str(assignments[arg])

        retState.prevPrintData = '(' + self.name + argListString + ')'
        if inHeuristicMode:
            retState.heuristicValue = stateObject.heuristicValue + 1
        return retState
