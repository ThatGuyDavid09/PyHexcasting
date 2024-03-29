import numpy as np

from errors.HexCastSyntaxError import HexCastSyntaxError
from errors.PyHexCastError import PyHexCastError
from token_types.DropKeep import DropKeep
from token_types.NumberLiteral import NumberLiteral
from token_types.Operator import Operator
from token_types.VectorLiteral import VectorLiteral


class Parser:
    def __init__(self, lexer=None):
        self.lexer = lexer

    def process_all_tokens(self):
        tokens = []
        while True:
            token = self.lexer.next_token()
            parsed_token, is_next = self.parse_token(token)
            if isinstance(parsed_token, PyHexCastError):
                tokens = parsed_token
                return tokens

            if tokens != "EOF":
                tokens.append(parsed_token)

            if not is_next:
                break
        return tokens

    def parse_token(self, token):
        token = str(token)
        if token == "\n":
            return "EOF", False
        if token.replace('.', '').isnumeric():
            return NumberLiteral(float(token)), True

        token = token.replace("vector", "vec")
        if "vec([" in token or "np.array" in token:
            token = token.replace("vector", "vec")
            token = token.replace("vec", "np.array")
            return VectorLiteral(eval(token)), True

        # Operators are not case sensitive and some common replacements
        token = token.lower()
        token = token.replace("list", "lst")
        token = token.replace("vector", "vec")
        token = token.replace("make", "mk")
        token = token.replace("clear", "clr")

        mapping = {
            "add": "+",
            "sub": "-",
            "mul": "*",
            "div": "/",
            "abs": "|",
            "mag": "|",
            "pwr": "^",
            "power": "^",
            "eq": "=",
            "==": "=",
            "not_eq": "!=",
            "neq": "!=",
            "gt": ">",
            "lt": "<",
            "ge": ">=",
            "geq": ">=",
            "le": "<=",
            "leq": "<="
        }

        mapped = mapping.get(token, token)
        token = mapped

        # Handle drop_keep specifically
        if token[:3] == "dk_":
            try:
                to_ret = DropKeep(token)
            except ValueError:
                return HexCastSyntaxError(f"\"{token}\" is invalid drop_keep syntax"), False
            return to_ret, True

        try:
            to_ret = Operator(token)
        except ValueError:
            return HexCastSyntaxError(f"\"{token}\" is an invalid operator"), False
        return to_ret, True
