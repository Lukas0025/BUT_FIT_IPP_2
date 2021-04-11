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
        if len(args) != 2:
            exit(1)

        self.symtable.set_value(
            self._get_typeval(args[0]),
            self.symtable.get_type_str(self._get_typeval(args[1])),
            self.symtable.get_value_str(self._get_typeval(args[1]))
        )

        self.ip += 1

    def createframe(self, args):
        self.symtable.createframe()
        self.ip += 1

    def pushframe(self, args):
        self.symtable.pushframe()
        self.ip += 1
    
    def popframe(self, args):
        self.symtable.popframe()
        self.ip += 1

    def defvar(self, args):
        self.symtable.def_var(
            self._get_typeval(args[0])
        )

        self.ip += 1

    def call(self):
        pass

    def return_f(self):
        pass

    def pushs(self, args):
        self.stack.append({
            'type': self.symtable.get_type_str(self._get_typeval(args[0])),
            'value': self.symtable.get_value_str(self._get_typeval(args[0]))
        })

        self.ip += 1


    def pops(self, args):
        var = self.stack.pop()

        self.symtable.set_value(
            self._get_typeval(args[0]),
            var['type'],
            var['value']
        )

        self.ip += 1

    def add(self):
        pass

    def sub(self):
        pass

    def mul(self):
        pass

    def idiv(self):
        pass

    def lt(self):
        pass

    def gt(self):
        pass

    def eq(self):
        pass

    def and_f(self):
        pass

    def or_f(self):
        pass

    def not_f(self):
        pass

    def int2char(self, args):
        self.symtable.set_value(
            self._get_typeval(args[0]),
            self.symtable.get_type_str(self._get_typeval(args[1])),
            chr(int(self.symtable.get_value_str(self._get_typeval(args[1]))))
        )

        self.ip += 1

    def str2int(self):
        pass

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