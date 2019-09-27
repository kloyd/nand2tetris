// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm

// Puts the first argument[0] elements of the Fibonacci series
// in the memory, starting in the address given in argument[1].
// Argument[0] and argument[1] are initialized by the test script 
// before this code starts running.

// push argument 1
// addr = ARG + 1
@ARG
D=M
@1
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
// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
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
// pop that 0
@THAT
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
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// end push constant
// pop that 1
@THAT
D=M
@1
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

(MAIN_LOOP_START)

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
// if-goto COMPUTE_ELEMENT
@SP
M=M-1
@SP
A=M
D=M
@COMPUTE_ELEMENT
D;JNE
// goto END_PROGRAM
@END_PROGRAM
0;JMP

(COMPUTE_ELEMENT)

// push that 0
// addr = THAT + 0
@THAT
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
// end push that
// push that 1
// addr = THAT + 1
@THAT
D=M
@1
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
// end push that
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
// pop that 2
@THAT
D=M
@2
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

// push pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// end push pointer
// push constant 1
@1
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
// add
D=D+M
A=A-1
M=D
A=A+1
D=A
@SP
M=D
// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
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

// goto MAIN_LOOP_START
@MAIN_LOOP_START
0;JMP

(END_PROGRAM)
