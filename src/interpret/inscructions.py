import errors

class inscructions:
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

    def undefined(self):
        exit(1)

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
                

    def _value(self, arg):
        return self.symtable.get_value_str(self._get_typeval(arg))

    def _type_of(self, arg):
        return self.symtable.get_type_str(self._get_typeval(arg))

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

    def _get_typeval(self, arg):

        try:
            vartype = self.program._get_lower_attrib(arg)['type']
        except KeyError:
            errors.xml_struct("no type attribute for arg")

        if vartype != 'var':
            return "{}@{}".format(vartype, arg.text)
        else:
            return arg.text

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

    def createframe(self, args):
        self.args_check([], args)
        self.symtable.createframe()
        self.ip += 1

    def pushframe(self, args):
        self.args_check([], args)
        self.symtable.pushframe()
        self.ip += 1
    
    def popframe(self, args):
        self.args_check([], args)
        self.symtable.popframe()
        self.ip += 1

    def defvar(self, args):
        self.args_check([
            ['var']
        ], args)

        self.symtable.def_var(
            self._get_typeval(args[0])
        )

        self.ip += 1

    def call(self):
        pass

    def return_f(self):
        pass

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

        out = a // b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            out_type,
            str(out)
        )

        self.ip += 1

    def div(self, args):
        self.args_check([
            ['var'],
            ['int', 'float'],
            ['int', 'float']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        out = a / b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            'float',
            str(out)
        )

        self.ip += 1

    def lt(self, args):
        self.args_check([
            ['var'],
            ['string', 'int', 'float', 'bool'],
            ['string', 'int', 'float', 'bool']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        out = a < b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            'bool',
            str(out)
        )

        self.ip += 1


    def gt(self, args):
        self.args_check([
            ['var'],
            ['string', 'int', 'float', 'bool'],
            ['string', 'int', 'float', 'bool']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        out = a > b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            'bool',
            str(out)
        )

        self.ip += 1

    def eq(self, args):
        self.args_check([
            ['var'],
            ['string', 'int', 'float', 'bool'],
            ['string', 'int', 'float', 'bool']
        ], args)

        a = self._typed_value(args[1])
        b = self._typed_value(args[2])

        out = a == b

        self.symtable.set_value(
            self._get_typeval(args[0]),
            'bool',
            str(out)
        )

        self.ip += 1

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

    def read(self):
        pass

    def write(self, args):
        print(
            self.symtable.get_value_str(
                self._get_typeval(args[0])
            ), end = ''
        )

        self.ip += 1

    def concat(self):
        pass

    def strlen(self):
        pass

    def getchar(self):
        pass

    def setchar(self):
        pass

    def type_f(self):
        pass

    def label(self):
        pass

    def jump(self):
        pass

    def jumpifeq(self):
        pass

    def jumpifneq(self):
        pass

    def exit(self):
        pass

    def dprint(self):
        pass

    def break_f(self):
        pass