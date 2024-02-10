import math


def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func

    return decorate


@static_var("lut", [1])
def factorial(n):
    while n >= len(factorial.lut):
        factorial.lut.append(factorial.lut[-1] * len(factorial.lut))
    return factorial.lut[n]


def encode(permutation):
    """Return Lehmer Code of the given permutation.
    """

    def permutation_is_valid(permutation):
        if not permutation:
            return False

        minimum = min(permutation)
        maximum = max(permutation)

        used = [0] * (maximum - minimum + 1)
        for i in permutation:
            used[i - minimum] += 1

        if min(used) == 1 and max(used) == 1:
            return True
        else:
            return False

    def count_lesser(i, permutation):
        return sum(it < permutation[i] for it in permutation[i + 1:])

    def parial_result(i, permutation):
        return count_lesser(i, permutation) * factorial(len(permutation) - 1 - i)

    if not permutation_is_valid(permutation):
        return False

    return sum(parial_result(i, permutation) for i in range(0, len(permutation)))

def find_lehmer_length(lehmer):
    if lehmer == 0:
        return 1
    if lehmer == 1:
        return 2
    length = 0
    while lehmer < factorial(length):
        length += 1
    return length - 1


def decode(length, lehmer):
    """Return permutation for the given Lehmer Code and permutation length. Result permutation contains
    number from 0 to length-1.
    """
    # length = find_lehmer_length(lehmer)

    result = [(lehmer % factorial(length - i)) // factorial(length - 1 - i) for i in range(length)]
    used = [False] * length
    for i in range(length):
        counter = 0
        for j in range(length):
            if not used[j]:
                counter += 1
            if counter == result[i] + 1:
                result[i] = j
                used[j] = True
                break
    return result

def lehmer_to_permutation(lehmer_code):
    """Convert Lehmer code to permutation."""
    n = len(lehmer_code)
    permutation = []
    available_numbers = list(range(1, n+1))

    for i in range(n):
        index = lehmer_code[i]
        permutation.append(available_numbers.pop(index))

    return permutation

def permute_end_of_list(lst, lehmer_code):
    """Permute the end of a list according to a Lehmer code."""
    perm_lst = decode(len(lst), lehmer_code)
    # permutation = lehmer_to_permutation(perm_lst)
    n = len(perm_lst)
    end_part = lst[-n:]

    permuted_end_part = [end_part[i] for i in perm_lst]
    lst[-n:] = permuted_end_part
    return lst
