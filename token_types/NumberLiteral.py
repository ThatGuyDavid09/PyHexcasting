class NumberLiteral:
    def __init__(self, value):
        self.value = float(value)

    def __str__(self):
        return f"Literal {str(self.value)}"

    def __repr__(self):
        return f"<{self.__str__()}>"
