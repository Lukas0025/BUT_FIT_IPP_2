from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def xml(msg):
    eprint(msg)
    exit(31)

def xml_struct(msg):
    eprint(msg)
    exit(32)

def cli_params(msg):
    eprint(msg)
    exit(10)

def open_input_file(msg):
    eprint(msg)
    exit(11)

def open_output_file(msg):
    eprint(msg)
    exit(11)

def semantic(msg):
    eprint(msg)
    exit(52)

def operands_types(msg):
    eprint(msg)
    exit(53)

def var_not_exist(msg):
    eprint(msg)
    exit(54)

def frame_not_exist(msg):
    eprint(msg)
    exit(55)

def missing_val_ret_stack(msg):
    eprint(msg)
    exit(56)

def operand_value(msg):
    eprint(msg)
    exit(57)

def string(msg):
    eprint(msg)
    exit(58)

def inner(msg):
    eprint(msg)
    exit(99)