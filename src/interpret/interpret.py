from inscructions import inscructions
from symtable import symtable
import errors

class ipp21(inscructions):
    def __init__(self, program):
        self.ip = 0
        self.symtable = symtable()
        self.program = program
        self.stack = []

    def _sort_params(self, params):
        sorted_params = []

        for j in range(len(params)):
            for i in range(len(params)):
                if params[i].tag.lower() == "arg{}".format(j + 1):
                    sorted_params.append(params[i])

        if len(sorted_params) != len(params):
            errors.xml_struct("unexpected tag in arguments for {}".format(params.tag.lower()))

        return sorted_params

    def run(self, instruction):
        callable_instruction = self.get_inscrustion(instruction.attrib['opcode'])

        params = self._sort_params(instruction)
        callable_instruction(params)