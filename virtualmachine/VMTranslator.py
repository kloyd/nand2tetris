import sys
import re
import glob
import os

class Parser:
    def __init__(self):
        print('init') # constructor

    def hasMoreCommands(self):
        print('hasMoreCommands')

    def advance(self):
        print('advance')

    def commandType(self):
        print('commandType')

    def arg1(self):
        print('arg1')

    def arg2(self):
        print('arg2')


def segment_code(segment):
    return {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
        'temp': 'TEMP'
    }[segment]


def op_code(operation):
    return {
        'add': '+',
        'sub': '-',
        'neg': '-',
        'not': '!',
        'eq': 'EQ',
        'gt': 'GT',
        'lt': 'LT',
        'and': '&',
        'or': '|'
    }[operation]


def write_asm(output_file, line):
    output_file.write(line)
    output_file.write("\n")


def write_comment(output_file, line):
    output_file.write(line)


def push_constant(output_file, i):
    write_asm(output_file, "// push constant " + i)
    write_asm(output_file, "@" + i)
    write_asm(output_file, "D=A")
    write_asm(output_file, "@SP")
    write_asm(output_file, "A=M")
    write_asm(output_file, "M=D")
    write_asm(output_file, "@SP")
    write_asm(output_file, "M=M+1")
    write_asm(output_file, "// end push constant")


def push_standard(output_file, segment, location):
    write_asm(output_file, "// push " + segment + " " + location)
    seg_code = segment_code(segment)
    # write_asm(output_file, "// address = " + seg_code + " + " + location)
    if segment == 'temp':
        write_asm(output_file, "@5")
        write_asm(output_file, "D=A")
    else:
        write_asm(output_file, "@" + seg_code)
        write_asm(output_file, "D=M")

    write_asm(output_file, "@" + location)
    write_asm(output_file, "D=D+A")
    write_asm(output_file, "@addr")
    write_asm(output_file, "M=D")
    # write_asm(output_file, "// *SP = *addr")
    # write_asm(output_file, "// A already at @addr")
    write_asm(output_file, "A=M")
    write_asm(output_file, "D=M")
    write_asm(output_file, "@SP")
    write_asm(output_file, "A=M")
    write_asm(output_file, "M=D")
    # write_asm(output_file, "// SP++")
    write_asm(output_file, "@SP")
    write_asm(output_file, "M=M+1")
    write_asm(output_file, "// end push " + segment)


def push_pointer(output_file, location):
    write_asm(output_file, "// push pointer " + location)
    if location == "0":
        write_asm(output_file, "@THIS")
    elif location == "1":
        write_asm(output_file, "@THAT")
    else:
        write_comment(output_file, "// Illegal pointer operation")
    write_asm(output_file, "D=M")
    write_asm(output_file, "@SP")
    write_asm(output_file, "A=M")
    write_asm(output_file, "M=D")
    write_asm(output_file, "@SP")
    write_asm(output_file, "M=M+1")
    write_asm(output_file, "// end push pointer")


def push_static(output_file, module_name, location):
    write_asm(output_file, "// push static " + location)
    write_asm(output_file, "@" + module_name + "." + location)
    write_asm(output_file, "D=M")
    write_asm(output_file, "@SP")
    write_asm(output_file, "A=M")
    write_asm(output_file, "M=D")
    # write_asm(output_file, "// SP++")
    write_asm(output_file, "@SP")
    write_asm(output_file, "M=M+1")


def pop_standard(output_file, segment, location):
    write_asm(output_file, "// pop " + segment + " " + location)
    seg_code = segment_code(segment)
    # address = segmentPointer + location
    if segment == 'temp':
        write_asm(output_file, "@5")
        write_asm(output_file, "D=A")
    else:
        write_asm(output_file, "@" + seg_code)
        write_asm(output_file, "D=M")

    write_asm(output_file, "@" + location)
    write_asm(output_file, "D=D+A")
    write_asm(output_file, "@address")
    write_asm(output_file, "M=D")
    # SP--
    write_asm(output_file, "@SP")
    write_asm(output_file, "M=M-1")
    # *addr = *SP
    write_asm(output_file, "@SP")
    write_asm(output_file, "A=M")
    write_asm(output_file, "D=M")
    write_asm(output_file, "@address")
    write_asm(output_file, "A=M")
    write_asm(output_file, "M=D")


