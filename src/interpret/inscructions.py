import errors
import re

class inscructions:
    ##
    # get inscruction function by opcode
    # @param self
    # @param opcode str of opcode
    # @return function of opcode
    def get_inscrustion(self, opcode):
        return {
            'move': self.move,
            'createframe': self.createframe,
            'pushframe': self.pushframe,
            'popframe': self.popframe,
            'defvar': self.defvar,
            'call': self.call,
            'return': self.return_f,
            'pushs': self.pushs,
            'pops': self.pops,
            'add': self.add,
            'sub': self.sub,
            'mul': self.mul,
            'idiv': self.idiv,
            'div': self.div,
            'lt': self.lt,
            'gt': self.gt,
            'eq': self.eq,
            'and': self.and_f,
            'or': self.or_f,
            'not': self.not_f,
            'int2char': self.int2char,
            'stri2int': self.str2int,
            'read': self.read,
            'write': self.write,
            'print': self.write, # write alias
            'concat': self.concat,
            'strlen': self.strlen,
            'getchar': self.getchar,
            'setchar': self.setchar,
            'type': self.type_f,
            'label': self.label,
            'jump': self.jump,
            'jumpifeq': self.jumpifeq,
            'jumpifneq': self.jumpifneq,
            'exit': self.exit,
            'dprint': self.dprint,
            'break': self.break_f
        }.get(opcode.lower(), self.undefined)

    ##
    # Decode string escape \XXX to unicode char in string
    # @param self
    # @param string string with escapes
    # @return decoded string
    def decode_escapes(self, string):
        escape = re.compile("\\\\[0-9][0-9][0-9]")

        es = escape.search(string)
        while es != None:
            str_array = list(string)

            str_array[es.start()] = chr(int(es.group()[1:]))
            
            str_array.pop(es.start() + 1)
            str_array.pop(es.start() + 1)
            str_array.pop(es.start() + 1)
            
            string = "".join(str_array)
            es = escape.search(string)

        if "\\" in list(string):
            errors.string("fail to decode escape in '{}'".format(string))

        return string

    ##
    # function or undefined opcode
    # @param self
    # @param args args for inscruction
    def undefined(self, args):
        errors.xml_struct("Undefined OPCODE ip:{}".format(self.ip))

    ##
    # check args types and length if bad exit
    # @param self
    # @param needs array of possible types or args ex. [['var'], ['int', 'float']]
    # @param args args for inscruction
    # @param uninit bool accept uninited vars
    def args_check(self, needs, args, uninit = False):
        if len(needs) != len(args):
            errors.xml_struct("bad args count for opcodes ip:{}".format(self.ip))

        for i in range(len(needs)):
            try:
                vartype = self.program._get_lower_attrib(args[i])['type']
            except KeyError:
                errors.xml_struct("no type attribute for arg ip:{}".format(self.ip))

            if "var" in needs[i] or "label" in needs[i]:
                if vartype not in needs[i]:
                    errors.operands_types("bad type of operand expected {} given ['{}'] ip:{}".format(needs[i], vartype,self.ip))
            elif self._type_of(args[i]) not in needs[i]:
                
                if not uninit:
                    self._value(args[i])

                errors.operands_types("bad type of operand expected {} given {} ip:{}".format(needs[i], self._type_of(args[i]), self.ip))
                
    ##
    # get value of expression of value ex. int@-10 returns -10 
    # or GF@a returns value from smytable for GF@a
    # @param self
    # @param args args for inscruction
    # @return str value of expression
    def _value(self, arg):
        return self.symtable.get_value_str(self._get_typeval(arg))

    ##
    # get type of expression of value ex. int@-10 returns int
    # or GF@a returns type from smytable for GF@a
    # @param self
    # @param args args for inscruction
    # @return str type of expression
    def _type_of(self, arg):
        return self.symtable.get_type_str(self._get_typeval(arg))

    ##
    # get value of expression of value in python types ex. int@-10 returns int(-10) 
    # or GF@a returns value from smytable for type(GF@a)
    # @param self
    # @param args args for inscruction
    # @return mixed value of expression
    def _typed_value(self, arg):
        value = self._value(arg)
        typed = self._type_of(arg)

        if (typed == 'int'):
            return int(value)
        elif (typed == 'float'):
            return float(value)
        elif typed == 'bool':
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
            
            errors.operand_value("bad value of operand type Bool")
        else:
            return value

    ##
    # get string of attr in format type@value
    # @param self
    # @param args args for inscruction
    # @return string type@value
    def _get_typeval(self, arg):

        try:
            vartype = self.program._get_lower_attrib(arg)['type']
        except KeyError:
            errors.xml_struct("no type attribute for arg")

        if vartype not in ['int', 'float', 'string', 'label', 'bool', 'var', 'type', 'nil']:
            errors.xml_struct("bad type in type attrib {}".format(vartype))

        if vartype != 'var' and vartype != 'label':
            varvalue = arg.text
            if varvalue == None:
                varvalue = ""

            return "{}@{}".format(vartype, varvalue)
        else:
            # @todo check var/label is valid
            return arg.text

    ##
    # interpret instruction MOVE
    # @param self
    # @param args args for inscruction
    def move(self, args):
        self.args_check([
            ["var"],
            ['string', 'int', 'float', 'bool', 'nil']
        ], args)

        self.symtable.set_value(
            self._get_typeval(args[0]),
            self._type_of(args[1]),
            self._value(args[1])
        )

        self.ip += 1

    ##
    # interpret instruction CREATEFRAME
    # @param self
    # @param args args for inscruction
    def createframe(self, args):
        self.args_check([], args)
        self.symtable.create_frame()
        self.ip += 1

    ##
    # interpret instruction PUSHFRAME
    # @param self
    # @param args args for inscruction
    def pushframe(self, args):
        self.args_check([], args)
        self.symtable.push_frame()
        self.ip += 1

    ##
    # interpret instruction POPFRAME
    # @param self
    # @param args args for inscruction
    def popframe(self, args):
        self.args_check([], args)
        self.symtable.pop_frame()
        self.ip += 1

    ##
    # interpret instruction DEFVAR
    # @param self
    # @param args args for inscruction
    def defvar(self, args):
        self.args_check([
            ['var']
        ], args)

        self.symtable.def_var(
            self._get_typeval(args[0])
        )

        self.ip += 1

    ##
    # interpret instruction CALL
    # @param self
    # @param args args for inscruction
    def call(self, args):
        self.args_check([
            ['label'],
        ], args)

        self.return_stack.append(self.ip + 1)
        self.jump([args[0]])

    ##
    # interpret instruction RETURN
    # @param self
    # @param args args for inscruction
    def return_f(self, args):
        self.args_check([], args)

        if len(self.return_stack) < 1:
            errors.missing_val_ret_stack("in return stack is no address to return")

        self.ip = self.return_stack.pop()

    ##
    # interpret instruction PUSHS
    # @param self
    # @param args args for inscruction
    def pushs(self, args):
        self.args_check([
            ['string', 'int', 'float', 'bool', 'nil']
        ], args)

        self.stack.append({
            'type': self._type_of(args[0]),
            'value': self._value(args[0])
        })

        self.ip += 1

    ##
    # interpret instruction POPS
    # @param self
    # @param args args for inscruction
    def pops(self, args):
        self.args_check([
            ['var']
        ], args)

        if len(self.stack) < 1:
            errors.missing_val_ret_stack("cant pop from empty stack")

        var = self.stack.pop()

        self.symtable.set_value(
            self._get_typeval(args[0]),
            var['type'],
            var['value']
        )

        self.ip += 1

    ##
    # interpret instruction ADD
    # @param self
    # @param args args for inscruction
    def add(self, args):
        self.args_check([
            ['var'],
            ['int', 'float'],
            ['int', 'float']
        ], args)

        a = self._typed_value(args[1])
        a_type = self._type_of(args[1])
        b = self._typed_value(args[2])
        b_type = self._type_of(args[2])

        if (b_type == 'float' or a_type == 'float'):
            out_type = 'float'
        else:
            out_type = 'int'

        out = a + b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            out_type,
            str(out)
        )

        self.ip += 1

    ##
    # interpret instruction SUB
    # @param self
    # @param args args for inscruction
    def sub(self, args):
        self.args_check([
            ['var'],
            ['int', 'float'],
            ['int', 'float']
        ], args)

        a = self._typed_value(args[1])
        a_type = self._type_of(args[1])
        b = self._typed_value(args[2])
        b_type = self._type_of(args[2])

        if (b_type == 'float' or a_type == 'float'):
            out_type = 'float'
        else:
            out_type = 'int'

        out = a - b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            out_type,
            str(out)
        )

        self.ip += 1

    ##
    # interpret instruction MUL
    # @param self
    # @param args args for inscruction
    def mul(self, args):
        self.args_check([
            ['var'],
            ['int', 'float'],
            ['int', 'float']
        ], args)

        a = self._typed_value(args[1])
        a_type = self._type_of(args[1])
        b = self._typed_value(args[2])
        b_type = self._type_of(args[2])

        if (b_type == 'float' or a_type == 'float'):
            out_type = 'float'
        else:
            out_type = 'int'

        out = a * b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            out_type,
            str(out)
        )

        self.ip += 1

    ##
    # interpret instruction IDIV
    # @param self
    # @param args args for inscruction
    def idiv(self, args):
        self.args_check([
            ['var'],
            ['int', 'float'],
            ['int', 'float']
        ], args)

        a = self._typed_value(args[1])
        a_type = self._type_of(args[1])
        b = self._typed_value(args[2])
        b_type = self._type_of(args[2])

        if (b_type == 'float' or a_type == 'float'):
            out_type = 'float'
        else:
            out_type = 'int'

        if b == 0:
            errors.operand_value("try to div by 0")

        out = a // b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            out_type,
            str(out)
        )

        self.ip += 1

    ##
    # interpret instruction DIV
    # @param self
    # @param args args for inscruction
    def div(self, args):
        self.args_check([
            ['var'],
            ['int', 'float'],
            ['int', 'float']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        if b == 0:
            errors.operand_value("try to div by 0")

        out = a / b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            'float',
            str(out)
        )

        self.ip += 1

    ##
    # interpret instruction LT
    # @param self
    # @param args args for inscruction
    def lt(self, args):
        self.args_check([
            ['var'],
            ['string', 'int', 'float', 'bool', 'type'],
            ['string', 'int', 'float', 'bool', 'type']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        if self._type_of(args[1]) != self._type_of(args[2]):
            errors.operands_types("fail to do LT with this types")

        out = a < b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            'bool',
            str(out)
        )

        self.ip += 1

    ##
    # interpret instruction GT
    # @param self
    # @param args args for inscruction
    def gt(self, args):
        self.args_check([
            ['var'],
            ['string', 'int', 'float', 'bool', 'type'],
            ['string', 'int', 'float', 'bool', 'type']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        if self._type_of(args[1]) != self._type_of(args[2]):
            errors.operands_types("fail to do GT with this types")

        out = a > b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            'bool',
            str(out)
        )

        self.ip += 1

    ##
    # interpret instruction EQ
    # @param self
    # @param args args for inscruction
    def eq(self, args):
        self.args_check([
            ['var'],
            ['string', 'int', 'float', 'bool', 'type', 'nil'],
            ['string', 'int', 'float', 'bool', 'type', 'nil']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        if self._type_of(args[1]) == 'nil' or self._type_of(args[2]) == 'nil':
            pass
        elif self._type_of(args[1]) != self._type_of(args[2]):
            errors.operands_types("fail to do EQ with this types")

        out = a == b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            'bool',
            str(out)
        )

        self.ip += 1

    ##
    # interpret instruction AND
    # @param self
    # @param args args for inscruction
    def and_f(self, args):
        self.args_check([
            ['var'],
            ['bool'],
            ['bool']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        out = a and b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            'bool',
            str(out)
        )

        self.ip += 1

    ##
    # interpret instruction OR
    # @param self
    # @param args args for inscruction
    def or_f(self, args):
        self.args_check([
            ['var'],
            ['bool'],
            ['bool']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        out = a or b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            'bool',
            str(out)
        )

        self.ip += 1

    ##
    # interpret instruction NOT
    # @param self
    # @param args args for inscruction
    def not_f(self, args):
        self.args_check([
            ['var'],
            ['bool']
        ], args)

        a = self._typed_value(args[1])

        out = not a

        self.symtable.set_value(
            self._get_typeval(args[0]),
            'bool',
            str(out)
        )

        self.ip += 1

    ##
    # interpret instruction INT2CHAR
    # @param self
    # @param args args for inscruction
    def int2char(self, args):
        self.args_check([
            ['var'],
            ['int']
        ], args)

        try:
            self.symtable.set_value(
                self._get_typeval(args[0]),
                'string',
                chr(self._typed_value(args[1]))
            )
        except:
            errors.string("fail to converse int2char with {}".format(self._get_typeval(args[1])))

        self.ip += 1

    ##
    # interpret instruction STRI2INT
    # @param self
    # @param args args for inscruction
    def str2int(self, args):
        self.args_check([
            ['var'],
            ['string'],
            ['int']
        ], args)

        string = self._typed_value(args[1])
        index = self._typed_value(args[2])

        if index not in range(len(string)):
            errors.string("try do stri2int on unexist position {}".format(index))

        self.symtable.set_value(
            self._get_typeval(args[0]),
            self._type_of(args[1]),
            ord(string[index])
        )

        self.ip += 1

    ##
    # interpret instruction READ
    # @param self
    # @param args args for inscruction
    def read(self, args):
        self.args_check([
            ['var'],
            ['type']
        ], args)

        readedtype = self._value(args[1]).lower()

        if readedtype not in ['int', 'float', 'bool', 'string']:
            errors.operand_value("unsuported type to read {}".format(readedtype))

        try:
            if self.infile == None:
                readed = input()
            else:
                readed = self.infile.readline()
        except:
                readed = "nil"
                readedtype = "nil"

        ## check type
        try:
            if readedtype == 'int':
                readed = int(readed)

            elif readedtype == 'float':
                readed = float(readed)

            elif readedtype == 'bool':
                readed = readed.lower()
                if readed == "true":
                    readed = True
                elif readed == "false":
                    readed = False
                else:
                    readed = "nil"
                    readedtype = "nil"
        except:
            readed = "nil"
            readedtype = "nil"

        self.symtable.set_value(
            self._get_typeval(args[0]),
            readedtype,
            str(readed)
        )

        self.ip += 1

    ##
    # interpret instruction WRITE
    # @param self
    # @param args args for inscruction
    def write(self, args):
        self.args_check([
            ['string', 'int', 'float', 'bool', 'type', 'nil']
        ], args)

        value = self._typed_value(args[0])
        vtype = self._type_of(args[0])

        if vtype == 'bool':
            if value:
                value = 'true'
            else:
                value = 'false'
        elif vtype == 'nil':
            value = ''

        print(
            self.decode_escapes(str(value)),
            end = ''
        )

        self.ip += 1

    ##
    # interpret instruction CONCAT
    # @param self
    # @param args args for inscruction
    def concat(self, args):
        self.args_check([
            ['var'],
            ['string'],
            ['string']
        ], args)

        self.symtable.set_value(
            self._get_typeval(args[0]),
            "string",
            self._typed_value(args[1]) + self._typed_value(args[2])
        )

        self.ip += 1

    ##
    # interpret instruction STRLEN
    # @param self
    # @param args args for inscruction
    def strlen(self, args):
        self.args_check([
            ['var'],
            ['string']
        ], args)

        self.symtable.set_value(
            self._get_typeval(args[0]),
            "int",
            len(self._typed_value(args[1]))
        )

        self.ip += 1

    ##
    # interpret instruction GETCHAR
    # @param self
    # @param args args for inscruction
    def getchar(self, args):
        self.args_check([
            ['var'],
            ['string'],
            ['int']
        ], args)

        index = self._typed_value(args[2])
        string = self._typed_value(args[1])

        if index not in range(len(string)):
            errors.string("try get char outside range of string")

        self.symtable.set_value(
            self._get_typeval(args[0]),
            "string",
            string[index]
        )

        self.ip += 1

    ##
    # interpret instruction SETCHAR
    # @param self
    # @param args args for inscruction
    def setchar(self, args):
        self.args_check([
            ['string'],
            ['int'],
            ['string']
        ], args)

        curr = list(self._typed_value(args[0]))
        index = self._typed_value(args[1])

        if index not in range(len(curr)):
            errors.string("put char on unexist position {}".format(index))

        curr[index] = self._typed_value(args[2])[0]

        self.symtable.set_value(
            self._get_typeval(args[0]),
            "string",
            "".join(curr)
        )

        self.ip += 1

    ##
    # interpret instruction TYPE
    # @param self
    # @param args args for inscruction
    def type_f(self, args):
        self.args_check([
            ['var'],
            ['int', 'float', 'bool', 'string', 'type', 'nil', None]
        ], args, uninit = True)

        typeof = self._type_of(args[1])
        if typeof == None:
            typeof = ''

        self.symtable.set_value(
            self._get_typeval(args[0]),
            "type",
            typeof
        )

        self.ip += 1

    ##
    # interpret instruction LABEL
    # @param self
    # @param args args for inscruction
    def label(self, args):
        self.args_check([
            ['label']
        ], args)

        self.ip += 1

        self.symtable.def_label(
            self._get_typeval(args[0]),
            self.ip
        )


    ##
    # interpret instruction JUMP
    # @param self
    # @param args args for inscruction
    def jump(self, args):
        self.args_check([
            ['label']
        ], args)

        self.ip = self.symtable.get_label(self._get_typeval(args[0]))

    ##
    # interpret instruction JUMPIFEQ
    # @param self
    # @param args args for inscruction
    def jumpifeq(self, args):
        self.args_check([
            ['label'],
            ['string', 'int', 'float', 'bool', 'type', 'nil'],
            ['string', 'int', 'float', 'bool', 'type', 'nil']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        if self._type_of(args[1]) == 'nil' or self._type_of(args[2]) == 'nil':
            pass
        elif self._type_of(args[1]) != self._type_of(args[2]):
            errors.operands_types("fail to do JUMPIFEQ with this types {} and {}".format(
                self._type_of(args[1]),
                self._type_of(args[2])
            ))

        if (a == b):
            return self.jump([args[0]])

        self.ip += 1

    ##
    # interpret instruction JUMPIFNEQ
    # @param self
    # @param args args for inscruction
    def jumpifneq(self, args):
        self.args_check([
            ['label'],
            ['string', 'int', 'float', 'bool', 'type', 'nil'],
            ['string', 'int', 'float', 'bool', 'type', 'nil']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        if self._type_of(args[1]) == 'nil' or self._type_of(args[2]) == 'nil':
            pass
        elif self._type_of(args[1]) != self._type_of(args[2]):
            errors.operands_types("fail to do JUMPIFNEQ with this types {} and {}".format(
                self._type_of(args[1]),
                self._type_of(args[2])
            ))

        if (a != b):
            return self.jump([args[0]])
            
        self.ip += 1

    ##
    # interpret instruction EXIT
    # @param self
    # @param args args for inscruction
    def exit(self, args):
        self.args_check([
            ['int']
        ], args)

        retcode = self._typed_value(args[0])

        if retcode not in range(0,50):
            errors.operand_value("invalid exit code {}".format(retcode))

        exit(retcode)

    ##
    # interpret instruction DPRINT
    # @param self
    # @param args args for inscruction
    def dprint(self, args):
        self.args_check([
            ['int', 'string', 'float', 'type', 'bool', 'nil']
        ], args)

        errors.eprint(self._value(args[0]))

    ##
    # interpret instruction BREAK
    # @param self
    # @param args args for inscruction
    def break_f(self, args):
        self.args_check([], args)

        errors.eprint("\n------------------------")
        errors.eprint("IPP21 interpret status\n")
        errors.eprint("inscruction pointer: {}".format(self.ip))
        errors.eprint("stack: {}".format(self.stack))
        errors.eprint("return stack: {}".format(self.return_stack))
        errors.eprint("\nsymtable:")
        errors.eprint("   labels: {}".format(self.symtable.labels))
        errors.eprint("   frames: {}".format(self.symtable.frames))
        errors.eprint("   GF frame: {}".format(self.symtable.frames[0].table))
        
        if len(self.symtable.frames) > 1:
            errors.eprint("   LF frame: {}".format(self.symtable.frames[-1].table))

        if hasattr(self.symtable, 'tmpframe'):
            errors.eprint("   TF frame: {}".format(self.symtable.tmpframe.table))

        self.ip += 1