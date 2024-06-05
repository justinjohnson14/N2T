import sys


stackCommands = ["push", "pop"]
alCommands = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
bCommands = ["label", "goto", "if-goto"]
fCommands = ["function", "call", "return"]

global position, arthJumpFlag


def stack(line):
    splt = line.split(" ")
    if splt[0] == "push":
        match splt[1]:
            case "constant":
                return "@" + splt[2] + "\n" + "D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
            case "local":
                return pushTemplate("LCL", splt[2], False)
            case "argument":
                return pushTemplate("ARG", splt[2], False)
            case "this":
                return pushTemplate("THIS", splt[2], False)    
            case "that":
                return pushTemplate("THAT", splt[2], False)
            case "temp":
                return pushTemplate("5", splt[2], False)
            case "pointer":
                n = "THIS" if splt[2] == "0" else "THAT"
                return pushTemplate(n, splt[2], True)
            case "static":
                return pushTemplate(str(16+int(splt[2])), splt[2], True)
    else:
        match splt[1]:
            case "local":
                return popTemplate("LCL", splt[2], False)
            case "argument":
                return popTemplate("ARG", splt[2], False)
            case "this":
                return popTemplate("THIS", splt[2], False)    
            case "that":
                return popTemplate("THAT", splt[2], False)
            case "temp":
                return popTemplate("5", splt[2]+5, False)
            case "pointer":
                n = "THIS" if splt[2] == "0" else "THAT"
                return popTemplate(n, splt[2], True)
            case "static":
                return popTemplate(str(16+int(splt[2])), splt[2], True)
            

def popTemplate(segment: str, index: str, isDirect: bool):
    
    ptrCode = "D=A\n" if (isDirect) else "D=M\n@" + index + "\nD=D+A\n"

    return (
        "@"+ segment + "\n"+
        ptrCode +
        "@R13\n"+
        "M=D\n"+
        "@SP\n"+
        "AM=M-1\n"+
        "D=M\n"+
        "@R13\n"+
        "A=M\n"+
        "M=D\n"
    )

def pushTemplate(segment: str, index: int, isDirect: bool):
    ptrCode = "" if (isDirect) else "@" + index + "\n" + "A=D+A\nD=M\n"

    return(
        "@" + segment + "\n" +
        "D=M\n" +
        ptrCode + 
        "@SP\n" + 
        "A=M\n"+
        "M=D\n"+
        "@SP\n"+
        "M=M+1\n"
    )


def al(line):
    global arthJumpFlag
    match line:
        case "add":
            return arithTemplate() + "M=M+D\n"
        case "sub":
            return arithTemplate() + "M=M-D\n"
        case "neg":
            return "D=0\n@SP\nA=M-1\nM=D-M\n"
        case "eq":
            arthJumpFlag+=1
            return logiTemplate("JNE")
        case "gt":
            arthJumpFlag+=1
            return logiTemplate("JGT")
        case "lt":
            arthJumpFlag+=1
            return logiTemplate("JLT")
        case "and":
            return arithTemplate() + "M=M&D\n"
        case "or":
            return arithTemplate() + "M=D|M\n"
        case "not":
            return "@SP\nA=M-1\nM=!M\n"


def arithTemplate():
    return (
        "@SP\n"+
        "AM=M-1\n"+
        "D=M\n"+
        "A=A-1\n"
    )

def logiTemplate(t):
    return (
        "@SP\n" +
        "AM=M-1\n" +
        "D=M\n" +
        "A=A-1\n" +
        "D=M-D\n" +
        "@FALSE" + arthJumpFlag + "\n" +
        "D;" + t + "\n" +
        "@SP\n" +
        "A=M-1\n" +
        "M=-1\n" +
        "@CONTINUE" + arthJumpFlag + "\n" +
        "0;JMP\n" +
        "(FALSE" + arthJumpFlag + ")\n" +
        "@SP\n" +
        "A=M-1\n" +
        "M=0\n" +
        "(CONTINUE" + arthJumpFlag + ")\n"
    )


def b(line):
    match line.split(" ")[0]:
        case "label":
            return "("+line.split(" ")[1]+")\n"
        case "goto":
            return (
                "@" + line.split(" ")[1] + "\n" +
                "0;JMP\n"
            )
        case "if-goto":
            return (
                "@SP\n"+
                "D=M\n" +
                "@" + line.split(" ")[1] + "\n" +
                "D;JNE\n"
            )






#def f(line):
    #if line.split(" ")[0] == "push":
        #print("push")
    #else:
        #print("pop")








def parse(command: str):
    global position
    command = command.lstrip()
    if command.split(" ")[0] in stackCommands:
        return stack(command)
    elif command in alCommands:
        return al(command)
    elif command.split(" ")[0] in bCommands:
        return b(command)
    elif command.split(" ")[0] in fCommands:
        return f(command)
    elif command[0:2] == "//":
        return ""
    elif command == "":
        return ""
    else:
        sys.exit("Incorrect syntax in line: " + str(position))

def main():
    file=sys.argv[1]
    ofName = file.split(".")[0]
    output = open(ofName + ".asm", "w")
    global position, arthJumpFlag, programLine
    arthJumpFlag = 0
    position = 0
    programLine = 0

    with open(file) as f:
        for line in f:
            position += 1
            line = line.rstrip()
            if line != '\n' and line != None: l = parse(line)
            if l != "":
                output.write(l)
                programLine += 1

    
    output.close






if __name__=="__main__":
    main()