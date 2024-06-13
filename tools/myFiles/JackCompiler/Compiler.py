import sys
from pathlib import Path
import os
import re


keywords = ["class", "constructor", "function", "method", 
            "field", "static", "var", "int", "char", 
            "boolean","void","true","false","null","this",
            "let","do","if","else","while","return"]

symbol = ["{","}","(",")","[","]",".",",",";","+","-","*",
          "/","&","|","<",">","=","~"]

intConstant = "^[0-9]+$"
stringConstant = '^"[^"\n]*"$'
identifier = "^[a-zA-Z]+.*$"

global position, arthJumpFlag, newLabel, output
mc = False

def tokenizer(input):
    global mc
    if input in keywords:
        return "<keyword>" + input + "</keyword>\n"
    elif input in symbol:
        return "<symbol>" + input + "</symbol>\n"
    elif re.search(intConstant, input)!=None:
        return "<intConst>" + input + "</intConst>\n"
    elif re.search(stringConstant, input)!=None:
        return "<stringConst>" + input + "</stringConst>\n"
    elif re.search(identifier, input)!=None:
        return "<identifier>" + input + "</identifier>\n"
    elif input[:2] == "/*":
        mc = True
    elif input[:2] == "*/":
        mc = False
    else:
        r=input
        for i in input:
            if i in symbol:
                r = r.replace(i," "+i+" ")
                return parse(r)


def parse(command: str):
    global position, mc
    #input is a singular line
    spltCmd = command.split(" ")
    ret = ""
    for c in spltCmd:
        if c[:2] == "//":
            return ret
        x = tokenizer(c)
        if not mc and x != None:
            ret += x
    return ret

def parseFile(file):
    global position, arthJumpFlag, programLine, newLabel, output
    arthJumpFlag = 0
    position = 0
    programLine = 0

    with open(file) as f:
        for line in f:
            #position += 1
            line = line.strip()
            if line != '\n' and line != None: l = parse(line)
            if l != "" and l != None:
                output.write(l)
                programLine += 1

def main():
    path=sys.argv[1]
    global output, newLabel
    newLabel = 0
    if Path(path).is_dir():
        ofName = path.split("/")[-2]
        output = open(path + ofName + ".chk", "w")
        for subdir, dirs, files in os.walk(path):
            for file in files:
                if(file.split(".")[1]) == "jack":
                    parseFile(path + file)
    else:
        ofName = path.split(".")[0]
        output = open(ofName + ".chk", "w")
        parseFile(path)

    output.close




if __name__=="__main__":
    main()