from arg_types import ArgTypes


class Arg:
    """
    Argumentos
    """

    def __init__(self, argType, argValue, isNegation):
        # Tipo de argumento: (Terminal | Variable)
        self.type = argType

        # Valor del argumento
        self.value = argValue

        # En caso es una negacion (!)
        self.isNegation = isNegation

    def __str__(self):
        toString = ''

        if self.isNegation:
            toString += '~'

        if self.type == ArgTypes.TERMINAL:
            # print('isTerminal', self.value)
            toString += str(self.value).upper()
        else:
            # print('isNotTerminal', self.value)
            toString += str(self.value).lower()

        return toString

    def isVariable(self):
        """
        Retorna true, en caso sea una variable
        """

        return self.type == ArgTypes.VARIABLE

    def __eq__(self, other):
        """
        Comparacion entre Argumentos para verificar igualdad
            - Verifica tipo
            - Verifica valor
            - Verifica negacion
        """

        same_type = self.type == other.type
        same_value = self.value == other.value
        same_negation = self.isNegation == other.isNegation

        return same_type and same_value and same_negation

    def __ne__(self, other):
        """
        Verifica desigualdad de Argumentos (!iguales)
        """

        return not self.__eq__(other)
