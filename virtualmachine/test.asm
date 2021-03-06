// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/07/MemoryAccess/BasicTest/BasicTest.vm

// Executes pop and push commands using the virtual memory segments.
// push constant 10
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
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
// push constant 21
@21
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 22
@22
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop argument 2
@ARG
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
// pop argument 1
@ARG
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
// push constant 36
@36
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop this 6
@THIS
D=M
@6
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
// push constant 42
@42
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 45
@45
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 5
@THAT
D=M
@5
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
// push constant 510
@510
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop temp 6
@5
D=M
@6
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
// push that 5
// addr = THAT + 5
@THAT
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
// push this 6
// addr = THIS + 6
@THIS
D=M
@6
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
// push this 6
// addr = THIS + 6
@THIS
D=M
@6
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
// push temp 6
// addr = TEMP + 6
@5
D=M
@6
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
// push pointer 0
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push pointer 1
@THAT
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
// pop pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D
// push static 1
@test.1
D=M
@SP
A=M
M=D
// SP++
@SP
M=M+1
// pop static 0
@SP
M=M-1
@SP
A=M
D=M
@test.0
M=D
