import re

from Executor import Executor
from Parser import Parser
from token_types.Operator import Operator


def main():
    # a = Operator("=")
    # print(a)
    executor = Executor()
    parser = Parser()
    while True:
        instruction = input()
        parsed, _ = parser.parse_token(instruction)
        executor.execute_instruction(parsed)
        print(f"{executor.stack}")


if __name__ == "__main__":
    main()
