from enum import Enum

class Operator(Enum):
    # Simple Math
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MAG = "|"
    FLR = "floor"
    CEIL = "ceil"
    VCTR_MK = "vector_mk"
    VCTR_UNMK = "vector_unmk"
    MOD = "%"
    AXIS = "axis"
    RANDOM = "random"

    # Constants
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    ZERO_VEC = "zero_vec"
    VEC_X_PLUS = "vec_x+"
    VEC_X_MINUS = "vec_x-"
    VEC_Y_PLUS = "vec_y+"
    VEC_Y_MINUS = "vec_y-"
    VEC_Z_PLUS = "vec_z+"
    VEC_Z_MINUS = "vec_z-"
    TAU = "tau"
    PI = "pi"
    E = "e"

    # Stack manipulation
    SWAP = "swap"
    ROTATE_LFT = "rotate_left"
    ROTATE_RIGHT = "rotate_right"
    DUP = "dup"
    DUP_SECOND = "dup_2nd"
    DUP_TOP_DOWN = "dup_top_down"
    DUP_N = "dup_n"
    DUP_2 = "dup_2"
    STACK_LEN = "stack_len"
    YANK_N = "yank"
    COPY_N = "cpyank"
    LEHRER_PERMUTE = "permute"

    # Logical
    BOOL_COERCE = "bool"
    BOOL_TO_NUM = "bool_num"
    NOT = "not"
    OR = "or"
    AND = "and"
    XOR = "xor"
    CONDITIONAL_REMOVE = "cond_remove"
    EQ = "eq"
    NOT_EQ = "neq"
    GT = "gt"
    LT = "lt"
    GE = "ge"
    LE = "le"

    # List manip
    INDEX = "index"
    SUBLIST = "sublist"
    APPEND = "append"
    EXTEND = "extend"
    EMPTY_LST = "empty_lst"
    SINGLET = "singlet"
    LENGTH = "len"
    REVERSE = "rev"
    FIND = "find"
    DELETE_INDEX = "del_index"
    SET_INDEX = "set_index"
    MK_LST = "mk_lst"
    UNMK_LST = "unmk_lst"
    ENQUEUE = "enqueue"
    DEQUEUE = "dequeue"

    # Operator manip
    ESCAPE = "\\"
    START_ESCAPE_SEQ = "("
    END_ESCAPE_SEQ = ")"

    # Storage
    PRINT = "print"
    STORE_TEMP = "store"
    READ_TEMP = "read"

    # Advanced math
    SIN = "sin"
    COS = "cos"
    TAN = "tan"
    ARCSIN = "arcsin"
    ARCCOS = "arccos"
    ARCTAN = "arctan"
    ARCTAN2 = "arctan2"
    LOG = "log"

    # Sets
    UNIFY = "unify"
    INTERSECT = "intersect"
    DISJUNCT = "disjunct"
    INVERT = "invert"
    UNIQUE = "unique"

    # Meta eval
    EVAL = "eval"
    LIST_EVAL = "lst_eval"
    HALT = "halt"
