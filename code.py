""" module for constructing the code object """

import opcodes as opc
import utils as utl

# named objects of the form name : object
names = {}
name_cnt = 0


class Code(object):
    """ class implementing the code object """

    def __init__(self, pyclist, cur=0):
        """  initializes the fields of the code object """
        self.pyclist = pyclist
        self.cur = cur
        self.code = self.acq_code()
        self.consts = self.acq_consts()
        self.names = self.acq_names()
        self.varnames = self.acq_varnames()
        self.name = self.acq_name()

    def get_name(self):
        """ returns the name member """
        return self.name

    def get_cur(self):
        """ returns the current position in the pyc_list"""
        return self.cur

    def get_pyclist(self):
        """ returns the pyclist """
        return self.pyclist

    def get_opcode(self, cur):
        """ returns the opcode at self.code[cur] """
        return self.code[cur]

    def get_oparg(self, cur):
        """ returns the oparg of the opcode at cur """
        return utl.decimal(self.code, cur)

    def is_end(self, cur):
        """ True if end of the code reached """
        if cur >= len(self.code):
            return True
        else:
            return False

    def acq_code(self):
        """ constructs co_code field of the code object """
        pyclist = self.pyclist
        cur = utl.start_of_code(pyclist, self.cur)
        end = cur + utl.decimal(pyclist, cur-5, 4)
        code = []
        while cur < end:
            if not utl.is_func_def(cur, pyclist):
                if utl.have_arg(pyclist[cur]):
                    code.extend(pyclist[cur:cur+3])
                    cur += 3
                else:
                    code.append(pyclist[cur])
                    cur += 1
            else:
                code.append(opc.MAKE_FUNCTION)
                code.extend([0] * 8)
                cur += 9

        self.cur = cur
        return code

    def acq_consts(self):
        """ constructs co_consts of the code object """
        cur = self.cur
        pyclist = self.pyclist
        num_co = utl.decimal(pyclist, cur, 4)
        cur += 5
        consts = []
        for dummy in range(num_co):
            if pyclist[cur] == opc.TYPE_INTEGER:
                consts.append(utl.decimal(pyclist, cur, 4))
                cur += 5
            elif pyclist[cur] == opc.TYPE_NONE:
                consts.append(0)
                cur += 1
            elif pyclist[cur] == opc.TYPE_CODE:
                code_obj = Code(pyclist, cur)
                f_idx = code_obj.get_name()
                consts.append(code_obj)
                names[f_idx][0] = code_obj
                cur = utl.end_of_code(pyclist, cur)

        self.cur = cur
        return consts

    def acq_names(self):
        """ constructs co_names of the code object """
        global name_cnt
        cur = self.cur
        pyclist = self.pyclist
        n_names = utl.decimal(pyclist, cur)
        func_idx = 0
        cur += 5
        co_names = {}
        idx = 0
        for dummy in range(n_names):
            # first occurrence of a name
            if (pyclist[cur] == opc.TYPE_INTERN):
                names[name_cnt] = [0]
                co_names[idx] = names[name_cnt]
                name_cnt += 1
                idx += 1
                cur = utl.skip_element(pyclist, cur)
            elif (pyclist[cur] == opc.TYPE_SREF):
                func_idx = utl.decimal(pyclist, cur)
                co_names[idx] = names[func_idx]
                idx += 1
                cur += 5
            else:
                cur += 1

        self.cur = cur
        return co_names

    def acq_varnames(self):
        """ constructs co_varnames of the code object """
        global name_cnt
        cur = self.cur
        pyclist = self.pyclist
        varnames = []
        n_varnames = utl.decimal(pyclist, cur, 4)
        cur += 5
        for dummy in range(n_varnames):
            varnames.append(0)
            if pyclist[cur] == opc.TYPE_INTERN:
                names[name_cnt] = [0]
                name_cnt += 1
                cur = utl.skip_element(pyclist,  cur)
            elif pyclist[cur] == opc.TYPE_SREF:
                cur += 5
            else:
                cur += 1

        self.cur = cur
        return varnames

    def acq_name(self):
        """ constructs name of the code object """
        global name_cnt
        cur = self.cur
        pyclist = self.pyclist
        n_field = 0
        # skip 2 (:28 s that is cellvars and freevars
        while True:
                if pyclist[cur] == opc.TYPE_TUPLE:
                    n_field += 1
                if n_field == 2:
                    break
                cur += 1

        cur += 5
        # skip filenmae
        cur = utl.skip_element(pyclist, cur)
        self.cur = cur
        # getting the index of the name  of the code
        if pyclist[cur] == opc.TYPE_INTERN:
            names[name_cnt] = [0]
            name_cnt += 1
            return name_cnt - 1

        else:
            return utl.decimal(pyclist, cur, 4)

    def view(self):
        """ shows the fields of the code object """
        print "****************"
        print utl.show_pyc(self.code)
        print len(self.consts), 'constants'
        for idx in range(len(self.consts)):
            if type(self.consts[idx]) == int:
                print self.consts[idx]
            else:
                self.consts[idx].view()
        print self.names
        print self.varnames
        print self.name
        print 'global names'
        print names
        print '--------------------------------'
