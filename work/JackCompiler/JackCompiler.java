import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.Scanner;


enum TokenType{
    KEYWORD,
    SYMBOL,
    IDENTIFIER,
    INT_CONST,
    STRING_CONST,
    NONE
}

enum Keyword{
    CLASS,
    METHOD,
    FUNCTION,
    CONSTRUCTOR,
    INT,
    BOOLEAN,
    CHAR,
    VOID,
    VAR,
    STATIC,
    FIELD,
    LET,
    DO,
    IF,
    ELSE,
    WHILE,
    RETURN,
    TRUE,
    FALSE,
    NULL,
    THIS,
    NONE
}

public class JackCompiler {
    public static ArrayList<File> getVMFiles(File dir){
        File[] files = dir.listFiles();

        ArrayList<File> result = new ArrayList<File>();

        for (File f:files){

            if (f.getName().endsWith(".vm")){

                result.add(f);

            }

        }

        return result;

    }

    public static void main(String[] args) {

        //String fileInName = "/Users/xuchen/Documents/IntroToComputerSystem/nand2tetris/projects/07/MemoryAccess/StaticTest/";

        if (args.length < 1){

            System.out.println("Usage:java VMtranslator [filename|directory]");

        }else {

            String fileInName = args[0];

            File fileIn = new File(fileInName);

            ArrayList<File> vmFiles = new ArrayList<File>();

            String fileOutPath = "";

            if (fileIn.isFile()) {

                //if it is a single file, see whether it is a vm file
                String path = fileIn.getAbsolutePath();

                vmFiles.add(fileIn);

                fileOutPath = fileIn.getAbsolutePath().substring(0, fileIn.getAbsolutePath().lastIndexOf("/"));

            } else if (fileIn.isDirectory()) {

                //if it is a directory get all vm files under this directory
                vmFiles = getVMFiles(fileIn);

                //if no vn file in this directory
                if (vmFiles.size() == 0) {

                    throw new IllegalArgumentException("No vm file in this directory");

                }

                fileOutPath = fileIn.getAbsolutePath().substring(0, fileIn.getAbsolutePath().lastIndexOf("/"));
            }

            for (File f : vmFiles) {

                JackTokenizer tokenizer = new JackTokenizer(f);
                String outString = "";
                FileWriter output;
                System.out.println(fileOutPath + "/" + f.getName().substring(0, f.getName().lastIndexOf(".")) + ".xml");

                try {
                    output = new FileWriter(fileOutPath + "/" + f.getName().substring(0, f.getName().lastIndexOf(".")) + ".xml");
                    while (tokenizer.hasMoreTokens()) {
                        tokenizer.advance();
                        
                        switch (tokenizer.tokenType()) {
                            case KEYWORD:
                                outString = "<keyword> " + tokenizer.keyword() +" </keyword>";
                            case SYMBOL:
                                outString = "<symbol> " + tokenizer.symbol() +" </symbol>";
                            case IDENTIFIER:
                                outString = "<identifier> " + tokenizer.identifier() +" </identifier>";
                            case INT_CONST:
                                outString = "<intConstant> " + tokenizer.intVal() +" </intConstant>";
                            case STRING_CONST:
                                outString = "<stringConstant> " + tokenizer.stringVal() +" </stringConstant>";
                            default:
                                break;
                        }
                        output.write(outString);
                    }
                    output.close();
                } catch(Exception e){
                    System.err.println(e.getMessage());
                    output = null;
                }

            }
        }
    }
}

class JackTokenizer {
    public String token = "";
    public Scanner scan;
    public boolean mlComment = false;
    public static ArrayList<String> keywords = new ArrayList<String>();
    public static String symbols = "{}()[].,;+-*/&|<>=~";

    static {
        keywords.add("class"); keywords.add("method"); keywords.add("function"); keywords.add("constructor"); keywords.add("int"); keywords.add("boolean"); 
        keywords.add("char"); keywords.add("void"); keywords.add("var"); keywords.add("static"); keywords.add("field"); keywords.add("let"); keywords.add("do"); 
        keywords.add("if"); keywords.add("else"); keywords.add("while"); keywords.add("return"); keywords.add("true"); keywords.add("false"); keywords.add("null"); 
        keywords.add("this");
    }

    public JackTokenizer(File file){
        try{
            this.scan = new Scanner(file);
        } catch(Exception e){
            System.err.println(e.getMessage());
        }
    }

    public boolean hasMoreTokens(){
        return scan.hasNext();
    }

    public void advance(){
        token = scan.next().strip();
        if(token.equals("//")){
            token = scan.nextLine();
        } else if (token.equals("*/")){
            mlComment = false;
            return;
        }else if(token.equals("/**") || token.strip().equals("/*") || mlComment) {
            mlComment = true;
            return;
        }  else {
            System.out.println(token.strip());
        }
    }

    public TokenType tokenType(){
        if(keywords.contains(token)){
            return TokenType.KEYWORD;
        } else if(symbols.contains(token)){
            return TokenType.SYMBOL;
        } else if(0 <= Integer.parseInt(token) && Integer.parseInt(token) <= 32767){
            return TokenType.INT_CONST;
        } else if(token.matches("[^\"\n]*")){
            return TokenType.STRING_CONST;
        } else if(token.matches("^[^0-9].[a-zA-Z0-9_]*$")){
            return TokenType.IDENTIFIER;
        }else {
            return TokenType.NONE;
        }
    }

    public String keyword(){
        if(tokenType()!=TokenType.KEYWORD){
            return token;
        } else {
            return "";
        }
    }

    public char symbol(){
        if (tokenType() == TokenType.SYMBOL){
            return token.charAt(0);
        } else {
            return ' ';
        }
    }

    public String identifier(){
        if (tokenType() == TokenType.IDENTIFIER){
            return token;
        } else {
            return "";
        }
    }

    public Integer intVal(){
        if (tokenType() == TokenType.INT_CONST){
            return Integer.getInteger(token);
        } else {
            return -1;
        }
    }

    public String stringVal(){
        if (tokenType() == TokenType.STRING_CONST){
            return token;
        } else {
            return "";
        }
    }
}

class CompilationEngine {
    public CompilationEngine(){

    }

    public void compileClass(){

    }

    public void compileClassVarDec(){

    }

    public void compileSubroutine(){

    }

    public void compileParameterList(){

    }

    public void compileVarDec(){

    }

    public void compileStatements(){

    }

    public void compileLet(){

    }

    public void compileIf(){

    }

    public void compileWhile(){

    }

    public void compileDo(){

    }

    public void compileReturn(){
        
    }

    public void compileExpression(){

    }

    public void compileTerm(){

    }

    public void compileExpressionList(){

    }

    
}
