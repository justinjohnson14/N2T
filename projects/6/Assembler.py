import sys
#take file as input
#parse file
#output 16 bit numbers in a row

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

predef = {
    "":""
}


def parse(input):
    if input[0] == "@":
        return bin(int(input.split("@")[1]))[2:].zfill(16)
    else:
        return""

def main():
    file=sys.argv[1]
    ofName = file.split(".")[0]
    output = open(ofName + ".hack", "w")

    with open(file) as f:
        for line in f:
            l = parse(line)
            if l != "":
                print(l)
            
            
    
    output.close






if __name__=="__main__":
    main()