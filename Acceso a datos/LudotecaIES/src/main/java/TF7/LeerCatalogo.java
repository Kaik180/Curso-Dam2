package TF7;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class LeerCatalogo {
    static void main() {
        try {
            String texto = Files.readString(Path.of("catalogo.json"));
            JSONObject catalogo = new JSONObject(texto);
            JSONArray videojuegos = catalogo.getJSONArray("videojuegos");
            System.out.println(catalogo.getString("nombre"));
            for (int i = 0; i < videojuegos.length(); i++) {
                JSONObject juego = videojuegos.getJSONObject(i);
                System.out.println(juego.getInt("id") + " - "
                        + juego.getString("titulo") + " ("
                        + juego.getString("plataforma") + ")");
            }
        } catch (IOException e) {
            System.out.println("Error al leer el fichero: " + e.getMessage());
        } catch (JSONException e) {
            System.out.println("Error en el JSON: " + e.getMessage());
        }
    }
}
