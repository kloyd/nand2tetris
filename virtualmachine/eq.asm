// eq using stack
@SP
A=M
A=A-1
A=A-1
D=M      
A=A+1      
D=D-M
@EQ1
D;JEQ
@0
D=A
@EQEND1
0;JMP
(EQ1)
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
(END)
@END
0;JMP
