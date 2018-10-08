import sys
import re


def segment_code(segment):
    return {
        'local' : 'LCL',
        'argument' : 'ARG',
        'this' : 'THIS',
        'that' : 'THAT',
        'temp' : 'TEMP'
    }[segment]


def op_code(operation):
    return {
    'add' : '+',
    'sub' : '-', 
    'neg' : '-',
    'not' : '!',
    'eq' : 'EQ', 
    'gt' : 'GT', 
    'lt' : 'LT', 
    'and' : '&', 
    'or' : '|'
    }[operation]

def write_asm(line):
    outputfile.write(line)
    outputfile.write("\n")


def write_comment(line):
    outputfile.write(line)


def push_constant(i):
    write_asm("// push constant " + i)
    write_asm("@" + i)
    write_asm("D=A")
    write_asm("@SP")
    write_asm("A=M")
    write_asm("M=D")
    write_asm("@SP")
    write_asm("M=M+1")


def push_standard(segment,location):
    write_asm("// push " + segment + " " + location)
    seg_code = segment_code(segment)
    write_asm("// addr = " + seg_code + " + " + location)
    if segment == 'temp':
        write_asm("@5")
        write_asm("D=A")
    else:
        write_asm("@" + seg_code)
        write_asm("D=M")

    write_asm("@" + location)
    write_asm("D=D+A")
    write_asm("@addr")
    write_asm("M=D")
    write_asm("// *SP = *addr")
    write_asm("// A already at @addr")
    write_asm("A=M")
    write_asm("D=M")
    write_asm("@SP")
    write_asm("A=M")
    write_asm("M=D")
    write_asm("// SP++")
    write_asm("@SP")
    write_asm("M=M+1")


def push_pointer(location):
    write_asm("// push pointer " + location)
    if location == "0":
        write_asm("@THIS")
    elif location == "1":
        write_asm("@THAT")
    else:
        write_comment("// Illegal pointer operation")
    write_asm("D=M")
    write_asm("@SP")
    write_asm("A=M")
    write_asm("M=D")
    write_asm("@SP")
    write_asm("M=M+1")


def push_static(location):
    write_asm("// push static " + location)
    write_asm("@" + modulename + "." + location)
    write_asm("D=M")
    write_asm("@SP")
    write_asm("A=M")
    write_asm("M=D")
    write_asm("// SP++")
    write_asm("@SP")
    write_asm("M=M+1")


def pop_standard(segment, location):
    write_asm ("// pop " + segment + " " + location)
    seg_code = segment_code(segment)
    # addr = segmentPointer + location
    if segment == 'temp':
        write_asm("@5")
        write_asm("D=A")
    else:
        write_asm("@" + seg_code)
        write_asm ("D=M")

    
    write_asm ("@" + location)
    write_asm ("D=D+A")
    write_asm ("@addr")
    write_asm ("M=D")
    # SP--
    write_asm ("@SP")
    write_asm ("M=M-1")
    # *addr = *SP
    write_asm ("@SP")
    write_asm ("A=M")
    write_asm ("D=M")
    write_asm ("@addr")
    write_asm ("A=M")
    write_asm ("M=D")

def pop_static(location):
    write_asm("// pop static " + location)
    write_asm("@SP")
    write_asm("M=M-1")
    write_asm("@SP")
    write_asm("A=M")
    write_asm("D=M")
    write_asm("@" + modulename + "." + location)
    write_asm("M=D")


def pop_pointer(location):
    write_asm("// pop pointer " + location)
    write_asm("@SP")
    write_asm("M=M-1")
    write_asm("@SP")
    write_asm("A=M")
    write_asm("D=M")
    if location == "0":
        write_asm("@THIS")
    elif location == "1":
        write_asm("@THAT")
    else:
        write_comment("// Illegal pointer operation")
    write_asm("M=D")


def math_op(op):
    opCode = op_code(op)
    write_asm("// math operation " + op)
    write_asm("@SP")
    write_asm("A=M")
    write_asm("A=A-1")
    write_asm("A=A-1")
    write_asm("D=M")  
    write_asm("A=A+1") 
    write_asm("// " + op)     
    write_asm("D=D" + opCode + "M")     
    write_asm("A=A-1")     
    write_asm("M=D")       
    write_asm("A=A+1")
    write_asm("D=A")
    write_asm("@SP")
    write_asm("M=D")

