// Initialization Code.
// SP = 256
@256
D=A
@SP
M=D
// Call Sys.init()
// call Sys.init
// push return address
@RET-Sys1
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP - n - 5, n =0
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
// LCL = SP 
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(RET-Sys1)
// end call
// function: Class1.set 0
(Class1.set)
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
// pop static 0
@SP
M=M-1
@SP
A=M
D=M
@Class1.0
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
// pop static 1
@SP
M=M-1
@SP
A=M
D=M
@Class1.1
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
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
// function: Class1.get 0
(Class1.get)
// push static 0
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class1.1
D=M
@SP
A=M
M=D
@SP
M=M+1
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
// function: Class2.set 0
(Class2.set)
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
// pop static 0
@SP
M=M-1
@SP
A=M
D=M
@Class2.0
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
// pop static 1
@SP
M=M-1
@SP
A=M
D=M
@Class2.1
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
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
// function: Class2.get 0
(Class2.get)
// push static 0
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class2.1
D=M
@SP
A=M
M=D
@SP
M=M+1
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
// function: Sys.init 0
(Sys.init)
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// call Class1.set
// push return address
@RET-Sys2
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP - n - 5, n =2
@SP
D=M
@5
D=D-A
@2
D=D-A
@ARG
M=D
// LCL = SP 
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(RET-Sys2)
// end call
// pop temp 0
@5
D=A
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
// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// call Class2.set
// push return address
@RET-Sys3
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP - n - 5, n =2
@SP
D=M
@5
D=D-A
@2
D=D-A
@ARG
M=D
// LCL = SP 
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(RET-Sys3)
// end call
// pop temp 0
@5
D=A
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
// call Class1.get
// push return address
@RET-Sys4
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP - n - 5, n =0
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
// LCL = SP 
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(RET-Sys4)
// end call
// call Class2.get
// push return address
@RET-Sys5
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP - n - 5, n =0
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
// LCL = SP 
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(RET-Sys5)
// end call
(WHILE)
// goto WHILE
@WHILE
0;JMP
