@2
M = 0

(LOOP)
@0
D=M
@END
D;JEQ

// Cargamos R1
@1
D=M

@2
M=M+D

// Decremento del ciclo
@0
M=M-1
@LOOP
0;JMP
(END)
@END
0;JEQ
