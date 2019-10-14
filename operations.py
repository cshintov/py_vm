""" operations done by the virtual machine """

from stack import Stack
import opcodes as opc
stk = Stack()


def pop_top(cur):
    """ pops the top of the stack """
    stk.pop()
    return cur+1


def unary_not(cur):
    """ negates the top of the stack """
    stk.push(not stk.pop())
    return cur + 1


def binary_add(cur):
    """ top1 + top """
    tos = stk.pop()
    tos1 = stk.pop()
    stk.push(tos1 + tos)
    return cur + 1


def binary_mul(cur):
    """ top1 + top """
    tos = stk.pop()
    tos1 = stk.pop()
    stk.push(tos1 * tos)
    return cur + 1


def binary_sub(cur):
    """ top1 - top """
    tos = stk.pop()
    tos1 = stk.pop()
    stk.push(tos1 - tos)
    return cur + 1


def binary_div(cur):
    """ top1 - top """
    tos = stk.pop()
    tos1 = stk.pop()
    stk.push(tos1 / tos)
    return cur + 1


def binary_modulo(cur):
    """ top1 - top """
    tos = stk.pop()
    tos1 = stk.pop()
    stk.push(tos1 % tos)
    return cur + 1


def print_item(cur):
    """ prints the top of the stack """
    print stk.get_top_n(0),
    return cur + 1


def print_newline(cur):
    """ prints the newline """
    print
    return cur + 1


def load_name(code_obj, cur):
    """ loads co_names[oparg] to stack """
    oparg = code_obj.get_oparg(cur)
    name = code_obj.names[oparg]
    if type(name) == int:
        stk.push(name)
    else:
        stk.push(code_obj.names[oparg][0])
    return cur + 3


def load_const(code_obj, cur):
    """ loads co_consts[oparg] to stack """
    oparg = code_obj.get_oparg(cur)
    stk.push(code_obj.consts[oparg])
    return cur + 3


def load_global(code_obj, cur):
    """ loads co_consts[oparg] to stack """
    oparg = code_obj.get_oparg(cur)
    stk.push(code_obj.names[oparg][0])
    return cur + 3


def load_fast(code_obj, cur):
    """ loads co_consts[oparg] to stack """
    oparg = code_obj.get_oparg(cur)
    stk.push(code_obj.varnames[oparg])
    return cur + 3


def store_name(code_obj, cur):
    """ stores top to co_names[oparg] """
    oparg = code_obj.get_oparg(cur)
    code_obj.names[oparg] = stk.pop()
    return cur + 3


def store_fast(code_obj, cur):
    """ stores top to co_names[oparg] """
    oparg = code_obj.get_oparg(cur)
    code_obj.varnames[oparg] = stk.pop()
    return cur + 3


def setup_loop(code_obj, cur):
    """ setup loop """
    return cur + 3


def pop_block(cur):
    """ pop loop block """
    return cur + 1


def pop_jump_if_false(code_obj, cur):
    """ jumps if the top is false """
    if not stk.pop():
        return code_obj.get_oparg(cur)
    else:
        return cur + 3


def pop_jump_if_true(code_obj, cur):
    """ jumps if the top is true """
    if stk.pop():
        return code_obj.get_oparg(cur)
    else:
        return cur + 3


def jump_forward(code_obj, cur):
    """ jumps to cur + offset"""
    return cur + 3 + code_obj.get_oparg(cur)


def jump_absolute(code_obj, cur):
    """ jumps to target """
    return code_obj.get_oparg(cur)


def make_function(code_obj, cur):
    """ does nothing just updates the cur """
    return cur + 9


def less_than(op1, op2):
    """ a < b """
    return op1 < op2


def less_equal(op1, op2):
    """ a <= b """
    return op1 <= op2


def equal(op1, op2):
    """ a == b """
    return op1 == op2


def not_equal(op1, op2):
    """ a != b """
    return op1 != op2


def greater_than(op1, op2):
    """ a > b """
    return op1 > op2


def grt_equal(op1, op2):
    """ a >= b """
    return op1 >= op2


""" dictionary compare_op_index: comparison """
comparisons = {
    0: less_than,
    1: less_equal,
    2: equal,
    3: not_equal,
    4: greater_than,
    5: grt_equal
}


def compare_op(code_obj, cur):
    """ compares top1 and top """
    top = stk.pop()
    top1 = stk.pop()
    oparg = code_obj.get_oparg(cur)
    stk.push(comparisons[oparg](top1, top))
    return cur + 3


""" dictionary opcode: operation """
operations = {
    opc.BINARY_ADD: binary_add,
    opc.BINARY_SUBTRACT: binary_sub,
    opc.BINARY_MULTIPLY: binary_mul,
    opc.BINARY_DIVIDE: binary_div,
    opc.BINARY_MODULO: binary_modulo,
    opc.LOAD_NAME: load_name,
    opc.LOAD_FAST: load_fast,
    opc.LOAD_CONSTANT: load_const,
    opc.LOAD_GLOBAL: load_global,
    opc.STORE_NAME: store_name,
    opc.STORE_FAST: store_fast,
    opc.PRINT_ITEM: print_item,
    opc.PRINT_NEWLINE: print_newline,
    opc.POP_JUMP_IF_FALSE: pop_jump_if_false,
    opc.POP_JUMP_IF_TRUE: pop_jump_if_true,
    opc.JUMP_FORWARD: jump_forward,
    opc.JUMP_ABSOLUTE: jump_absolute,
    opc.COMPARE_OP: compare_op,
    opc.UNARY_NOT: unary_not,
    opc.POP_TOP: pop_top,
    opc.MAKE_FUNCTION: make_function,
    opc.SETUP_LOOP: setup_loop,
    opc.POP_BLOCK: pop_block
}
