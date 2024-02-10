import math
import random

import numpy as np

from errors.PyHexCastError import PyHexCastError
from token_types.NumberLiteral import NumberLiteral
from token_types.Operator import Operator
from util.LehrerDecoder import permute_end_of_list


class Executor:
    def __init__(self):
        self.stack = []
        self.temporary = None

    def execute_instructions(self, instructions):
        if isinstance(instructions, PyHexCastError):
            raise instructions
        for instruction in instructions:
            self.execute_instruction(instruction)

    def execute_instruction(self, instruction):
        if isinstance(instruction, NumberLiteral):
            self.stack.append(instruction.value)

        # Simple math
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
            if isinstance(a, np.ndarray) and isinstance(a, np.ndarray):
                self.stack.append(b.dot(a))
            else:
                self.stack.append(b * a)
        elif instruction == Operator.DIV:
            a = self.stack.pop()
            b = self.stack.pop()
            if isinstance(a, np.ndarray) and isinstance(a, np.ndarray):
                self.stack.append(b.cross(a))
            else:
                self.stack.append(b / a)
        elif instruction == Operator.MAG:
            a = self.stack.pop()
            if isinstance(a, np.ndarray):
                self.stack.append(np.linalg.norm(a))
            else:
                self.stack.append(abs(a))
        elif instruction == Operator.PWR:
            a = self.stack.pop()
            b = self.stack.pop()
            if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
                self.stack.append(a * np.dot(b, a) / np.dot(b, b))
            else:
                self.stack.append(b ** a)
        elif instruction == Operator.FLR:
            a = self.stack.pop()
            self.stack.append(math.floor(a))
        elif instruction == Operator.CEIL:
            a = self.stack.pop()
            self.stack.append(math.ceil(a))
        elif instruction == Operator.VCTR_MK:
            x = self.stack.pop()
            y = self.stack.pop()
            z = self.stack.pop()
            self.stack.append(np.array([x, y, z]))
        elif instruction == Operator.VCTR_UNMK:
            a = self.stack.pop()
            self.stack.extend([a.x, a.y, a.z])
        elif instruction == Operator.MOD:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b % a)
        elif instruction == Operator.AXIS:
            a = self.stack.pop()
            if isinstance(a, np.ndarray):
                if np.array_equal(a, np.array([0, 0, 0])):
                    self.stack.append(a)
                    return

                axes_vectors = [
                    np.array([1, 0, 0]),
                    np.array([0, 1, 0]),
                    np.array([0, 0, 1]),
                    np.array([-1, 0, 0]),
                    np.array([0, -1, 0]),
                    np.array([0, 0, -1])
                ]
                dot_products = [np.dot(a.flatten(), axis_vector) for axis_vector in axes_vectors]
                closest_axis_index = np.argmax(dot_products)
                self.stack.append(axes_vectors[closest_axis_index])
            else:
                if a == 0:
                    self.stack.append(0)
                else:
                    self.stack.append(-1 if a < 0 else 1)
        elif instruction == Operator.RANDOM:
            self.stack.append(random.random())

        # Constants
        elif instruction == Operator.TRUE:
            self.stack.append(True)
        elif instruction == Operator.FALSE:
            self.stack.append(False)
        elif instruction == Operator.NULL:
            self.stack.append(None)
        elif instruction == Operator.ZERO_VEC:
            self.stack.append(np.array([0, 0, 0]))
        elif instruction == Operator.VEC_X_PLUS:
            self.stack.append(np.array([1, 0, 0]))
        elif instruction == Operator.VEC_X_MINUS:
            self.stack.append(np.array([-1, 0, 0]))
        elif instruction == Operator.VEC_Y_PLUS:
            self.stack.append(np.array([0, 1, 0]))
        elif instruction == Operator.VEC_Y_MINUS:
            self.stack.append(np.array([0, -1, 0]))
        elif instruction == Operator.VEC_Z_PLUS:
            self.stack.append(np.array([0, 0, 1]))
        elif instruction == Operator.VEC_Z_MINUS:
            self.stack.append(np.array([0, 0, -1]))
        elif instruction == Operator.TAU:
            self.stack.append(math.tau)
        elif instruction == Operator.PI:
            self.stack.append(math.pi)
        elif instruction == Operator.E:
            self.stack.append(math.e)

        # Stack manip
        elif instruction == Operator.SWAP:
            stack = self.stack
            self.stack = stack[:-2] + [stack[-1], stack[-2]]
        elif instruction == Operator.ROTATE_LFT:
            stack = self.stack
            self.stack = stack[:-3] + [stack[-2], stack[-1], stack[-3]]
        elif instruction == Operator.ROTATE_RIGHT:
            stack = self.stack
            self.stack = stack[:-3] + [stack[-1], stack[-3], stack[-2]]
        elif instruction == Operator.DUP:
            self.stack.append(self.stack[-1])
        elif instruction == Operator.DUP_SECOND:
            self.stack.append(self.stack[-2])
        elif instruction == Operator.DUP_TOP_DOWN:
            stack = self.stack
            self.stack = stack[:-2] + [stack[-1]] + stack[-2:]
        elif instruction == Operator.DUP_N:
            times = self.stack.pop()
            element = self.stack.pop()
            self.stack.extend([element] * times)
        elif instruction == Operator.DUP_2:
            stack = self.stack
            self.stack = stack + stack[-2:]
        elif instruction == Operator.STACK_LEN:
            self.stack.append(len(self.stack))
        elif instruction == Operator.YANK_N:
            stack = self.stack
            last_index = stack.pop()
            if last_index >= 0:
                stack.append(stack.pop(-1 * (last_index + 1)))
            else:
                stack.insert(last_index, stack.pop())
            self.stack = stack
        elif instruction == Operator.COPY_N:
            stack = self.stack
            last_index = stack.pop()
            if last_index >= 0:
                stack.append(stack[-1 * (last_index + 1)])
            else:
                stack.insert(last_index, stack[-1])
            self.stack = stack
        elif instruction == Operator.LEHMER_PERMUTE:
            code = self.stack.pop()
            self.stack = permute_end_of_list(self.stack, code)

