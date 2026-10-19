import 'dart:convert';
import 'package:http/http.dart' as http;

/// Servei encarregat de comunicar-se directament amb l'API REST de Healthys Express
class HealthysApi {
  static const String baseUrl =
      'https://healthys-express-backend-production.up.railway.app/api';

  /// Obté la llista crua de JSON dels entrants (opcionalment filtrada per subtipus)
  Future<List<Map<String, dynamic>>> getEntrantsRaw([String? tipus]) async {
    final String url = (tipus != null && tipus.trim().isNotEmpty)
        ? '$baseUrl/entrants/${Uri.encodeComponent(tipus.trim())}'
        : '$baseUrl/entrants';

    return await _fetchList(url);
  }

  /// Obté la llista crua de JSON dels plats principals (opcionalment filtrada per subtipus)
  Future<List<Map<String, dynamic>>> getPrincipalsRaw([String? tipus]) async {
    final String url = (tipus != null && tipus.trim().isNotEmpty)
        ? '$baseUrl/principals/${Uri.encodeComponent(tipus.trim())}'
        : '$baseUrl/principals';

    return await _fetchList(url);
  }

  /// Obté la llista crua de JSON de les begudes (opcionalment filtrada per subtipus)
  Future<List<Map<String, dynamic>>> getBegudesRaw([String? tipus]) async {
    final String url = (tipus != null && tipus.trim().isNotEmpty)
        ? '$baseUrl/begudes/${Uri.encodeComponent(tipus.trim())}'
        : '$baseUrl/begudes';

    return await _fetchList(url);
  }

  /// Mètode auxiliar genèric per realitzar la petició HTTP GET amb descodificació UTF-8
  Future<List<Map<String, dynamic>>> _fetchList(String url) async {
    try {
      final response = await http
          .get(Uri.parse(url))
          .timeout(const Duration(seconds: 12));

      if (response.statusCode == 200) {
        // Descodificació en UTF-8 per tractar accents i caràcters especials
        final String bodyString = utf8.decode(response.bodyBytes);
        final dynamic decoded = jsonDecode(bodyString);

        if (decoded is List) {
          return decoded.cast<Map<String, dynamic>>();
        } else {
          throw Exception('La resposta rebuda no és una llista JSON.');
        }
      } else {
        throw Exception(
            'Error del servidor: Codi d\'estat ${response.statusCode}');
      }
    } catch (e) {
      print('\x1B[33m[Avís Xarxa] Error en connectar amb $url: $e\x1B[0m');
      print('\x1B[33m[Avís Xarxa] S\'activarà el mode de seguretat / dades de reserva.\x1B[0m');
      return _getFallbackData(url);
    }
  }

  /// Dades de reserva (fallback) per si el servidor Railway està dormit o no hi ha internet
  List<Map<String, dynamic>> _getFallbackData(String url) {
    if (url.contains('/entrants')) {
      return [
        {
          'id': 'ENT01',
          'name': 'Amanida mediterrània (Offline)',
          'description': 'Enciam, tomàquet, cogombre, olives, formatge feta i vinagreta.',
          'tipus': 'amanides',
          'allergens': ['Llet'],
          'price': 9.0,
          'calories': 220,
          'dietType': ['Sense gluten', 'Vegetarià'],
          'additionalInfo': 'Fresca i lleugera.',
          'img': 'img/amanida_mediterrania.png'
        },
        {
          'id': 'ENT04',
          'name': 'Tartar de tonyina (Offline)',
          'description': 'Tartar fresc de tonyina amb alvocat, llavors de sèsam i salsa de soja.',
          'tipus': 'tartars',
          'allergens': ['Peix', 'Sèsam'],
          'price': 7.5,
          'calories': 200,
          'dietType': ['Sense gluten', 'Baixa en carbohidrats'],
          'additionalInfo': 'Rica en omega 3.',
          'img': 'img/tartar_tonyina.png'
        }
      ];
    } else if (url.contains('/principals')) {
      return [
        {
          'id': 'PRI01',
          'name': 'Poke de tonyina (Offline)',
          'description': 'Poke de tonyina fresca amb alvocat, ceba, alga nori, i salsa de soja.',
          'tipus': 'pokes',
          'allergens': ['Peix', 'Sèsam'],
          'price': 12.0,
          'calories': 350,
          'dietType': ['Sense gluten', 'Alta en proteïnes'],
          'additionalInfo': 'Ric en omega 3 i saludable.',
          'img': 'img/poke_tonyina.png'
        }
      ];
    } else {
      return [
        {
          'id': 'BEG01',
          'name': 'Kombucha de gingebre (Offline)',
          'description': 'Kombucha refrescant amb gingebre natural i un toc de llimona.',
          'tipus': 'kombuches',
          'allergens': [],
          'price': 3.5,
          'calories': 60,
          'isAlcoholic': false,
          'additionalInfo': 'Ideal per a la digestió.',
          'img': 'img/kombucha_gingebre.png'
        }
      ];
    }
  }
}
