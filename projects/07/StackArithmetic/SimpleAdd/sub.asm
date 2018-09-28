// stack addition
// Basic design.
// D = *(SP-2)
// D = D <op> *(SP-1)
// SP=SP-2
// *SP=D
// SP++


@SP
A=M
A=A-1
A=A-1
D=M      
A=A+1      
D=D+M     
A=A-1     
M=D       
A=A+1
D=A
@SP
M=D

