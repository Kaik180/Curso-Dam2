import 'dart:convert';
import 'package:http/http.dart' as http;

/// UNITAT 2.5 - ACTIVITAT 1: CONSUM DIRECTE D'API REST AMB HTTP I UTF-8
///
/// Obté i processa les llistes d'entrants, begudes i principals des de l'API de Railway:
/// https://healthys-express-backend-production.up.railway.app/

const String baseUrl = 'https://healthys-express-backend-production.up.railway.app/api';

/// Funció que obté i descodifica una col·lecció en format JSON des d'un endpoint
Future<List<dynamic>> descarregarEndpoint(String endpoint) async {
  final Uri uri = Uri.parse('$baseUrl/$endpoint');
  print('Consultant $uri ...');

  final response = await http.get(uri).timeout(const Duration(seconds: 12));

  if (response.statusCode == 200) {
    // Descodificació en UTF-8 per caràcters especials i accents
    final String body = utf8.decode(response.bodyBytes);
    return jsonDecode(body) as List<dynamic>;
  } else {
    throw Exception('Error del servidor: Codi ${response.statusCode}');
  }
}

void main() async {
  print('================================================================');
  print('   UD 2.5 - ACT 1: DESCARREGA I PROCESSAT D\'API REST (HTTP)');
  print('================================================================\n');

  try {
    // 1. Obtenir Entrants
    final List<dynamic> entrants = await descarregarEndpoint('entrants');
    print('\x1B[32m✔ Entrants descarregats: ${entrants.length} plats.\x1B[0m');
    print('  Primer entrant rebut: ${entrants.first['name']} (${entrants.first['price']} €)');

    // 2. Obtenir Plats Principals
    final List<dynamic> principals = await descarregarEndpoint('principals');
    print('\x1B[32m✔ Principals descarregats: ${principals.length} plats.\x1B[0m');
    print('  Primer plat principal: ${principals.first['name']} (${principals.first['price']} €)');

    // 3. Obtenir Begudes
    final List<dynamic> begudes = await descarregarEndpoint('begudes');
    print('\x1B[32m✔ Begudes descarregades: ${begudes.length} begudes.\x1B[0m');
    print('  Primera beguda: ${begudes.first['name']} (${begudes.first['price']} €)\n');

    // 4. Processament funcional de prova
    final preuMigEntrants = entrants
            .map((e) => (e['price'] as num).toDouble())
            .reduce((a, b) => a + b) /
        entrants.length;
    print('Preu mitjà dels entrants de l\'API: \x1B[36m${preuMigEntrants.toStringAsFixed(2)} €\x1B[0m');

    print('\n\x1B[32m✔ Activitat 1 de la Unitat 2.5 completada amb èxit!\x1B[0m');
  } catch (e) {
    print('\x1B[31m[Error en la petició HTTP] $e\x1B[0m');
  }
}
