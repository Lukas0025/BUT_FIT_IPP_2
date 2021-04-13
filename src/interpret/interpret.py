from program_file import program_file
from ipp21 import ipp21
import sys, getopt
import errors

def main(argv):
    program = None
    input_file = None

    try:
        opts, args = getopt.getopt(argv,"",["source=","input=", "help"])
    except getopt.GetoptError:
        errors.eprint("interpret.py --source <sourcefile> --input <inputfile>")
        errors.cli_params("bad cli params used")
        
    for opt, arg in opts:
        if opt == '--help':
            print('simple IPP21 interpret\n\ninterpret.py --source <sourcefile> --input <inputfile>')
            sys.exit()
        elif opt in ("--source"):
            program = program_file(arg)
        elif opt in ("--input"):
            try:
                input_file = open(arg, "r")
            except FileNotFoundError as error:
                errors.open_input_file(error)
            except Exception:
                errors.open_input_file("unexpected error")

    if (program == None):
        errors.cli_params("no --source param")

    
    interpret = ipp21(program)
    interpret.run(input_file)

if __name__ == "__main__":
   main(sys.argv[1:])


