import sys
from pathlib import Path
import os


stackCommands = ["push", "pop"]
alCommands = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
bCommands = ["label", "goto", "if-goto"]
fCommands = ["function", "call", "return"]

global position, arthJumpFlag, newLabel, output


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
                return popTemplate("5", str(int(splt[2])+5), False)
            case "pointer":
                n = "THIS" if splt[2] == "0" else "THAT"
                return popTemplate(n, splt[2], True)
            case "static":
                return popTemplate(str(16+int(splt[2])), splt[2], True)
            

def popTemplate(segment: str, index: str, isDirect: bool):
    
    ptrCode = "D=A\n" if (isDirect) else "D=M\n@" + str(index) + "\nD=D+A\n"

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
    ptrCode = "" if (isDirect) else "@" + str(index) + "\n" + "A=D+A\nD=M\n"

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
        case "and":
            return arithTemplate() + "M=M&D\n"
        case "or":
            return arithTemplate() + "M=D|M\n"
        case "gt":
            v = logiTemplate("JLE")
            arthJumpFlag+=1
            return v
        case "lt":
            v =  logiTemplate("JGE")
            arthJumpFlag+=1
            return v
        case "eq":
            v =  logiTemplate("JNE")
            arthJumpFlag+=1
            return v
        case "not":
            return "@SP\nA=M-1\nM=!M\n"
        case "neg":
            return "D=0\n@SP\nA=M-1\nM=D-M\n"


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
        "@FALSE" + str(arthJumpFlag) + "\n" +
        "D;" + t + "\n" +
        "@SP\n" +
        "A=M-1\n" +
        "M=-1\n" +
        "@CONTINUE" + str(arthJumpFlag) + "\n" +
        "0;JMP\n" +
        "(FALSE" + str(arthJumpFlag) + ")\n" +
        "@SP\n" +
        "A=M-1\n" +
        "M=0\n" +
        "(CONTINUE" + str(arthJumpFlag) + ")\n"
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
                arithTemplate() + 
                "@" + line.split(" ")[1] + "\n" +
                "D;JNE\n"
            )


def preFrameTemplate(pos):
    return (
        "@FRAME\n"+
        "D=M-1\n"+
        "AM=D\n"+
        "D=M\n"+
        "@" + pos + "\n"+
        "M=D\n"
    )



def f(line):
    global programLine
    global newLabel
    if line == "return":
        return (
            "@LCL\n"+
            "D=M\n"+
            "@FRAME\n"+
            "M=D\n"+
            "@5\n"+
            "A=D-A\n"+
            "D=M\n"+
            "@RET\n"+
            "M=D\n"+
            popTemplate("ARG", 0, False)+
            "@ARG\n"+
            "D=M\n"+
            "@SP\n"+
            "M=D+1\n"+
            preFrameTemplate("THAT") +
            preFrameTemplate("THIS") +
            preFrameTemplate("ARG") +
            preFrameTemplate("LCL") +
            "@RET\n"+
            "A=M\n"+
            "0;JMP\n"
        )
    elif line.split(" ")[0] == "function":
        result = "(" + line.split(" ")[1] + ")\n"
        for i in range(int(line.split(" ")[2])-1):
            result = result + "@SP\nM=M+1\n"
        return result
    elif line.split(" ")[0] == "call":
        returnLabel = "RETURN_LABEL" + str(newLabel)
        newLabel += 1
        nArgs = line.split(" ")[2]
        return(
            "@" + returnLabel + "\n" + "D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"+
            pushTemplate("LCL",0,True)+
            pushTemplate("ARG",0,True)+
            pushTemplate("THIS",0,True)+
            pushTemplate("THAT",0,True)+
            "@SP\n" +
            "D=M\n" +
            "@5\n" +
            "D=D-A\n" +
            "@" + nArgs + "\n" +
            "D=D-A\n" +
            "@ARG\n" +
            "M=D\n" +
            "@SP\n" +
            "D=M\n" +
            "@LCL\n" +
            "M=D\n" +
            "@" + line.split(" ")[1] + "\n" +
            "0;JMP\n" +
            "(" + returnLabel + ")\n"
        )
    else:
        return ""





def parse(command: str):
    global position
    try: 
        command2 = command.split(" ")[0] 
    except: 
        command2 = command
    command = command.lstrip()
    command2 = command2.lstrip()
    if command2 in stackCommands:
        return stack(command)
    elif command2 in alCommands:
        return al(command2)
    elif command2 in bCommands:
        return b(command)
    elif command2 in fCommands:
        return f(command)
    elif command[0:2] == "//":
        return ""
    elif command == "":
        return ""
    else:
        sys.exit("Incorrect syntax in line: " + str(position))

def parseFile(file):
    #ofName = file.split(".")[0]
    #output = open(ofName + ".asm", "w")
    global position, arthJumpFlag, programLine, newLabel, output
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

def main():
    path=sys.argv[1]
    global output, newLabel
    newLabel = 0
    if Path(path).is_dir():
        ofName = path.split("/")[-2]
        output = open(path + ofName + ".hack", "w")
        for subdir, dirs, files in os.walk(path):
            for file in files:
                if(file.split(".")[1]) == "asm":
                    parseFile(path + file)
    else:
        ofName = path.split(".")[0]
        output = open(ofName + ".hack", "w")
        parseFile(path)

    output.close




if __name__=="__main__":
    main()