def pop_static(output_file, modulename, location):
    write_asm(output_file, "// pop static " + location)
    write_asm(output_file, "@SP")
    write_asm(output_file, "M=M-1")
    write_asm(output_file, "@SP")
    write_asm(output_file, "A=M")
    write_asm(output_file, "D=M")
    write_asm(output_file, "@" + modulename + "." + location)
    write_asm(output_file, "M=D")


def pop_pointer(output_file, location):
    write_asm(output_file, "// pop pointer " + location)
    write_asm(output_file, "@SP")
    write_asm(output_file, "M=M-1")
    write_asm(output_file, "@SP")
    write_asm(output_file, "A=M")
    write_asm(output_file, "D=M")
    if location == "0":
        write_asm(output_file, "@THIS")
    elif location == "1":
        write_asm(output_file, "@THAT")
    else:
        write_comment(output_file, "// Illegal pointer operation")
    write_asm(output_file, "M=D")


def math_op(output_file, op):
    opCode = op_code(op)
    write_asm(output_file, "// math operation " + op)
    write_asm(output_file, "@SP")
    write_asm(output_file, "A=M")
    write_asm(output_file, "A=A-1")
    write_asm(output_file, "A=A-1")
    write_asm(output_file, "D=M")
    write_asm(output_file, "A=A+1")
    # write_asm(output_file, "// " + op)
    write_asm(output_file, "D=D" + opCode + "M")
    write_asm(output_file, "A=A-1")
    write_asm(output_file, "M=D")
    write_asm(output_file, "A=A+1")
    write_asm(output_file, "D=A")
    write_asm(output_file, "@SP")
    write_asm(output_file, "M=D")


def comparison_op(output_file, op):
    global compareCounter
    compareCode = op_code(op)
    jumpTrueCode = compareCode + "_" + str(compareCounter)
    jumpEndCode = compareCode + "END" + str(compareCounter)
    write_asm(output_file, "// comparison " + op)
    write_asm(output_file, "// eq using stack")
    write_asm(output_file, "@SP")
    write_asm(output_file, "A=M")
    write_asm(output_file, "A=A-1")
    write_asm(output_file, "A=A-1")
    write_asm(output_file, "D=M    ")
    write_asm(output_file, "A=A+1    ")
    write_asm(output_file, "D=D-M")
    write_asm(output_file, "@" + jumpTrueCode)
    write_asm(output_file, "D;J" + compareCode)
    write_asm(output_file, "@0")
    write_asm(output_file, "D=A")
    write_asm(output_file, "@" + jumpEndCode)
    write_asm(output_file, "0;JMP")
    write_asm(output_file, "(" + jumpTrueCode + ")")
    write_asm(output_file, "// set D to -1")
    write_asm(output_file, "D=0")
    write_asm(output_file, "D=D-1")
    write_asm(output_file, "(" + jumpEndCode + ")")
    write_asm(output_file, "// D contains true (-1) or false (0) at this point.")
    write_asm(output_file, "// decrement sp twice")
    write_asm(output_file, "@SP        // *SP = D")
    write_asm(output_file, "M=M-1")
    write_asm(output_file, "M=M-1")
    write_asm(output_file, "A=M")
    write_asm(output_file, "M=D")
    write_asm(output_file, "@SP        // SP++")
    write_asm(output_file, "M=M+1")
    compareCounter = compareCounter + 1


