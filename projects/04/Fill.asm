// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// screensize=8192   
// screenbase=SCREEN
// while true
//     d = KBD
//     if d == 0 
//         fill = 0
//     else
//         fill = -1
//     temp = 8192
//     R1 = SCREEN
//     while temp > 0
//         RAM[R1] = fill
//         R1 = R1 +1
//         temp = temp -1
//     end while
//  end while

(MAINLOOP)
    @KBD
    D=M
    @FILLMINUS1
    D;JGT
    @fill
    M=0
    @SCREENFILL
    0;JMP

(FILLMINUS1)
    @fill
    M=-1

(SCREENFILL)
    @8192
    D=A
    @temp    // temp = 8192
    M=D
    @SCREEN  
    D=A
    @R1      // R1 = screen base address
    M=D

(FILLLOOP)
    // If temp == 0 skip back to reading keyboard.
    @temp  
    D=M
    @MAINLOOP
    D;JEQ

    @fill
    D=M    // put fill value in D
    @R1    // select screen
    A=M    // Address = contents of R1 (Screen base)
    M=D    // put fill in memory A
    @R1    
    M=M+1  // Increment memory address by one
    @temp
    D=M-1  // subtract 1 from total screen words
    @temp
    M=D
    @FILLLOOP  // repeat 8192 times.
    0;JMP


