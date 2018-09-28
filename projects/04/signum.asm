// Program signum.asm
// Computes: if R0 > 0
//                 R1 = 1
//             else
//                 R1 = 0

    @R0
    D=M   // D= RAM[0]

    @POSITIVE
    D;JGT  // IF R0>0 GOTO 8

    @R1
    M=0

    @END
    0;JMP

(POSITIVE)
    @R1
    M=1

(END)
    @END
    0;JMP
