

#Write code blocks for certain actions

#Push constant i onto stack
def popConsti(i: int):
    string = """
    @i
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1"""
    string = string.replace("i", str(i))
    return string

#pop stack onto memory segment[i]
#Where segment can be LCL, ARG, THIS, THAT and i is a non negative integer
def popLocali(segment: str, i):
    string = """
    @SP
    M=M-1

    //store location to save pop in addr
    @seg
    D=M
    @i
    D=D+A
    @addr
    M=D

    //copy value at stack pointer to addr
    @SP
    A=M
    D=M
    @addr
    A=M
    M=D"""
    string = string.replace("seg", segment)
    string = string.replace("i", str(i))