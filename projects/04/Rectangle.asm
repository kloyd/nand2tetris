// Program: Rectangle.asm
// Draws a filled rectangle


    @R0
    D=M
    @n
    M=D  // n = RAM[0]

    @i
    M=0  // i = 0

    @SCREEN
    D=A
    @address
    M=D      // screen base address

(LOOP)
    @i
    D=M
    @n
    D=D-M
    @END
    D;JGT   // if i > n goto END

    @address
    A=M
    M=-1  // RAM[address] = -1 (16 pixels)

    @i
    M=M+1
    @32
    D=A
    @address
    M=D+M
    @LOOP
    0; JMP

(END)
    @END
    0; JMP
    