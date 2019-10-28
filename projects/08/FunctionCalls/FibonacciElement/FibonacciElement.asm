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
// function: Main.fibonacci 0
(Main.fibonacci)
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
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// comparison lt
// eq using stack
@SP
A=M
A=A-1
A=A-1
D=M    
A=A+1    
D=D-M
@LT_1
D;JLT
@0
D=A
@LTEND1
0;JMP
(LT_1)
// set D to -1
D=0
D=D-1
(LTEND1)
// D contains true (-1) or false (0) at this point.
// decrement sp twice
@SP        // *SP = D
M=M-1
M=M-1
A=M
M=D
@SP        // SP++
M=M+1
// if-goto IF_TRUE
@SP
M=M-1
@SP
A=M
D=M
@IF_TRUE
D;JNE
// goto IF_FALSE
@IF_FALSE
0;JMP
(IF_TRUE)
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
(IF_FALSE)
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
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
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
// call Main.fibonacci
// push return address
@RET-Main2
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
// ARG = SP - n - 5, n =1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
// LCL = SP 
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RET-Main2)
// end call
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
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
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
// call Main.fibonacci
// push return address
@RET-Main3
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
// ARG = SP - n - 5, n =1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
// LCL = SP 
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RET-Main3)
// end call
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
// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// call Main.fibonacci
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
// ARG = SP - n - 5, n =1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
// LCL = SP 
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RET-Sys4)
// end call
(WHILE)
// goto WHILE
@WHILE
0;JMP