def unary_op(output_file, op):
    write_asm(output_file, "// unary operation " + op)
    unaryOp = op_code(op)
    write_asm(output_file, "@SP")
    write_asm(output_file, "A=M")
    write_asm(output_file, "A=A-1")
    write_asm(output_file, "D=M")
    write_asm(output_file, "// " + op)
    write_asm(output_file, "D=" + unaryOp + "D")
    # write_asm("A=A-1")
    write_asm(output_file, "M=D")
    write_asm(output_file, "A=A+1")
    write_asm(output_file, "D=A")
    write_asm(output_file, "@SP")
    write_asm(output_file, "M=D")


def write_label(output_file, label):
    write_asm(output_file, "(" + label + ")")


def write_if_goto(output_file, label):
    write_asm(output_file, "// if-goto " + label)
    write_asm(output_file, "@SP")
    write_asm(output_file, "M=M-1")
    write_asm(output_file, "@SP")
    write_asm(output_file, "A=M")
    write_asm(output_file, "D=M")
    write_asm(output_file, "@" + label)
    write_asm(output_file, "D;JNE")


def write_goto(output_file, label):
    write_asm(output_file, "// goto " + label)
    write_asm(output_file, "@" + label)
    write_asm(output_file, "0;JMP")


def write_init(output_file):
    write_asm("// Initialization Code.")


def write_function(output_file, module, name, arg_count):
    args = int(arg_count)
    write_asm(output_file, "// function: " + name + " " + arg_count)
    write_asm(output_file, "(" + name + ")")
    n = 0
    # push number of locals required clear to zero.
    while n < args:
        push_constant(output_file, '0')
        n = n + 1


# call module n
def write_call(output_file, module, name):
    write_asm(output_file, "// call " + name)
    # push return-address
    return_address = "RET-" + module
    # push return-address
    write_asm(output_file, "@" + return_address)
    write_asm(output_file, "D=A")
    # standard stack push of contents of D register.
    push_d_register(output_file)

    # push LCL
    write_asm(output_file, "@LCL")
    write_asm(output_file, "D=M")
    # standard stack push of contents of D register.
    push_d_register(output_file)
    # push ARG
    write_asm(output_file, "@ARG")
    write_asm(output_file, "D=M")
    push_d_register(output_file)
    # push THIS
    write_asm(output_file, "@THIS")
    write_asm(output_file, "D=M")
    push_d_register(output_file)
    # push THAT
    write_asm(output_file, "@THAT")
    write_asm(output_file, "D=M")
    push_d_register(output_file)
    # ARG = SP-n-5
    write_asm(output_file, "@SP")
    write_asm(output_file, "D=A")  # d = sp
    # d = d - 5
    write_asm(output_file, "@5")
    write_asm(output_file, "D=D-A")
    # d = d - n
    write_asm(output_file, "@2") # arg number!!!!
    write_asm(output_file, "D=D-A")
    # store D into ARG
    # LCL = SP
    # goto f (f = function name)
    # write the return-address label
    write_asm(output_file, "(" + return_address + ")")
    write_asm(output_file, "// end call")


def push_d_register(output_file):
    write_asm(output_file, "@SP")
    write_asm(output_file, "A=M")
    write_asm(output_file, "M=D")
    write_asm(output_file, "@SP")
    write_asm(output_file, "M=M+1")


def write_return(output_file, module, name):
    write_asm(output_file, "// return ")


