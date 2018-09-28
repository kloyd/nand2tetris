// pop segment i
// segment = local, i = 2
// addr = LCL + 2
@LCL
D=M
@2
D=D+A
@addr
// SP--
M=D
@SP
M=M-1
// *addr = *SP
@SP
A=M
D=M
@addr
A=M
M=D