// push local i (5)
// addr = LCL + i
@LCL
D=M
@5
D=D+A
@addr
M=D
// *SP = *addr
// A already at @addr
A=M
D=M
@SP
A=M
M=D
// SP++
@SP
M=M+1
