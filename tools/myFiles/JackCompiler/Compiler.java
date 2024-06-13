public class Compiler {

    public static ArrayList<File> getVMFiles(File dir){
        File[] files = dir.listFiles();

        ArrayList<File> result = new ArrayList<File>();

        for (File f : files){
            if (f.getName().endsWith(".vm")){
                result.add(f);
            }
        }

        return result;
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
        ArrayList<File> vmFiles = new ArrayList<File>();
        if (fileIn.isFile()) {
            String path = fileIn.getAbsolutePath();

            if(!Parser.getExt(path).equals(".vm")){
                throw new IllegalArgumentException(".vm file is required!");
            }
            vmFiles.add(fileIn);

            fileOutPath = fileIn.getAbsolutePath().substring(0, file.getAbsolutePath().lastIndexOf(".")) + ".hack"
        } else if(fileIn.isDirectory()){

        }

        filtOut = new File(fileOutPath);
        writer = new CodeWriter(fileOut);

        writer.writeInit();

        for(File f : vmFiles){

        }

        writer.close();

        System.out.println("File created: " + fileOutPath);
    }
}