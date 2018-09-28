// push pointer 0
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
M=M-1
@SP
A=M
D=M
@THIS
M=D

// push pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D
