import math
import random

import numpy as np

from errors.PyHexCastError import PyHexCastError
from token_types.ExecutionMode import ExecutionMode
from token_types.DropKeep import DropKeep
from token_types.EscapeMode import EscapeMode
from token_types.NumberLiteral import NumberLiteral
from token_types.Operator import Operator
from util.LehrerDecoder import permute_end_of_list


class Executor:
    def __init__(self):
        self.stack = []
        self.temporary = None
        self.execution_mode = ExecutionMode.NORMAL
        self.escape_mode = EscapeMode.NORMAL
        self.escaped_many = []

    def execute_instructions(self, instructions):
        if isinstance(instructions, PyHexCastError):
            raise instructions
        for instruction in instructions:
            stop = self.execute_instruction(instruction)
            if stop:
                break

    def execute_instruction(self, instruction):
        # Skip and stop if somehow we got here in a stopped execution mode
        if self.execution_mode == ExecutionMode.STOP:
            return True

        if isinstance(instruction, NumberLiteral):
            self.stack.append(instruction.value)

        # Handle escape
        if self.escape_mode == EscapeMode.ESCAPE_NEXT:
            if self.execution_mode == ExecutionMode.ESCAPE_MANY:
                self.escaped_many.append(instruction)
            else:
                self.stack.append(instruction)
            return

        # Handle escape many
        if self.execution_mode == ExecutionMode.ESCAPE_MANY:
            if instruction == Operator.END_ESCAPE_SEQ:
                self.execution_mode = ExecutionMode.NORMAL
                self.stack.append(self.escaped_many)
                self.escaped_many = []
            else:
                self.escaped_many.append(instruction)
            return


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
        elif isinstance(instruction, DropKeep):
            drop_order = instruction.get_drop_order()
            padding = len(self.stack) - len(drop_order)
            drop_order = [False] * padding + drop_order[::-1]
            self.stack = [item for item, drop in zip(self.stack, drop_order) if not drop]

        # Logical operators
        elif instruction == Operator.BOOL_COERCE:
            item = self.stack.pop()
            if item == 0 or item is None or item == []:
                self.stack.append(False)
            else:
                self.stack.append(True)
        elif instruction == Operator.BOOL_TO_NUM:
            item = self.stack.pop()
            # Prevents truthy things from qualifying
            if not isinstance(item, bool):
                raise ValueError("value must be boolean")
            if item:
                self.stack.append(1)
            else:
                self.stack.appent(0)
        elif instruction == Operator.NOT:
            item = self.stack.pop()
            if not isinstance(item, bool):
                raise ValueError("value must be boolean")
            self.stack.append(not item)
        elif instruction == Operator.OR:
            a = self.stack.pop()
            b = self.stack.pop()
            if not (isinstance(a, bool) and isinstance(a, bool)):
                raise ValueError("values must be boolean")
            self.stack.append(a or b)
        elif instruction == Operator.AND:
            a = self.stack.pop()
            b = self.stack.pop()
            if not (isinstance(a, bool) and isinstance(a, bool)):
                raise ValueError("values must be boolean")
            self.stack.append(a and b)
        elif instruction == Operator.XOR:
            a = self.stack.pop()
            b = self.stack.pop()
            if not (isinstance(a, bool) and isinstance(a, bool)):
                raise ValueError("values must be boolean")
            self.stack.append(a ^ b)
        elif instruction == Operator.CONDITIONAL_REMOVE:
            a = self.stack.pop()
            if not isinstance(a, bool):
                raise ValueError("value must be boolean")
            if a:
                self.stack.pop(-2)
            else:
                self.stack.pop()
        elif instruction == Operator.EQ:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(a == b)
        elif instruction == Operator.NOT_EQ:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(a != b)
        elif instruction == Operator.GT:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(a > b)
        elif instruction == Operator.LT:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(a < b)
        elif instruction == Operator.GE:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(a >= b)
        elif instruction == Operator.LE:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(a >= b)

        # List manip
        elif instruction == Operator.INDEX:
            index = self.stack.pop()
            lst = self.stack.pop()
            self.stack.appent(lst[index])
        elif instruction == Operator.SUBLIST:
            lower = self.stack.pop()
            upper = self.stack.pop()
            lst = self.stack.pop()
            self.stack.append(lst[lower:upper])
        elif instruction == Operator.APPEND:
            app = self.stack.pop()
            lst = self.stack.pop()
            self.stack.appent(lst.append(app))
        elif instruction == Operator.EXTEND:
            ext = self.stack.pop()
            lst = self.stack.pop()
            self.stack.appent(lst.extend(ext))
        elif instruction == Operator.EMPTY_LST:
            self.stack.appent([])
        elif instruction == Operator.SINGLET:
            item = self.stack.pop()
            self.stack.append([item])
        elif instruction == Operator.LENGTH:
            lst = self.stack.pop()
            self.stack.append(len(lst))
        elif instruction == Operator.REVERSE:
            lst = self.stack.pop()
            self.stack.append(lst[::-1])
        elif instruction == Operator.FIND:
            num = self.stack.pop()
            lst = self.stack.pop()
            self.stack.append(lst.find(num))
        elif instruction == Operator.DELETE_INDEX:
            index = self.stack.pop()
            lst = self.stack.pop()
            self.stack.append(lst.pop(index))
        elif instruction == Operator.SET_INDEX:
            try:
                item = self.stack.pop()
                index = self.stack.pop()
                lst = self.stack.pop()
                lst[index] = item
                self.stack.append(lst)
            except IndexError:
                pass
        elif instruction == Operator.MK_LST:
            count = self.stack.pop()
            lst = []
            for i in range(count):
                lst.append(self.stack.pop())
            self.stack.append(lst)
        elif instruction == Operator.UNMK_LST:
            lst = self.stack.pop()
            self.stack.extend(lst)
        elif instruction == Operator.ENQUEUE:
            item = self.stack.pop()
            lst = self.stack.pop()
            lst.insert(0, item)
            self.stack.append(lst)
        elif instruction == Operator.DEQUEUE:
            lst = self.stack.pop()
            item = lst.pop(0)
            self.stack.extend([lst, item])

        # Operator manip
        elif instruction == Operator.ESCAPE:
            self.escape_mode = EscapeMode.ESCAPE_NEXT
        elif instruction == Operator.START_ESCAPE_SEQ:
            self.execution_mode = ExecutionMode.ESCAPE_MANY
        elif instruction == Operator.END_ESCAPE_SEQ:
        # This can only happen if end escape seq was processed before
        # start escape seq, and as such, is an error
            raise RuntimeError(')" executed before "("')

        # Storage
        elif instruction == Operator.PRINT:
            a = self.stack.pop()
            print(a)
        elif instruction == Operator.STORE_TEMP:
            a = self.stack.pop()
            self.temporary = a
        elif instruction == Operator.READ_TEMP:
            self.stack.append(self.temporary)

        # Advanced math
        elif instruction == Operator.SIN:
            a = self.stack.pop()
            self.stack.append(math.sin(a))
        elif instruction == Operator.COS:
            a = self.stack.pop()
            self.stack.append(math.cos(a))
        elif instruction == Operator.TAN:
            a = self.stack.pop()
            self.stack.append(math.tan(a))
        elif instruction == Operator.ARCSIN:
            a = self.stack.pop()
            self.stack.append(math.asin(a))
        elif instruction == Operator.ARCCOS:
            a = self.stack.pop()
            self.stack.append(math.acos(a))
        elif instruction == Operator.ARCTAN:
            a = self.stack.pop()
            self.stack.append(math.atan(a))
        elif instruction == Operator.ARCTAN2:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(math.atan2(a, b))
        elif instruction == Operator.LOG:
            log = self.stack.pop()
            base = self.stack.pop()
            self.stack.append(math.log(log, base))

        # Sets
        elif instruction == Operator.UNIFY:
            a = self.stack.pop()
            b = self.stack.pop()

            if isinstance(a, float) and isinstance(b, float):
                if not (a.is_integer() and b.is_integer()):
                    raise ValueError("Arguments must be integers, not floats")
                a = int(a)
                b = int(b)
                self.stack.append(a | b)
            elif isinstance(a, list) and isinstance(b, list):
                set_a = set(a)
                set_b = set(b)
                self.stack.append(set_a | set_b)
            else:
                raise ValueError("Arguments must either both be sets or both be integers")
        elif instruction == Operator.INTERSECT:
            a = self.stack.pop()
            b = self.stack.pop()

            if isinstance(a, float) and isinstance(b, float):
                if not (a.is_integer() and b.is_integer()):
                    raise ValueError("Arguments must be integers, not floats")
                a = int(a)
                b = int(b)
                self.stack.append(a & b)
            elif isinstance(a, list) and isinstance(b, list):
                set_a = set(a)
                set_b = set(b)
                self.stack.append(list(set_a & set_b))
            else:
                raise ValueError("Arguments must either both be sets or both be integers")
        elif instruction == Operator.DISJUNCT:
            a = self.stack.pop()
            b = self.stack.pop()

            if isinstance(a, float) and isinstance(b, float):
                if not (a.is_integer() and b.is_integer()):
                    raise ValueError("Arguments must be integers, not floats")
                a = int(a)
                b = int(b)
                self.stack.append(a ^ b)
            elif isinstance(a, list) and isinstance(b, list):
                set_a = set(a)
                set_b = set(b)
                self.stack.append(list(set_a ^ set_b))
            else:
                raise ValueError("Arguments must either both be sets or both be integers")
        elif instruction == Operator.INVERT:
            a = self.stack.pop()

            if isinstance(a, float):
                if not a.is_integer():
                    raise ValueError("Argument must be integer, not float")
                a = int(a)
                self.stack.append(~a)
            else:
                raise ValueError("Argument must be integer")
        elif instruction == Operator.UNIQUE:
            a = self.stack.pop()

            if isinstance(a, list):
                self.stack.append(list(set(a)))
            else:
                raise ValueError("Argument must be list")

        # Meta eval
        elif instruction == Operator.EVAL:
            to_execute = self.stack.pop()
            if not isinstance(to_execute, list):
                to_execute = [to_execute]

            executor = Executor()
            executor.stack = self.stack
            executor.temporary = self.temporary
            executor.execute_instructions(to_execute)
            self.stack = executor.stack
        elif instruction == Operator.LIST_EVAL:
            items = self.stack.pop()
            instructions = self.stack.pop()
            finished_stacks = []
            for item in items:
                executor = Executor()
                executor.temporary = self.temporary
                executor.stack = self.stack + [item]
                executor.execute_instructions(instructions)
                finished_stacks.extend(executor.stack)
                self.temporary = executor.temporary
            self.stack.append(finished_stacks)
        elif instruction == Operator.HALT:
            self.execution_mode = ExecutionMode.STOP
            return True
        else:
            raise RuntimeError("Invalid operator")

