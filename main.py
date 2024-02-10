import re

import numpy as np

from Executor import Executor
from Parser import Parser
from Lexer import Lexer
from token_types.Operator import Operator


def main():
    # a = Operator("=")
    # print(a)
    executor = Executor()
    while True:
        instructions = input()
        lexer = Lexer(instructions)
        parsed = Parser(lexer).process_all_tokens()
        executor.execute_instructions(parsed)
        print(f"{executor.stack}")


if __name__ == "__main__":
    main()
