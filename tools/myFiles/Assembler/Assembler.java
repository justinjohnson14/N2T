public class Assembler {

    public static ArrayList<File> getasmFiles(File dir){
        File[] files = dir.listFiles();

        ArrayList<File> result = new ArrayList<File>();

        for (File f : files){
            if (f.getName().endsWith(".vm")){
                result.add(f);
            }
        }

        return result;
    }

    public static ParseFile(String fileIn){
        //loop through each line in file
        //make sure line is not invalid
        //call parseLine on the line
        Private Scanner cmds;
        try {
            cmds = new Scanner(fileIn);

            String preprocesed = "";
            String line = "";

            while(cmds.hasNext()){
                line = noComments(cmds.nextLine()).trim();

                if(line.length()>0){
                    preprocesed += line + "\n";
                }
            }

            cmds = new Scanner(preprocesed.trim());
        } catch(FileNotFoundException){
            System.out.println("File not found!");
        }

        while(cmds.hasNextLine()){

            currentCmd = cmds.nextLine();
            argument1 = "";//initialize arg1
            argument2 = -1;//initialize arg2
    
            String[] segs = currentCmd.split(" ");
    
            if (segs.length > 3){
            
                throw new IllegalArgumentException("Too much arguments!");
    
            }
    
            if (arithmeticCmds.contains(segs[0])){
            
                argType = ARITHMETIC;
                argument1 = segs[0];
    
            }else if (segs[0].equals("return")) {
            
                argType = RETURN;
                argument1 = segs[0];
    
            }else {
            
                argument1 = segs[1];
    
                if(segs[0].equals("push")){
                
                    argType = PUSH;
    
                }else if(segs[0].equals("pop")){
                
                    argType = POP;
    
                }else if(segs[0].equals("label")){
                
                    argType = LABEL;
    
                }else if(segs[0].equals("if-goto")){
                
                    argType = IF;
    
                }else if (segs[0].equals("goto")){
                
                    argType = GOTO;
    
                }else if (segs[0].equals("function")){
                
                    argType = FUNCTION;
    
                }else if (segs[0].equals("call")){
                
                    argType = CALL;
    
                }else {
                
                    throw new IllegalArgumentException("Unknown Command Type!");
    
                }
    
                if (argType == PUSH || argType == POP || argType == FUNCTION || argType == CALL){
                
                    try {
                    
                        argument2 = Integer.parseInt(segs[2]);
    
                    }catch (Exception e){
                    
                        throw new IllegalArgumentException("Argument2 is not an integer!");
    
                    }
    
                }
        }

        }
    }

    public static ParseLine(){

    }
}

public static void main(String[] args){
    if(args.length != 1){
        System.out.println("Usage:")
    } else{
        String fileInName = args[0];
        File fileIn = new File(fileInName);
        String fileOutPath = "";
        File fileOut;
        CodeWriter writer;
        ArrayList<File> asmFiles = new ArrayList<File>();
        if (fileIn.isFile()) {
            String path = fileIn.getAbsolutePath();

            if(!Parser.getExt(path).equals(".vm")){
                throw new IllegalArgumentException(".vm file is required!");
            }
            asmFiles.add(fileIn);

            fileOutPath = fileIn.getAbsolutePath().substring(0, file.getAbsolutePath().lastIndexOf(".")) + ".hack"
        } else if(fileIn.isDirectory()){
            asmFiles = getasmFiles(flieIn);

            if(asmFiles.size()==0){
                throw new IllegalArgumentException("No vm file in this directory");
            }

            fileOutPath = fileIn.getAbsolutePath() +"/"+fileIn.getName() + ".asm";
        }

        filtOut = new File(fileOutPath);
        writer = new CodeWriter(fileOut);

        writer.writeInit();

        for(File f : asmFiles){
            //parse file
        }

        writer.close();

        System.out.println("File created: " + fileOutPath);
    }
}