package TF7;
import org.json.JSONArray;

public class CrearRecorrerJsonArrays {
    static void main() {
        JSONArray nombres = new JSONArray();
        nombres.put("Pepito Grillo");
        nombres.put("Pinocho");
        nombres.put("Gepetto");
        for (int i = 0; i < nombres.length(); i++) {
            System.out.println(nombres.getString(i));
        }

    }
}
