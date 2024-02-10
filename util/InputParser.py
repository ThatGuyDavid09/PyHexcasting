from Lexer import Lexer
from Parser import Parser


class InputParser:
    @staticmethod
    def parse_input(user_input):
        parsed = InputParser.parse_input_rec(user_input)
        return parsed

    @staticmethod
    def parse_input_rec(user_input):
        user_input = str(user_input)
        if user_input == "EOF":
            return None
        try:
            if user_input in "\\()+-*^/|!==<=>=":
                pass
            else:
                user_input = eval(user_input)
        except NameError:
            pass
        if isinstance(user_input, list):
            lst = []
            for item in user_input:
                parsed = InputParser.parse_input_rec(item)
                lst.append(parsed)
            return lst
        else:
            # lexer = Lexer(user_input)
            parsed, _ = Parser().parse_token(user_input)
            return parsed
