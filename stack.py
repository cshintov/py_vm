""" class for the stack """


class Stack(object):
    """ class implementing stack """
    def __init__(self):
        self.stack = []

    def push(self, data):
        """ push data onto the stack """
        self.stack.append(data)

    def pop(self):
        """ pops the top of the stack """
        try:
            return self.stack.pop(-1)
        except IndexError:
            print 'Stack is empty'

    def get_top_n(self, num):
        """ returns the top - numth element of the stack """
        try:
            return self.stack[-1 - num]
        except IndexError:
            print "there is only {} elements!".format(len(self.stack))

    def print_stack(self):
        """ prints the stack """
        print self.stack
