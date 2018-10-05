// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/07/StackArithmetic/StackTest/StackTest.vm

// Executes a sequence of arithmetic and logical operations
// on the stack. 
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// comparison eq
// eq using stack
@SP
A=M
A=A-1
A=A-1
D=M    
A=A+1    
D=D-M
@EQ_1
D;JEQ
@0
D=A
@EQEND1
0;JMP
(EQ_1)
D=D-1
(EQEND1)
// D contains true (-1) or false (0) at this point.
// decrement sp twice
@SP        // *SP = D
M=M-1
M=M-1
A=M
M=D
@SP        // SP++
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// comparison eq
// eq using stack
@SP
A=M
A=A-1
A=A-1
D=M    
A=A+1    
D=D-M
@EQ_2
D;JEQ
@0
D=A
@EQEND2
0;JMP
(EQ_2)
D=D-1
(EQEND2)
// D contains true (-1) or false (0) at this point.
// decrement sp twice
@SP        // *SP = D
M=M-1
M=M-1
A=M
M=D
@SP        // SP++
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// comparison eq
// eq using stack
@SP
A=M
A=A-1
A=A-1
D=M    
A=A+1    
D=D-M
@EQ_3
D;JEQ
@0
D=A
@EQEND3
0;JMP
(EQ_3)
D=D-1
(EQEND3)
// D contains true (-1) or false (0) at this point.
// decrement sp twice
@SP        // *SP = D
M=M-1
M=M-1
A=M
M=D
@SP        // SP++
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// comparison lt
// eq using stack
@SP
A=M
A=A-1
A=A-1
D=M    
A=A+1    
D=D-M
@LT_4
D;JLT
@0
D=A
@LTEND4
0;JMP
(LT_4)
D=D-1
(LTEND4)
// D contains true (-1) or false (0) at this point.
// decrement sp twice
@SP        // *SP = D
M=M-1
M=M-1
A=M
M=D
@SP        // SP++
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// comparison lt
// eq using stack
@SP
A=M
A=A-1
A=A-1
D=M    
A=A+1    
D=D-M
@LT_5
D;JLT
@0
D=A
@LTEND5
0;JMP
(LT_5)
D=D-1
(LTEND5)
// D contains true (-1) or false (0) at this point.
// decrement sp twice
@SP        // *SP = D
M=M-1
M=M-1
A=M
M=D
@SP        // SP++
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// comparison lt
// eq using stack
@SP
A=M
A=A-1
A=A-1
D=M    
A=A+1    
D=D-M
@LT_6
D;JLT
@0
D=A
@LTEND6
0;JMP
(LT_6)
D=D-1
(LTEND6)
// D contains true (-1) or false (0) at this point.
// decrement sp twice
@SP        // *SP = D
M=M-1
M=M-1
A=M
M=D
@SP        // SP++
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// comparison gt
// eq using stack
@SP
A=M
A=A-1
A=A-1
D=M    
A=A+1    
D=D-M
@GT_7
D;JGT
@0
D=A
@GTEND7
0;JMP
(GT_7)
D=D-1
(GTEND7)
// D contains true (-1) or false (0) at this point.
// decrement sp twice
@SP        // *SP = D
M=M-1
M=M-1
A=M
M=D
@SP        // SP++
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// comparison gt
// eq using stack
@SP
A=M
A=A-1
A=A-1
D=M    
A=A+1    
D=D-M
@GT_8
D;JGT
@0
D=A
@GTEND8
0;JMP
(GT_8)
D=D-1
(GTEND8)
// D contains true (-1) or false (0) at this point.
// decrement sp twice
@SP        // *SP = D
M=M-1
M=M-1
A=M
M=D
@SP        // SP++
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// comparison gt
// eq using stack
@SP
A=M
A=A-1
A=A-1
D=M    
A=A+1    
D=D-M
@GT_9
D;JGT
@0
D=A
@GTEND9
0;JMP
(GT_9)
D=D-1
(GTEND9)
// D contains true (-1) or false (0) at this point.
// decrement sp twice
@SP        // *SP = D
M=M-1
M=M-1
A=M
M=D
@SP        // SP++
M=M+1
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
D=A
@SP
A=M
M=D
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
// push constant 112
@112
D=A
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
// sub
D=D-M
A=A-1
M=D
A=A+1
D=A
@SP
M=D
// unary operationneg
// math operation and
@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
// and
D=D&M
A=A-1
M=D
A=A+1
D=A
@SP
M=D
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// math operation or
@SP
A=M
A=A-1
A=A-1
D=M
A=A+1
// or
D=D|M
A=A-1
M=D
A=A+1
D=A
@SP
M=D
// unary operationnot
