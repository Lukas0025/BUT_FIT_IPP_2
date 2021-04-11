from inscructions import inscructions
from symtable import symtable

class ipp21(inscructions):
    def __init__(self, program):
        self.ip = 0
        self.symtable = symtable()
        self.program = program

    def run(self, instruction):
        callable_instruction = self.get_inscrustion(instruction.attrib['opcode'])

        params = instruction
        callable_instruction(params)