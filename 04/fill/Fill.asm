(RESTART)
@SCREEN
D=A
@0
M=D	//SCREEN empieza en la posición RAM0


(KBDCHECK)
@KBD
D=M
@BLACK
D;JGT	//JUMP si presciona la tecla entonces black
@WHITE
D;JEQ	//ELSE salte a el while es 0 el color es white

@KBDCHECK
0;JMP
(BLACK)
@1
M=-1	//Ponemos el  (-1=11111111111111)
@CHANGE
0;JMP

(WHITE)
@1
M=0
@CHANGE
0;JMP
(CHANGE)
@1
D=M	//D contenedor BLACK or WHITE

@0
A=M	//posicion del SCREEN
M=D

@0
D=M+1	//INC el siguiente PIXEL
@KBD
D=A-D	//KBD-SCREEN=A

@0
M=M+1	//INC TO NEXT PIXEL
A=M

@CHANGE
D;JGT

@RESTART
0;JMP
