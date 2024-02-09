class Lexer:
    def __init__(self, program):
        self.tokens = program.split(" ")

    def next_token(self):
        if len(self.tokens) > 0:
            return self.tokens.pop(0)
        else:
            return "\n"
