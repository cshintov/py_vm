# A toy python vm with a few basic operations

This basic python vm written in Python implements basic arithmetic operations 
and function call. These are just a small subset of operations that the actual
CPython implements. The input to this VM is Python bytecode.

By executing a series of stack operations this tiny VM executes the bytecode and produces
the intended result. Just like the official implementation in C, the operations are decided 
by a switch on `OPCODE`s found in the bytecode. Because of the absence of the `switch` in 
Python, I have used a very helpful OPMAP (`operations`) dictionary to do the job. 

The stack operations are roughly as follows:

    1. Push OPERANDS to stack.
    2. When OPCODE is encountered, POP the corresponding number of OPERANDS. 
    3. Do the associated operation. 
    4. Push the result back.

### Note:
    This project originally was here: 
    https://github.com/cshintov/python/tree/master/projects/python_vm
