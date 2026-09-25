package org.example;

import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class ProcesoPrincipal {
	public static void main(String[] args) {
		try {
			String[] infoProceso = {"java", "org.example.ProcesoSecundario"};
			Process proceso = Runtime.getRuntime().exec(infoProceso);
			BufferedReader br = new BufferedReader(new InputStreamReader(proceso.getInputStream()));
			int exitStatus = proceso.waitFor();
			String line = br.readLine();
			while (line != null) {
				if (line != null) System.out.println("Salida:\n" + line);
				line = br.readLine();
			}
			if (exitStatus==0) {
				System.out.println("El proceso se ha completado satisfactoriamente");
			} else {
				System.out.println("El proceso ha fallado. Código de error: " + exitStatus);
			}
		} catch (IOException e) {
			System.out.println("Error de entrada salida en la comunicación con el proceso");
		} catch (InterruptedException e) {
			System.out.println("Error: ejecución interrumpida");
		}
	}
}
