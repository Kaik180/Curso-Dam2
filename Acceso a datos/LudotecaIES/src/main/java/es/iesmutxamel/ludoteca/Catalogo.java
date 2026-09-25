package es.iesmutxamel.ludoteca;

import java.util.ArrayList;
import java.util.Scanner;

public class Catalogo {
    private final ArrayList<Videojuego> Coleccion = new ArrayList<>();

    public void menu(){
        int opcion = 0;
        Scanner teclado = new Scanner(System.in);
        do {


            System.out.println("Elige una de las opciones:");
            System.out.println("1.-Añadir");
            System.out.println("2.-buscar");
            System.out.println("3.-Eliminar");
            System.out.println("4.-Salir");
            opcion = teclado.nextInt();
            switch (opcion){
                case 1:
                    añadir();
                    break;
                case 2:
                    buscar();
                    break;
                case 3:
                    eliminar();
                    break;

                default: System.out.println("Opcion no valida");
            }
        }while (opcion != 4);
    }
    static void añadir(){


    }
    static void buscar(){

    }
    static void eliminar(){

    }


}
