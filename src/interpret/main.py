from program_file import program_file
from interpret import ipp21

program   = program_file("../../spec/int-only/call.src")
interpret = ipp21(program)

interpret.run()


