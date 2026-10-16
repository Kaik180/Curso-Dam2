package Ejemplos;
import java.io.File;
import java.io.IOException;

public class EjemploFile {
    public static void main(String[] args) {
        try {
            // 1. Crear un nuevo directorio
            File directorio = new File("./mi_directorio");
            if (!directorio.exists()) {
                directorio.mkdir();
            }

            // 2. Crear un nuevo archivo vacío dentro del directorio
            File archivo = new File(directorio, "datos.txt");
            if (!archivo.exists()) {
                archivo.createNewFile();
            }

            // 3. Verificar propiedades del archivo y directorio
            System.out.println("¿Existe el archivo?: " + archivo.exists());
            System.out.println("¿Es un archivo?: " + archivo.isFile());
            System.out.println("¿Es un directorio?: " + directorio.isDirectory());
            System.out.println("Tamaño en bytes: " + archivo.length());

            // 4. Renombrar el archivo
            File archivoRenombrado = new File(directorio, "datos_renombrados.txt");
            archivo.renameTo(archivoRenombrado);

            // 5. Listar el contenido del directorio
            String[] elementos = directorio.list();
            System.out.println("Contenido del directorio:");
            if (elementos != null) {
                for (String elem : elementos) {
                    System.out.println(" - " + elem);
                }
            }

            // 6. Eliminar el archivo
            archivoRenombrado.delete();
        } catch (IOException e) {
            System.out.println("Error manipulando File: " + e.getMessage());
        }
    }
}
