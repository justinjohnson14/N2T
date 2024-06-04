//Pop stack onces onto local variable 2

//SP--
@SP
M=M-1

//store location to save pop in addr
@1
D=M
@2
D=D+A
@addr
M=D

//copy value at stack pointer to addr
@SP
A=M
D=M
@addr
A=M
M=D




//D = data register
//@loads values into A
//D=A means d equals the values thats in A register
//A=M means a equals the current value of memory pointed to by A
//M=D means the new value pointed to by A is equal to D