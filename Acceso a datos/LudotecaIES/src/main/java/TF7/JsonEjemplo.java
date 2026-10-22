package TF7;
import org.json.JSONObject;

public class JsonEjemplo {
    static void main() {
        //1- Creamos un objeto Json y lo añadimos las propiedades indicando la clave - valor
        JSONObject persona = new JSONObject();
        persona.put("nombre", "Pepito");
        persona.put("apellidos", "Grillo");
        persona.put("edad", 25);
        persona.put("activo", true);
        //el toString(2) indica que la sangria delos datos tenga 2 espacios
        System.out.println(persona.toString(2));
        System.out.println(persona.getString("nombre"));
        System.out.println(persona.getInt("edad"));
        System.out.println(persona.getBoolean("activo"));

    }
}
