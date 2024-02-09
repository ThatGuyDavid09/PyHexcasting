import re

from token_types.Operator import Operator


def main():
    # a = Operator("=")
    # print(a)
    print(re.fullmatch(r"^dk_[dk]+$", "dk_da"))


if __name__ == "__main__":
    main()
