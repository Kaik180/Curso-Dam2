package org.example;

import java.io.File;
import java.io.IOException;

public class Ejemplo_File {
    static void main() {
        File archivo = new File("mi_documento.txt");
        //Crear archivo y revisar que existe.
        try {
            if (!archivo.exists()) {
                boolean creado = archivo.createNewFile();
                System.out.println("¿Archivo creado?: " + creado);
            } else {
                System.out.println("El archivo ya existe en el disco.");
            }
        } catch (IOException e) {
            System.out.println("Error al crear el archivo: " + e.getMessage());
        }

        //Crear carpeta
        File carpeta = new File("datos_usuario");

        if (!carpeta.exists()) {
            boolean creada = carpeta.mkdir();
            File arch = new File(".\\datos_usuario\\mi_documento.txt");
            try {
                arch.createNewFile();
            } catch (IOException e) {
                System.out.println("Error al crear el archivo: " + e.getMessage());
            }
            System.out.println("Carpeta creada: " + creada);
        }else {
            carpeta.delete();
        }

        //renombrar
        File renombrar = new File("renombrado.txt");
        archivo.renameTo(renombrar);

        //listar todo lo que hay en un fichero

        File carpetaActual = new File(".");
        File[] loQueHay = carpetaActual.listFiles();
        System.out.println("Datos encontrados en: " + carpetaActual);
        for (File f : loQueHay) {
                System.out.println("- " + f.getName());
        }




        //Eliminar un fichero
        File archivoEliminado = new File("voyASerBorrado.txt");
        try {
            archivoEliminado.createNewFile();
        } catch (IOException e) {
            System.out.println("Error al crear el archivo: " + e.getMessage());
        }
        boolean eliminado = archivoEliminado.delete();
        if (eliminado) {
            System.out.println("Archivo eliminado con éxito.");
        } else {
            System.out.println("No se pudo eliminar el archivo.");
        }





    }
}
