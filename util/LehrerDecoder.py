import math


class Factorial:
    def __init__(self):
        self.acc = 1
        self.n = 1

    def __iter__(self):
        return self

    def __next__(self):
        val = self.acc
        self.acc *= self.n
        self.n += 1
        return val


def factorial():
    acc = 1
    n = 1

    while True:
        val = acc
        acc *= n
        n += 1
        yield val


class LehrerDecoder:

    @staticmethod
    def decode_lehmer_code(value, stack):
        strides = list(filter(lambda x: x <= value, factorial()))

        # if len(stack) < len(strides):
        #     raise ValueError("Manipulating too many elements on the stack!")

        stride_offset = len(stack) - len(strides)
        edit_target = stack[stride_offset:]
        swap = edit_target[:]

        while strides:
            divisor = strides.pop(0)
            index = value // divisor
            value %= divisor
            edit_target[0] = swap.pop(index)
            edit_target = edit_target[1:]

        return stack
