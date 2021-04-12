from program_file import program_file
from interpret import ipp21

program   = program_file("../../spec/int-only/label.src")
interpret = ipp21(program)

while True:
    instruction = program.get(interpret.ip)
    interpret.run(instruction)

    if interpret.ip >= program.length():
        break


