""" various utilities """

import opcodes as opc

INT_LIMIT = 2 ** 31


def read_bytes(filename):
    """ generator yielding bytes from a file """
    with open(filename, "rb") as file_h:
        while True:
            chunk = file_h.read()
            if chunk:
                for byte in chunk:
                    yield ord(byte)
            else:
                break


def get_pyc_list(filename):
    """ get the pyc file as a list of bytes """
    lst = list(read_bytes(filename))
    return lst


def show_pyc(lst):
    """ shows the pyclist in hex format """
    return [hex(num) for num in lst]


def decimal(pyc_list, cur, num_byte=2):
    """ compute the decimal value of the num_byte little endian hex """
    value = 0
    factor = 0
    for idx in range(num_byte):
        value |= pyc_list[cur+idx+1] << factor
        factor += 8
    if value >= INT_LIMIT:
        value = value - 2 * INT_LIMIT
    return value


def start_of_code(pyc_list, cur=0):
    """ find the start of the code segment """
    while (pyc_list[cur] != opc.TYPE_CODE and
            pyc_list[cur+17] != opc.TYPE_STRING):
        cur += 1
    if cur == len(pyc_list) - 1:
        raise Exception("no code segment in the rest of the pyc")
    return cur + 22


def skip_element(pycbuf, cur):
    """ skips a code element like integer, t_string, etc """
    leng = decimal(pycbuf, cur, 4)
    return cur + leng + 5


def end_of_code(pyc_list, cur=0):
    """ find the end of the current code """

    cur += 17  # now cur is at byte code s:73 , start of the code string

    cur = skip_element(pyc_list, cur)  # skipping the code string

    # skipping the co_consts field
    n_const = decimal(pyc_list, cur, 4)
    cur += 5
    for dummy in range(n_const):
        if pyc_list[cur] == opc.TYPE_INTEGER:
            cur += 5
        elif pyc_list[cur] == opc.TYPE_NONE:
            cur += 1
        elif pyc_list[cur] == opc.TYPE_CODE:
            cur = end_of_code(pyc_list, cur)
        else:
            cur += 1

    # skip 4 (:28 s that is co_names, varnames, cellvars, freevars
    n_const = 0
    while True:
            if pyc_list[cur] == opc.TYPE_TUPLE:
                n_const += 1
            if n_const == 4:
                break
            cur += 1

    cur += 5
    # skip filenmae
    cur = skip_element(pyc_list, cur)

    # skip function name
    cur = skip_element(pyc_list, cur)

    # skip first line number
    cur += 4

    # skip lnotab
    cur = skip_element(pyc_list, cur)
    return cur


def have_arg(opcode):
    """ checks the opcode has argument(oparg) or not """
    if opcode < opc.HAVE_ARG:
        return False
    else:
        return True


def is_func_def(cur, pycbuf):
    """ checks whether it is a function definition """
    if pycbuf[cur] == opc.LOAD_CONSTANT and pycbuf[cur+3] == opc.MAKE_FUNCTION:
        return True
    else:
        return False


def get_op_arg(pycbuf, cur):
    """ gets the oparg of the current opcode """
    oparg = decimal(pycbuf, cur)
    return oparg
