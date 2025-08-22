@i //bilau
M=1
@sum
M=0
(LOOP)
@i

        
D=M
@R0
D=D-M
@STOP
D;JGT
   @i   

   //laulau
D=M
@sum
M=D+M
@i
M=M+1
@LOOP
0;JMP
(STOP)
@sum
D=M
