// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// R2 = 0
// while R1 > 0
//    R2 = R2 + R0
//    R1 = R1 - 1
// wend

// temp storage for R1 counter = @temp
// Put your code here.

// Initialize result (R2) to Zero.
    @R2
    M=0
// load multiplier (R1) into temp.
    @R1
    D=M
    @temp
    M=D

(LOOP)
    // if temp == 0 goto END, we are done.
    @temp
    D=M
    @END
    D;JEQ

    // Add multiplicand to result
    @R2
    D=M
    @R0
    D=D+M
    @R2
    M=D


    // temp = temp - 1
    @temp
    D=M-1
    M=D

    @LOOP
    0;JMP

(END)
    @END
    0;JMP
