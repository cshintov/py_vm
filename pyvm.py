""" module for reading the pyc file """

from sys import argv
from code import Code
from operations import operations, stk
from utils import get_pyc_list, have_arg
from opcodes import CALL_FUNCTION, RETURN_VALUE


def call_function(code_obj, cur):
    """ executes the function """
    argc = code_obj.get_oparg(cur)
    func = stk.get_top_n(argc)

    # backup func's local vars
    bkup_locals = func.varnames[:]

    while argc:
        argc -= 1
        func.varnames[argc] = stk.pop()

    stk.pop()
    execute(func)

    # restore func's local vars
    func.varnames = bkup_locals[:]

    return cur + 3


def execute(code_obj):
    """ executes the code object """
    cur = 0
    while not code_obj.is_end(cur):
        opcode = code_obj.get_opcode(cur)

        if opcode == CALL_FUNCTION:
            cur = call_function(code_obj, cur)
            continue

        if opcode == RETURN_VALUE:
            return

        try:
            if have_arg(opcode):
                cur = operations[opcode](code_obj, cur)
            else:
                cur = operations[opcode](cur)

        except KeyError:
            msg = 'opcode {1} at {0} not found'.format(cur, hex(opcode))
            raise Exception(msg)


def execute_pyc(pyc_file):
    """ executes the pyc file """
    # getting the bytecode as a list of bytes
    pyc_lst = get_pyc_list(pyc_file)

    # getting the codeobject from the pyc list
    code_obj = Code(pyc_lst)

    # executing the code object
    print
    execute(code_obj)
    print


def main():
    """ main function """
    if len(argv) != 2 or '.pyc' not in argv[1]:
        print 'usage: pyvm.py filename.pyc'

    else:
        pyc_file = argv[1]
        execute_pyc(pyc_file)

if __name__ == '__main__':
    main()
