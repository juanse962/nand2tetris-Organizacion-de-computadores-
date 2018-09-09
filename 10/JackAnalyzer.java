/**
*Clase principal para compilar javac JackAnalyzer.java CompilationEngine.java  JackTokenizer.java
*java JackAnalyzer directory|filename.jack
*/
import java.io.File;
import java.util.ArrayList;

public class JackAnalyzer {

    public static ArrayList<File> getJackFiles(File dir){

        File[] files = dir.listFiles();
        ArrayList<File> result = new ArrayList<File>();
        if (files == null) return result;
        for (File f:files){
            if (f.getName().endsWith(".jack")){

                result.add(f);
            }
        }
        return result;
    }

    public static void main(String[] args) {

        if (args.length != 1){

            System.out.println("Usa:java JackAnalyzer directorio|fileInName.jack");

        }else {

            String fileInName = args[0];

            File fileIn = new File(fileInName);

            String fileOutPath = "", tokenFileOutPath = "";

            File fileOut,tokenFileOut;

            ArrayList<File> jackFiles = new ArrayList<File>();

            if (fileIn.isFile()) {

                //if es un unico archivo .jack
                String path = fileIn.getAbsolutePath();

                if (!path.endsWith(".jack")) {

                    throw new IllegalArgumentException(".jack se necesita");

                }

                jackFiles.add(fileIn);

            } else if (fileIn.isDirectory()) {

                //obtiene todos los .jack del directorio
                jackFiles = getJackFiles(fileIn);

                //if no hay archivos en este directorio
                if (jackFiles.size() == 0) {
                    throw new IllegalArgumentException("No hay archivos .jack en este directorio");
                }
            }

            for (File f: jackFiles) {

                fileOutPath = f.getAbsolutePath().substring(0, f.getAbsolutePath().lastIndexOf(".")) + ".xml";
                tokenFileOutPath = f.getAbsolutePath().substring(0, f.getAbsolutePath().lastIndexOf(".")) + "T.xml";
                fileOut = new File(fileOutPath);
                tokenFileOut = new File(tokenFileOutPath);
                CompilationEngine compilationEngine = new CompilationEngine(f,fileOut,tokenFileOut);
                compilationEngine.compileClass();
                System.out.println("Archivo creado : " + fileOutPath);
                System.out.println("Archivo creado : " + tokenFileOutPath);
            }
        }
    }
}
