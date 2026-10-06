package org.example;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;

public class Ejemplo_path {
    static void main() {
        //archivo creado y revisado
        List<String> lista = new ArrayList<>();
        lista.add("Ejemplo de path");
        Path p1 = Path.of("./src/ficheros/fichPath.txt");
        try {
            if (!Files.exists(p1)) {
                Files.write(p1,lista);
                System.out.println("Archivo creado.");
            } else {
                System.out.println("El archivo ya existe.");
            }
        }catch (IOException e){
            System.out.println("no se ha podido1");
        }
        //crear carpeta
        Path rutaCarpeta = Path.of("datos_usuario");
        try {
            Files.createDirectory(rutaCarpeta);
        }catch (IOException e){
            System.out.println("no se ha podido2");
        }

        //renombrar un archivo
        try {
            Path rutaRenombrada = Path.of("renombrado.txt");
            Files.move(p1, rutaRenombrada);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }


        //listar todo lo de esta carpeta
        Path carpetaActual = Path.of(".");
        File[] loQueHay = carpetaActual.toFile().listFiles();
        for (File f : loQueHay) {
            System.out.println("- " + f.getName());
        }

        //Eliminar un archivo
        Path archivoABorrar = Path.of("voyASerBorradoPath.txt");
           try {
               if (!Files.exists(archivoABorrar)) {
                   Files.createFile(archivoABorrar);
               }
               Files.delete(archivoABorrar);
           } catch (Exception e) {
               throw new RuntimeException(e);
           }


    }
}
