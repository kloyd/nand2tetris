// Sum1toN.asm

	@R0
	D=M
	@n
	M=D
	@i
	M=1
	@sum
	M=0

(LOOP)
	@i
	D=M
	@n
	D=D-M
	@STOP
	D;JGT  // if i > n goto STOP

	@sum
	D=M     // D = sum
	@i
	D=D+M   // D = D + i
	@sum
	M=D     // sum = D
	@i
	M=M+1   // i++
	@LOOP
	0;JMP

(STOP)
    @sum
    D=M
    @R1
    M=D

(END)
    @END
    0;JMP

    