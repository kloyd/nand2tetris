// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/08/ProgramFlow/BasicLoop/BasicLoop.vm

// Computes the sum 1 + 2 + ... + argument[0] and pushes the 
// result onto the stack. Argument[0] is initialized by the test 
// script before this code starts running.
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// pop local 0
@LCL
D=M
@0
D=D+A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
(LOOP_START)
// push argument 0
// addr = ARG + 0
@ARG
D=M
@0
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
// end push argument
// push local 0
// addr = LCL + 0
@LCL
D=M
@0
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
// end push local
// math operation add
@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
// add
D=D+M
A=A-1
M=D
A=A+1
D=A
@SP
M=D
// pop local 0
@LCL
D=M
@0
D=D+A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
// push argument 0
// addr = ARG + 0
@ARG
D=M
@0
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
// sub
D=D-M
A=A-1
M=D
A=A+1
D=A
@SP
M=D
// pop argument 0
@ARG
D=M
@0
D=D+A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
// push argument 0
// addr = ARG + 0
@ARG
D=M
@0
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
// end push argument
// if-goto LOOP_START
@SP
M=M-1
@SP
A=M
D=M
@LOOP_START
D;JNE
// push local 0
// addr = LCL + 0
@LCL
D=M
@0
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
// end push local
