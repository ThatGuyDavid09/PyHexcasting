from token_types.NumberLiteral import NumberLiteral


class VectorLiteral(NumberLiteral):
    def __init__(self, arr):
        super().__init__(0)
        self.value = arr