def comparison_op(op):
    global compareCounter
    compareCode = op_code(op)
    jumpTrueCode = compareCode + "_" + str(compareCounter)
    jumpEndCode = compareCode + "END" + str(compareCounter)
    write_asm("// comparison " + op)
    write_asm("// eq using stack")
    write_asm("@SP")
    write_asm("A=M")
    write_asm("A=A-1")
    write_asm("A=A-1")
    write_asm("D=M    ")  
    write_asm("A=A+1    ")  
    write_asm("D=D-M")
    write_asm("@" + jumpTrueCode)
    write_asm("D;J" + compareCode)
    write_asm("@0")
    write_asm("D=A")
    write_asm("@" + jumpEndCode)
    write_asm("0;JMP")
    write_asm("(" + jumpTrueCode + ")")
    write_asm("// set D to -1")
    write_asm("D=0")
    write_asm("D=D-1")
    write_asm("(" + jumpEndCode + ")")
    write_asm("// D contains true (-1) or false (0) at this point.")
    write_asm("// decrement sp twice")
    write_asm("@SP        // *SP = D")
    write_asm("M=M-1")
    write_asm("M=M-1")
    write_asm("A=M")
    write_asm("M=D")
    write_asm("@SP        // SP++")
    write_asm("M=M+1")
    compareCounter = compareCounter + 1


def unary_op(op):
    write_asm("// unary operation " + op)
    unaryOp = op_code(op)
    write_asm("@SP")
    write_asm("A=M")
    write_asm("A=A-1")
    write_asm("D=M")  
    write_asm("// " + op)     
    write_asm("D=" + unaryOp + "D")     
    #write_asm("A=A-1")     
    write_asm("M=D")       
    write_asm("A=A+1")
    write_asm("D=A")
    write_asm("@SP")
    write_asm("M=D")


def ParseLine(line):
    op = None
    seg = None
    loc = None
    comment_line = re.search('\/\/', line)
    if comment_line is None:
        m = re.search('(\w+)(\s*(\w+)\s*(\d+))?', line)
        if m is not None:
            op = m.group(1)
            seg = m.group(3)
            loc = m.group(4)
    return op, seg, loc


def Compile(op, seg, loc, source_line):
    if op is None:
        op = "none"
    if seg is None:
        seg = "none"
    if loc is None:
        loc = "none"
    if op == 'pop':
        if seg in ['local', 'argument', 'this', 'that', 'temp']:
            pop_standard(seg, loc)
        elif seg == 'static':
            pop_static(loc)
        elif seg == 'pointer':
            pop_pointer(loc)
        else:
            print("Bad op segment " + seg)
    elif op == 'push':
        if seg == 'constant':
            push_constant(loc)
        if seg in ['local', 'argument', 'this', 'that', 'temp']:
            push_standard(seg, loc)
        if seg == 'static':
            push_static(loc)
        if seg == 'pointer':
            push_pointer(loc)
    elif op in ['add', 'sub', 'and', 'or']:
        math_op(op)
    elif op in ['eq', 'gt', 'lt']:
        comparison_op(op)
    elif op in ['not', 'neg']:
        unary_op(op)
    elif op == 'none':
        write_comment(source_line)
    else:
        print("Operation " + op + ", Segment " + seg + " not implemented.")


### Main program.
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " vm_prog")
    exit(-1)

sourcefilename = sys.argv[1]
module_re = re.search('(\w+)\.vm$', sourcefilename)
modulename = module_re.group(1)

outputfilename = sourcefilename.split('.')[0] +  ".asm"
print("Parsing " + sourcefilename + " to " + outputfilename + ", with module " + modulename)

compareCounter = 1

inputfile = open(sourcefilename, "r")
outputfile = open(outputfilename, "w")

for line in inputfile:
    operation = ParseLine(line)
    if operation is not None:
        Compile(operation[0], operation[1], operation[2], line)


inputfile.close()
outputfile.close()



