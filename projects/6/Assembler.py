import sys
#take file as input
#parse file
#output 16 bit numbers in a row

position = 0
varPosition = 16

comp = {
    #a==0
    "0":   "0"+"101010",
    "1":   "0"+"111111",
    "-1":  "0"+"111010",
    "D":   "0"+"001100",
    "A":   "0"+"110000",
    "!D":  "0"+"001101",
    "!A":  "0"+"001111",
    "-D":  "0"+"110011",
    "-A":  "0"+"011111",
    "D+1": "0"+"110111",
    "A+1": "0"+"001110",
    "D-1": "0"+"110010",
    "A-1": "0"+"000010",
    "D+A": "0"+"010011",
    "A-D": "0"+"000111",
    "D&A": "0"+"000000",
    "D|A": "0"+"010101",
    #a==1
    "M":   "1"+"110000",
    "!M":  "1"+"001111",
    "-M":  "1"+"011111",
    "M+1": "1"+"001110",
    "M-1": "1"+"000010",
    "D+M": "1"+"010011",
    "D-M": "1"+"000111",
    "D&M": "1"+"000000",
    "D|M": "1"+"010101",
}

dest = {
    "null":"000",
    "M":   "001",
    "D":   "010",
    "DM":  "011",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "ADM": "111",
}
 
jmp = {
    "null":"000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

sym = {
    "R0":"0",
    "R1":"1",
    "R2":"2",
    "R3":"3",
    "R4":"4",
    "R5":"5",
    "R6":"6",
    "R7":"7",
    "R8":"8",
    "R9":"9",
    "R10":"10",
    "R11":"11",
    "R12":"12",
    "R13":"13",
    "R14":"14",
    "R15":"15",
    "SCREEN":"16384",
    "KBD":"24576",
    "SP":"0",
    "LCL":"1",
    "ARG":"2",
    "THIS":"3",
    "THAT":"4",
}

lblSym = {

}

varSym = {
}


def parse(input):
    input = input.replace('\n', '')
    input=input.replace(" ", "")
    if input[0] == "@":
        try:
            n = bin(int(input.split("@")[1]))[2:].zfill(16)
            return n
        except ValueError:
            #Check if input.split("@")[1] is exists as a symbol and what type it is, or how to handle if not
            var = input.split("@")[1]
            if var in sym.keys():
                return bin(int(sym[var]))[2:].zfill(16)
            elif var in lblSym.keys():
                return bin(int(lblSym[var]))[2:].zfill(16)
            elif var in varSym.keys():
                return bin(int(varSym[var]))[2:].zfill(16)
            else:
                global varPosition
                varSym[var] = varPosition
                varPosition += 1
                return bin(int(varPosition))[2:].zfill(16)
    elif input[0:2] == "//" or input=="\n":
        return ""
    elif input[0] == "(":
        return ""
    else:
        d="null"
        j="null"
        if input.find("=")!=-1:
            d = input.split("=")[0]
            c = input.split("=")[1]
        if input.find(";")!=-1:
            c=input.split(";")[0]
            j = input.split(";")[1]
        return "111" + comp[c] + dest[d] + jmp[j]
    
def addLbl(input):
    global position
    val = input.split("(")[1].split(")")[0]
    lblSym[val] = position

def main():
    file=sys.argv[1]
    ofName = file.split(".")[0]
    output = open(ofName + ".hack", "w")
    global position

    with open(file) as f:
        for line2 in f:
            line2 = line2.replace('\n', '')
            line2=line2.replace(" ", "")
            if line2 != '\n' and line2 != None:
                if line2.find("(")!=-1:
                    addLbl(line2)
    print(lblSym)
    with open(file) as f:
        for line in f:
            if line != '\n' and line != None: l = parse(line)
            if l != "":
                output.write(l + '\n')
                position+=1
            
            
    
    output.close






if __name__=="__main__":
    main()