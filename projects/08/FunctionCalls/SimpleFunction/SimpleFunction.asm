// function: SimpleFunction.test 2
(SimpleFunction.test)
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// push local 0
@LCL
D=M
@0
D=D+A
@addr
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// end push local
// push local 1
@LCL
D=M
@1
D=D+A
@addr
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// end push local
// math operation add
@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
D=D+M
A=A-1
M=D
A=A+1
D=A
@SP
M=D
// unary operation not
@SP
A=M
A=A-1
D=M
// not
D=!D
M=D
A=A+1
D=A
@SP
M=D
// push argument 0
@ARG
D=M
@0
D=D+A
@addr
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// end push argument
// math operation add
@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
D=D+M
A=A-1
M=D
A=A+1
D=A
@SP
M=D
// push argument 1
@ARG
D=M
@1
D=D+A
@addr
M=D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// end push argument
// math operation sub
@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
D=D-M
A=A-1
M=D
A=A+1
D=A
@SP
M=D
// return 
// FRAME = LCL
@LCL
D=M
@R13
M=D
// RET = *(FRAME-5)
@5
D=D-A
A=D
D=M
@R15
M=D
// # *ARG = pop()
// pop argument 0
@ARG
D=M
@0
D=D+A
@address
M=D
@SP
M=M-1
@SP
A=M
D=M
@address
A=M
M=D
// SP = ARG + 1
@ARG
D=M
D=D+1
@SP
M=D
// THAT = *(FRAME - 1)
@R13
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
// THIS = *(FRAME - 2)
@R13
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
// ARG = *(FRAME - 3)
@R13
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
// LCL = *(FRAME - 4)
@R13
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
// goto RET
@R15
A=M
0;JMP
