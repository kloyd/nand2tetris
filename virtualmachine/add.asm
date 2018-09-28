// add using stack
@SP        // SP--
M=M-1
@SP        // D = *SP
A=M
D=M
@SP        // SP--
M=M-1
@SP        // D = D + *SP
A=M
D=D+M
@SP        // *SP = D
A=M
M=D
@SP        // SP++
M=M+1
(END)
@END
0;JMP
