from token_types.NumberLiteral import NumberLiteral
from token_types.Operator import Operator


class Executor:
    def __init__(self, instructions=None):
        self.instructions = instructions
        self.stack = []
        self.temporary = None

    def execute_instuctions(self):
        for instruction in self.instructions:
            self.execute_instruction(instruction)

    def execute_instruction(self, instruction):
        if isinstance(instruction, NumberLiteral):
            self.stack.append(instruction.value)

        if instruction == Operator.ADD:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(a + b)
        elif instruction == Operator.SUB:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b - a)
        elif instruction == Operator.MUL:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(a * b)
        elif instruction == Operator.DIV:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b / a)
