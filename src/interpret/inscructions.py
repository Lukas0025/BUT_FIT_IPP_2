import errors

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
            'str2int': self.str2int,
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
    # function or undefined opcode
    # @param self
    # @param args args for inscruction
    def undefined(self, args):
        error.xml_struct("Undefined OPCODE")

    ##
    # check args types and length if bad exit
    # @param self
    # @param needs array of possible types or args ex. [['var'], ['int', 'float']]
    # @param args args for inscruction
    def args_check(self, needs, args):
        if len(needs) != len(args):
            errors.xml_struct("bad args count for opcodes")

        for i in range(len(needs)):
            try:
                vartype = self.program._get_lower_attrib(args[i])['type']
            except KeyError:
                errors.xml_struct("no type attribute for arg")

            if vartype == "var":
                if "var" not in needs[i]:
                    errors.operands_types("bad type of operand expected {} given ['var']".format(needs[i]))
            elif self._type_of(args[i]) not in needs[i]:
                errors.operands_types("bad type of operand expected {} given {}".format(needs[i], self._type_of(args[i])))
                
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

        if valtype not in ['int', 'float', 'string', 'label', 'bool', 'var', 'type']:
            errors.xml_struct("bad type in type attrib {}".format(vartype))

        if vartype != 'var' and vartype != 'label':
            return "{}@{}".format(vartype, arg.text)
        else:
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
        self.symtable.createframe()
        self.ip += 1

    ##
    # interpret instruction PUSHFRAME
    # @param self
    # @param args args for inscruction
    def pushframe(self, args):
        self.args_check([], args)
        self.symtable.pushframe()
        self.ip += 1

    ##
    # interpret instruction POPFRAME
    # @param self
    # @param args args for inscruction
    def popframe(self, args):
        self.args_check([], args)
        self.symtable.popframe()
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
    def call(self):
        pass

    ##
    # interpret instruction RETURN
    # @param self
    # @param args args for inscruction
    def return_f(self):
        pass

    ##
    # interpret instruction PUSHS
    # @param self
    # @param args args for inscruction
    def pushs(self, args):
        self.args_check([
            ['var'],
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
            ['string', 'int', 'float', 'bool'],
            ['string', 'int', 'float', 'bool']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        if self._type_of(args[1]) != self._typed_value(args[2]):
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
            ['string', 'int', 'float', 'bool'],
            ['string', 'int', 'float', 'bool']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        if self._type_of(args[1]) != self._typed_value(args[2]):
            errors.operands_types("fail to do LT with this types")

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
            ['string', 'int', 'float', 'bool'],
            ['string', 'int', 'float', 'bool']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        if self._type_of(args[1]) != self._typed_value(args[2]):
            errors.operands_types("fail to do LT with this types")

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
            ['bool'],
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

        self.symtable.set_value(
            self._get_typeval(args[0]),
            self._type_of(args[1]),
            chr(self._typed_value(args[1]))
        )

        self.ip += 1

    ##
    # interpret instruction STR2INT
    # @param self
    # @param args args for inscruction
    def str2int(self, args):
        self.args_check([
            ['var'],
            ['string'],
            ['int']
        ], args)

        self.symtable.set_value(
            self._get_typeval(args[0]),
            self._type_of(args[1]),
            ord(self._typed_value(args[1])[self._typed_value(args[2])])
        )

        self.ip += 1

    ##
    # interpret instruction READ
    # @param self
    # @param args args for inscruction
    def read(self):
        pass

    ##
    # interpret instruction WRITE
    # @param self
    # @param args args for inscruction
    def write(self, args):
        print(
            self.symtable.get_value_str(
                self._get_typeval(args[0])
            ), end = ''
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

        self.symtable.set_value(
            self._get_typeval(args[0]),
            "string",
            self._typed_value(args[1])[self._typed_value(args[2])]
        )

        self.ip += 1

    ##
    # interpret instruction SETCHAR
    # @param self
    # @param args args for inscruction
    def setchar(self, args):
        self.args_check([
            ['var'],
            ['int'],
            ['string']
        ], args)

        curr = self._typed_value(args[0])
        curr[self._typed_value(args[1])] = self._typed_value(args[2])[0]

        self.symtable.set_value(
            self._get_typeval(args[0]),
            "string",
            curr
        )

        self.ip += 1

    ##
    # interpret instruction TYPE
    # @param self
    # @param args args for inscruction
    def type_f(self, args):
        self.args_check([
            ['var'],
            ['var']
        ], args)

        self.symtable.set_value(
            self._get_typeval(args[0]),
            "type",
            self._type_of(args[1])
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

        self.symtable.def_label(
            self._val(arg[1])
            self.ip
        )

        self.ip += 1


    ##
    # interpret instruction JUMP
    # @param self
    # @param args args for inscruction
    def jump(self):
        pass

    ##
    # interpret instruction JUMPIFEQ
    # @param self
    # @param args args for inscruction
    def jumpifeq(self):
        pass

    ##
    # interpret instruction JUMPIFNEQ
    # @param self
    # @param args args for inscruction
    def jumpifneq(self):
        pass

    ##
    # interpret instruction EXIT
    # @param self
    # @param args args for inscruction
    def exit(self):
        pass

    ##
    # interpret instruction DPRINT
    # @param self
    # @param args args for inscruction
    def dprint(self):
        pass

    ##
    # interpret instruction BREAK
    # @param self
    # @param args args for inscruction
    def break_f(self):
        pass