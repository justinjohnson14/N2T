//endFrame = LCL
//retAddr = *(endFrame-5)
//*ARG = pop()
//SP=ARG+1
//THAT = *(endFrame-1)
//THIS = *(endFrame-2)
//ARG = *(endFrame-3)
//LCL = *(endFrame-4)
//goto retAddr

@LCL
D=M
@R14
M=D
@5
A=D-A
D=M
@R15
M=D
@SP
D=M
@ARG
M=D
@SP
M=D+1
@R14
D=M-1
@THAT
M=D
D=D-1
@THIS
M=D
D=D-1
@ARG
M=D
D=D-1
@LCL
M=D
D=D-1
@retAddr
0;JMP