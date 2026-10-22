package TF7;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class TF7 {
    static void main() {
        //1-Crear el fichero JSON
        JSONObject estudiante = new JSONObject();
        estudiante.put("nombre", "Kevin ");
        estudiante.put("apellidos", "MuñozCorcoles");
        estudiante.put("edad", 21);
        JSONArray asignaturas = new JSONArray();
        asignaturas.put("Ingles");
        asignaturas.put("Proyecto Intermodular");
        estudiante.put("asignaturas", asignaturas);

        //2- leer y mostrar los datos
        System.out.println(estudiante.toString(2));
        System.out.println(estudiante.getString("nombre"));
        System.out.println(estudiante.getString("apellidos"));

        System.out.println(estudiante.getInt("edad"));

        System.out.println("Asignaturas del alumno:");
        for (int i = 0; i < asignaturas.length(); i++) {
            System.out.println(asignaturas.getString(i));
        }
        Path ruta = Path.of("estudiante.json");
        try {
            Files.writeString(ruta, estudiante.toString(2),
                    StandardCharsets.UTF_8);
            System.out.println("Fichero guardado");
        } catch (IOException e) {
            System.out.println("Error al guardar: " + e.getMessage());
        }

        //3- añadir una propiedad
        try {
            String texto=Files.readString(Path.of("estudiante.json"),StandardCharsets.UTF_8);
                    // modificamos añadiendole el curso
                    estudiante.put("curso","2º DAM");
        } catch (IOException e) {
            System.out.println("No se pudo leer el fichero");
        }
        try {
            Files.writeString(ruta, estudiante.toString(2),
                    StandardCharsets.UTF_8);
            System.out.println("Fichero guardado");
        } catch (IOException e) {
            System.out.println("Error al guardar: " + e.getMessage());
        }

        //4- Modificar el arrays de asignaturas
        try {
            String texto=Files.readString(Path.of("estudiante.json"),StandardCharsets.UTF_8);
            // modificamos añadiendole el curso
            asignaturas.put("Programacion");
        } catch (IOException e) {
            System.out.println("No se pudo leer el fichero");
        }
        try {
            Files.writeString(ruta, estudiante.toString(2),
                    StandardCharsets.UTF_8);
            System.out.println("Fichero guardado");
        } catch (IOException e) {
            System.out.println("Error al guardar: " + e.getMessage());
        }

        //5- objetos y Arrays Anidados
        JSONObject Profesor = new JSONObject();
        estudiante.put("nombre", "Silvia ");
        JSONArray alumnos = estudiante.getJSONArray("nombre");
        asignaturas.put("Kevin");
        asignaturas.put("Juan");
        estudiante.put("Alumnos", alumnos);
        JSONObject alumno = alumnos.getJSONObject(0);
        String nombre = alumno.getString("nombre");

        for (int i = 0; i < alumnos.length(); i++) {
            JSONObject juego = alumnos.getJSONObject(i);
            System.out.println(juego.getString("nombre"));
            System.out.println(juego.getString("calificacion"));
        }


    }
}