def parse_line(line):
    op = None
    seg = None
    loc = None
    comment_line = re.search('^//', line)
    if comment_line is None:
        m = re.search('^(\w+)(\s*(\w+)\s*(\d+))?', line)
        if m is not None:
            op = m.group(1)
            if op == 'label':
                n = re.search('(\w+)\s*(\w+)', line)
                seg = n.group(2)
            elif op == 'if':
                n = re.search('^(if-goto)\s*(\w+)', line)
                seg = n.group(2)
            elif op == 'goto':
                n = re.search('^(goto)\s*(\w+)', line)
                seg = n.group(2)
            elif op == "function":
                n = re.search('^(function)\s+([\w.]+)\s+(\d+)', line)
                seg = n.group(2)
                loc = n.group(3)
            elif op == "call":
                n = re.search('^(call)\s+([\w.]+)', line)
                seg = n.group(2)
                loc = ""
            elif op == 'return':
                seg = ""
                loc = ""
            else:
                seg = m.group(3)
                loc = m.group(4)
    #       else:
    #           write_comment("skipping line: " + line)
    #   else:
    #       write_comment("comment line: " + line)
    return op, seg, loc


def compile_line(outputfile, module, op, seg, loc, source_line):
    if op is None:
        op = "none"
    if seg is None:
        seg = "none"
    if loc is None:
        loc = "none"
    if op == 'pop':
        if seg in ['local', 'argument', 'this', 'that', 'temp']:
            pop_standard(outputfile, seg, loc)
        elif seg == 'static':
            pop_static(outputfile, module, loc)
        elif seg == 'pointer':
            pop_pointer(outputfile, loc)
        else:
            print("Bad op segment " + seg)
    elif op == 'push':
        if seg == 'constant':
            push_constant(outputfile, loc)
        if seg in ['local', 'argument', 'this', 'that', 'temp']:
            push_standard(outputfile, seg, loc)
        if seg == 'static':
            push_static(outputfile, module, loc)
        if seg == 'pointer':
            push_pointer(outputfile, loc)
    elif op in ['add', 'sub', 'and', 'or']:
        math_op(outputfile, op)
    elif op in ['eq', 'gt', 'lt']:
        comparison_op(outputfile, op)
    elif op in ['not', 'neg']:
        unary_op(outputfile, op)
    elif op == 'none':
       sys.stdout.write(source_line)
    elif op == 'label':
        write_label(outputfile, seg)
    elif op == 'if':
        write_if_goto(outputfile, seg)
    elif op == 'goto':
        write_goto(outputfile, seg)
    elif op == 'function':
        write_function(outputfile, module, seg, loc)
    elif op == 'call':
        write_call(outputfile, module, seg)
    elif op == 'return':
        write_return(outputfile, "", "")
    else:
        print("Operation " + op + ", Segment " + seg + ", loc " + loc + " not implemented.")


def parseAndCompileOneFile(outputfile, sourcefilename, modulename):

    print("Parsing " + sourcefilename + " to " + outputfilename + ", with module " + modulename)
    inputfile = open(sourcefilename, "r")
    for line in inputfile:
        operation = parse_line(line)
        if operation is not None:
            compile_line(outputfile, modulename, operation[0], operation[1], operation[2], line)

    inputfile.close()


def parseAndCompileFile(source_file):
    module_re = re.search('(\w+)\.vm$', source_file)
    modulename = module_re.group(1)
    outputfilename = source_file.split('.')[0] + ".asm"
    outputfile = open(outputfilename, "w")
    parseAndCompileOneFile(outputfile, source_file, modulename)
    outputfile.close()


def parseAndCompileDir(source_dir):
    outputfilename = os.path.basename(source_dir) + ".asm"
    print(outputfilename)
    os.chdir(source_dir)
    print("directory compile: " + outputfilename)
    outputfile = open(outputfilename, "w")
    for file in glob.glob("*.vm"):
        module_re = re.search('(\w+)\.vm$', file)
        modulename = module_re.group(1)
        parseAndCompileOneFile(outputfile, file, modulename)

    print("closing " + outputfile.name)
    outputfile.close()

### Main program.
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " vm_prog")
    exit(-1)

compareCounter = 1

sourcefilename = sys.argv[1]
outputfilename = sourcefilename.split('.')[0] + ".asm"
# is this dir name or file name?
if sourcefilename.endswith('.vm'):
    parseAndCompileFile(sourcefilename)
else:
    parseAndCompileDir(sourcefilename)
