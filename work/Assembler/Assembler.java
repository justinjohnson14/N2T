class Assembler {

}

class Parser {
    public Parser(String file){
        //Opens input file stream and gets ready to parse it
    }

    public boolean hasMoreLines(){
        //Are there more lines in the input?
    }

    public void advance(){
        //Skips over whitespace and comments if necesary,
        //reads the next instruction from the input, and makes it the current instruction
        //This method should be called only if has more lines is true
        //Initially there is no current instruction
    }

    public InstructionType instructionType(){
        //Returns the type of the current instruction
        //A_INSTRUCTION for @xxx
        //C_INSTRUCTION for dest=comp;jump
        //L_INSTRUCTION FOR (xxx), where xxx is a symbol
    }

    public String symbol(){
        //if the current instruction is (xxx) return the sumbol xxx 
        //should be called only if instruction type is A_INSTRUCTION or L_
    }

    public String dest(){
        //Returns the symbolic dest part of the current C instruction
    }

    public String comp(){
        //Returns the symbolic comp part of the current instruction
    }

    public String jump(){
        //returns the sumbolic jump part of the current instruction
    }
}

class Coder {
    public Coder(){

    }

    public String dest(String str){
        //Returns binary code of the dest mnemonic
    }
    public String comp(String str){
        //returns binary code of the comp
    }
    public String jump(String str){
        //returns binary code of the jump
    }
}

class SymbolTable {
    public SymbolTable(){
        //Creates a new empty symbol table

    }

    public void addEntry(String sym, int addr){
        //adds symbol to the table
    }

    public boolean contains(String sym){
        //does the symbol table contain the given symbol
    }

    public int getAddress(String sym){
        //returns the address associated with the symbol
    }
}

public void main(String[] args){
    //Create procedure here
}