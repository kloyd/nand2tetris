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
// function: Sys.init 0
(Sys.init)
// push constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// pop pointer 0
@SP
M=M-1
@SP
A=M
D=M
@THIS
M=D
// push constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D
// call Sys.main
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
@Sys.main
0;JMP
(RET-Sys2)
// end call
// pop temp 1
@5
D=A
@1
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
(LOOP)
// goto LOOP
@LOOP
0;JMP
// function: Sys.main 5
(Sys.main)
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
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// pop pointer 0
@SP
M=M-1
@SP
A=M
D=M
@THIS
M=D
// push constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D
// push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// pop local 1
@LCL
D=M
@1
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
// push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// pop local 2
@LCL
D=M
@2
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
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// pop local 3
@LCL
D=M
@3
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
// push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// call Sys.add12
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
@Sys.add12
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
// push local 2
@LCL
D=M
@2
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
// push local 3
@LCL
D=M
@3
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
// push local 4
@LCL
D=M
@4
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
// function: Sys.add12 0
(Sys.add12)
// push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// pop pointer 0
@SP
M=M-1
@SP
A=M
D=M
@THIS
M=D
// push constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
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
// push constant 12
@12
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
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
