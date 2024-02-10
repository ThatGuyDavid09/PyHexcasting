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
        # try:
        lexer = Lexer(instructions)
        parsed = Parser(lexer).process_all_tokens()
        executor.execute_instructions(parsed)
        # except Exception as e:
        #     print("Exception at parsing")
        #     print("    " + str(e))
        #     continue

        if executor.temporary is not None:
            print(f"Temp - {executor.temporary}")
        for i in executor.stack[::-1]:
            print(f"{i}")


if __name__ == "__main__":
    main()
