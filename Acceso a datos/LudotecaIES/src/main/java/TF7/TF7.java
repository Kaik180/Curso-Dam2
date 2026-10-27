package TF7;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public class TF7 {
    public static void main(String[] args) {
        // =========================================================================
        // PARTE 1. Crear el fichero JSON
        // =========================================================================
        System.out.println("=== PARTE 1: Crear el fichero JSON (estudiante.json) ===");
        JSONObject estudiante = new JSONObject();
        estudiante.put("nombre", "Kevin");
        estudiante.put("apellidos", "Muñoz Corcoles");
        estudiante.put("edad", 21);

        JSONArray asignaturas = new JSONArray();
        asignaturas.put("Inglés");
        asignaturas.put("Proyecto Intermodular");
        estudiante.put("asignaturas", asignaturas);

        Path rutaEstudiante = Path.of("estudiante.json");
        try {
            Files.writeString(rutaEstudiante, estudiante.toString(2), StandardCharsets.UTF_8);
            System.out.println("Fichero estudiante.json creado correctamente:");
            System.out.println(estudiante.toString(2));
        } catch (IOException e) {
            System.out.println("Error al guardar estudiante.json: " + e.getMessage());
        }

        // =========================================================================
        // PARTE 2. Leer y mostrar los datos
        // =========================================================================
        System.out.println("\n=== PARTE 2: Leer y mostrar los datos de estudiante.json ===");
        try {
            String contenidoEstudiante = Files.readString(rutaEstudiante, StandardCharsets.UTF_8);
            JSONObject estudianteLeido = new JSONObject(contenidoEstudiante);

            String nombreCompleto = estudianteLeido.getString("nombre") + " " + estudianteLeido.getString("apellidos");
            int edad = estudianteLeido.getInt("edad");
            System.out.println("Nombre completo: " + nombreCompleto);
            System.out.println("Edad: " + edad);

            System.out.println("Asignaturas:");
            JSONArray asignaturasLeidas = estudianteLeido.getJSONArray("asignaturas");
            for (int i = 0; i < asignaturasLeidas.length(); i++) {
                System.out.println(" - " + asignaturasLeidas.getString(i));
            }
        } catch (IOException e) {
            System.out.println("Error al leer estudiante.json: " + e.getMessage());
        }

        // =========================================================================
        // PARTE 3. Añadir una propiedad ("curso" con el valor "2º DAM")
        // =========================================================================
        System.out.println("\n=== PARTE 3: Añadir propiedad 'curso' ===");
        try {
            String contenidoEstudiante = Files.readString(rutaEstudiante, StandardCharsets.UTF_8);
            JSONObject estudianteModificado = new JSONObject(contenidoEstudiante);

            estudianteModificado.put("curso", "2º DAM");

            Files.writeString(rutaEstudiante, estudianteModificado.toString(2), StandardCharsets.UTF_8);
            System.out.println("Propiedad 'curso' añadida y fichero actualizado:");
            System.out.println(estudianteModificado.toString(2));
        } catch (IOException e) {
            System.out.println("Error en Parte 3: " + e.getMessage());
        }

        // =========================================================================
        // PARTE 4. Modificar el array de asignaturas (añadir "Programación")
        // =========================================================================
        System.out.println("\n=== PARTE 4: Modificar el array de asignaturas ===");
        try {
            String contenidoEstudiante = Files.readString(rutaEstudiante, StandardCharsets.UTF_8);
            JSONObject estudianteActualizado = new JSONObject(contenidoEstudiante);

            JSONArray arrayAsignaturas = estudianteActualizado.getJSONArray("asignaturas");
            boolean yaExiste = false;
            for (int i = 0; i < arrayAsignaturas.length(); i++) {
                if ("Programación".equalsIgnoreCase(arrayAsignaturas.getString(i))) {
                    yaExiste = true;
                    break;
                }
            }
            if (!yaExiste) {
                arrayAsignaturas.put("Programación");
            }

            Files.writeString(rutaEstudiante, estudianteActualizado.toString(2), StandardCharsets.UTF_8);
            System.out.println("Fichero estudiante.json actualizado con la nueva asignatura.");

            // Comprobación volviendo a leer desde Java
            String contenidoVerificado = Files.readString(rutaEstudiante, StandardCharsets.UTF_8);
            JSONObject verificado = new JSONObject(contenidoVerificado);
            System.out.println("Comprobación de lectura:");
            System.out.println("Asignaturas en disco: " + verificado.getJSONArray("asignaturas").toString());
        } catch (IOException e) {
            System.out.println("Error en Parte 4: " + e.getMessage());
        }

        // =========================================================================
        // PARTE 5. Objetos y arrays anidados (profesor.json)
        // =========================================================================
        System.out.println("\n=== PARTE 5: Objetos y arrays anidados (profesor.json) ===");
        JSONObject profesorObj = new JSONObject();
        profesorObj.put("nombre", "Silvia");
        profesorObj.put("departamento", "Informática");

        JSONArray listaEstudiantes = new JSONArray();

        JSONObject est1 = new JSONObject();
        est1.put("nombre", "Kevin");
        est1.put("calificacion", 9.5);
        listaEstudiantes.put(est1);

        JSONObject est2 = new JSONObject();
        est2.put("nombre", "Juan");
        est2.put("calificacion", 8.0);
        listaEstudiantes.put(est2);

        profesorObj.put("estudiantes", listaEstudiantes);

        Path rutaProfesor = Path.of("profesor.json");
        try {
            Files.writeString(rutaProfesor, profesorObj.toString(2), StandardCharsets.UTF_8);
            System.out.println("Fichero profesor.json guardado correctamente:");
            System.out.println(profesorObj.toString(2));
        } catch (IOException e) {
            System.out.println("Error al guardar profesor.json: " + e.getMessage());
        }

        // Lectura de profesor.json mostrando nombre y calificación de cada estudiante
        try {
            String textoProfesor = Files.readString(rutaProfesor, StandardCharsets.UTF_8);
            JSONObject profesorLeido = new JSONObject(textoProfesor);
            System.out.println("\nLectura de profesor.json:");
            System.out.println("Profesor: " + profesorLeido.getString("nombre") + " (Dpto: " + profesorLeido.getString("departamento") + ")");

            JSONArray alumnosArray = profesorLeido.getJSONArray("estudiantes");
            System.out.println("Estudiantes y calificaciones:");
            for (int i = 0; i < alumnosArray.length(); i++) {
                JSONObject alumno = alumnosArray.getJSONObject(i);
                System.out.println(" - Alumno: " + alumno.getString("nombre") + " | Calificación: " + alumno.get("calificacion"));
            }
        } catch (IOException e) {
            System.out.println("Error al leer profesor.json: " + e.getMessage());
        }

        // =========================================================================
        // PARTE 6. Del JSON a las clases Java
        // =========================================================================
        System.out.println("\n=== PARTE 6: Del JSON a las clases Java ===");
        Path rutaInstituto = Path.of("instituto.json");
        try {
            if (!Files.exists(rutaInstituto)) {
                // Si no existe, creamos el JSON indicado en el enunciado
                String jsonInicial = """
                {
                  "equipo": "2º DAM",
                  "instituto": "IES Mutxamel",
                  "profesores": [
                    {
                      "nombre": "Pepito Grillo",
                      "cursos": [1, 2],
                      "modulos": ["Acceso a Datos", "Proyecto Intermodular"]
                    },
                    {
                      "nombre": "Pinocho",
                      "cursos": [2],
                      "modulos": ["Desarrollo de Interfaces"]
                    }
                  ]
                }
                """;
                Files.writeString(rutaInstituto, jsonInicial, StandardCharsets.UTF_8);
            }

            // Lectura del JSON y construcción manual de los objetos con org.json
            String textoInstituto = Files.readString(rutaInstituto, StandardCharsets.UTF_8);
            JSONObject rootInstituto = new JSONObject(textoInstituto);

            String equipo = rootInstituto.getString("equipo");
            String instituto = rootInstituto.getString("instituto");
            JSONArray profesoresJson = rootInstituto.getJSONArray("profesores");

            List<Profesor> listaProfesores = new ArrayList<>();
            for (int i = 0; i < profesoresJson.length(); i++) {
                JSONObject profJson = profesoresJson.getJSONObject(i);
                String nombreProf = profJson.getString("nombre");

                JSONArray cursosJson = profJson.getJSONArray("cursos");
                List<Integer> cursosList = new ArrayList<>();
                for (int c = 0; c < cursosJson.length(); c++) {
                    cursosList.add(cursosJson.getInt(c));
                }

                JSONArray modulosJson = profJson.getJSONArray("modulos");
                List<String> modulosList = new ArrayList<>();
                for (int m = 0; m < modulosJson.length(); m++) {
                    modulosList.add(modulosJson.getString(m));
                }

                Profesor profesor = new Profesor(nombreProf, cursosList, modulosList);
                listaProfesores.add(profesor);
            }

            EquipoDocente equipoDocente = new EquipoDocente(equipo, instituto, listaProfesores);

            System.out.println("Objetos Java construidos a partir del JSON:");
            System.out.println("Equipo docente: " + equipoDocente.getEquipo());
            System.out.println("Instituto: " + equipoDocente.getInstituto());
            System.out.println("Profesores cargados:");
            for (Profesor prof : equipoDocente.getProfesores()) {
                System.out.println(" - Nombre: " + prof.getNombre());
                System.out.println("   Cursos: " + prof.getCursos());
                System.out.println("   Módulos: " + prof.getModulos());
            }
            System.out.println("ToString completo: " + equipoDocente);

        } catch (IOException e) {
            System.out.println("Error en Parte 6: " + e.getMessage());
        }

        // =========================================================================
        // PARTE 7. Construir una estructura JSON más compleja
        // =========================================================================
        System.out.println("\n=== PARTE 7: Construir estructura JSON compleja ===");
        JSONObject examJson = new JSONObject();
        examJson.put("word", "exam");

        JSONArray resultsArray = new JSONArray();

        JSONObject resultItem = new JSONObject();
        resultItem.put("definition", "a test of knowledge or skill");
        resultItem.put("partOfSpeech", "noun");

        JSONArray synonymsArray = new JSONArray();
        synonymsArray.put("examination");
        synonymsArray.put("test");
        resultItem.put("synonyms", synonymsArray);

        resultsArray.put(resultItem);
        examJson.put("results", resultsArray);

        JSONObject syllablesObj = new JSONObject();
        syllablesObj.put("count", 2);

        JSONArray syllablesList = new JSONArray();
        syllablesList.put("ex");
        syllablesList.put("am");
        syllablesObj.put("list", syllablesList);

        examJson.put("syllables", syllablesObj);

        Path rutaExam = Path.of("exam.json");
        try {
            Files.writeString(rutaExam, examJson.toString(2), StandardCharsets.UTF_8);
            System.out.println("Fichero exam.json creado con éxito:");
            System.out.println(examJson.toString(2));
        } catch (IOException e) {
            System.out.println("Error al guardar exam.json: " + e.getMessage());
        }
    }
}
