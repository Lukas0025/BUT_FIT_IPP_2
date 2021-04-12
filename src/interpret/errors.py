##
# Project: ipp2
# file with errors and exit codes
# @author Lukáš Plevač <xpleva07>
# @date 12.4.2021

from __future__ import print_function
import sys

##
# print text on stderr
# @param args args to print
# @return None
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

##
# print msg on stderr and exit with code 31
# bad xml format unbale to read
# @param msg error message
# @return None
def xml(msg):
    eprint("XML parse error: {}".format(msg))
    exit(31)

##
# print msg on stderr and exit with code 32
# bad xml structure expected ex. tag but tag is nat same
# @param msg error message
# @return None
def xml_struct(msg):
    eprint("Bad XML scructure: {}".format(msg))
    exit(32)

##
# print msg on stderr and exit with code 10
# bad cli/terminal parametrs
# @param msg error message
# @return None
def cli_params(msg):
    eprint("Bad cli parameters: {}".format(msg))
    exit(10)

##
# print msg on stderr and exit with code 11
# error when opening input file
# @param msg error message
# @return None
def open_input_file(msg):
    eprint("error during input file open {}".format(msg))
    exit(11)

##
# print msg on stderr and exit with code 12
# error when opening output file
# @param msg error message
# @return None
def open_output_file(msg):
    eprint("error during output file open {}".format(msg))
    exit(12)

##
# print msg on stderr and exit with code 52
# generaic semantic error
# @param msg error message
# @return None
def semantic(msg):
    eprint("Semantic error: {}".format(msg))
    exit(52)

##
# print msg on stderr and exit with code 53
# bad operands types for action
# @param msg error message
# @return None
def operands_types(msg):
    eprint("Bad operands types: {}".format(msg))
    exit(53)
##
# print msg on stderr and exit with code 54
# varaible not exist
# @param msg error message
# @return None
def var_not_exist(msg):
    eprint("Varable not exist: {}".format(msg))
    exit(54)

##
# print msg on stderr and exit with code 55
# frame not exist
# @param msg error message
# @return None
def frame_not_exist(msg):
    eprint("Frame not exist: {}".format(msg))
    exit(55)

##
# print msg on stderr and exit with code 56
# missing value in return stack
# @param msg error message
# @return None
def missing_val_ret_stack(msg):
    eprint("missing value in return stack: {}".format(msg))
    exit(56)

##
# print msg on stderr and exit with code 57
# bad operand value ex. divade by 0
# @param msg error message
# @return None
def operand_value(msg):
    eprint("Bad operand value: {}".format(msg))
    exit(57)

##
# print msg on stderr and exit with code 58
# bad operand value ex. divade by 0
# @param msg error message
# @return None
def string(msg):
    eprint("error during string operation: {}".format(msg))
    exit(58)

##
# print msg on stderr and exit with code 99
# interal error
# @param msg error message
# @return None
def inner(msg):
    eprint("inner error: {}".format(msg))
    exit(99)