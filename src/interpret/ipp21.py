from inscructions import inscructions
from symtable import symtable
import errors

class ipp21(inscructions):
    def __init__(self, program):
        self.ip = 0
        self.symtable = symtable()
        self.program = program
        self.stack = []
        self.return_stack = []

    def _sort_params(self, params):
        sorted_params = []

        for j in range(len(params)):
            for i in range(len(params)):
                if params[i].tag.lower() == "arg{}".format(j + 1):
                    sorted_params.append(params[i])

        if len(sorted_params) != len(params):
            errors.xml_struct("unexpected tag in arguments for {}".format(params.tag.lower()))

        return sorted_params

    def _opcode(self, inscruction):
        attrs = self.program._get_lower_attrib(inscruction)

        if 'opcode' not in attrs:
            errors.xml_struct("no opcode for inscruction ip:{}".format(self.ip))

        return attrs['opcode']

    def run(self, input_file):

        self.infile = input_file

        #get labels first
        for i in range(self.program.length()):
            self.ip = i
            instruction = self.program.get(self.ip)
            if self._opcode(instruction) == 'label':
                self.label(self._sort_params(instruction))

        #now run program
        self.ip = 0
        while True:
            instruction = self.program.get(self.ip)
            opcode = self._opcode(instruction)
            
            if opcode != 'label':
                callable_instruction = self.get_inscrustion(opcode)
                
                params = self._sort_params(instruction)
                callable_instruction(params)
            else:
                self.ip += 1
                
            if self.ip >= self.program.length():
                break