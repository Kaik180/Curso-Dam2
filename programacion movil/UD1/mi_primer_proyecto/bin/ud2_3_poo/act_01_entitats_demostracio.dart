import 'package:mi_primer_proyecto/domain/entities/producte.dart';
import 'package:mi_primer_proyecto/domain/entities/entrant.dart';
import 'package:mi_primer_proyecto/domain/entities/principal.dart';
import 'package:mi_primer_proyecto/domain/entities/beguda.dart';

/// UNITAT 2.3 - PROGRAMACIÓ ORIENTADA A OBJECTES (DEMOSTRACIÓ D'ENTITATS)
///
/// En aquest exercici es posen a prova les entitats del domini desenvolupades a lib/domain/entities/:
/// 1. Classe abstracta Producte
/// 2. Subclasses: Entrant, Principal, Beguda
/// 3. Constructors amb paràmetres amb nom
/// 4. Constructors factoria .fromJSON()
/// 5. Mètodes getClass() i toStringSmart() amb colors ANSI

void main() {
  print('================================================================');
  print('   UD 2.3 - POO: PROVA I DEMOSTRACIÓ DE LES ENTITATS');
  print('================================================================\n');

  // 1. Creació manual d'un Entrant mitjançant el constructor amb paràmetres amb nom
  final Entrant entrantManual = Entrant(
    id: 'ENT-DEMO',
    name: 'Amanida Gourmet de la Casa',
    description: 'Mesclum d\'enciams, nous, formatge de cabra caramel·litzat i vinagreta de módena.',
    tipus: 'amanides',
    allergens: ['Llet', 'Fruits secs'],
    price: 8.50,
    calories: 210,
    additionalInfo: 'Recomanació del xef per a començar.',
    img: 'img/amanida_gourmet.png',
    dietType: ['Vegetarià', 'Sense gluten'],
  );

  // 2. Creació d'un Plat Principal mitjançant el constructor factoria .fromJSON()
  final Map<String, dynamic> jsonPrincipal = {
    'id': 'PRI-JSON',
    'name': 'Poke Bowl de Salmó i Alvocat',
    'description': 'Base d\'arròs de sushi, salmó fresc marinat, alvocat, edamame i salsa ponzu.',
    'tipus': 'pokes',
    'allergens': ['Peix', 'Soja', 'Sèsam'],
    'price': 13.95,
    'calories': 420,
    'additionalInfo': 'Opció proteica molt saludable.',
    'img': 'img/poke_salmo.png',
    'dietType': ['Sense gluten', 'Alt en proteïnes'],
  };
  final Principal principalJson = Principal.fromJSON(jsonPrincipal);

  // 3. Creació d'una Beguda mitjançant constructor factoria .fromJSON()
  final Map<String, dynamic> jsonBeguda = {
    'id': 'BEG-JSON',
    'name': 'Kombucha Artesana de Fruits Vermells',
    'description': 'Beguda fermentada ecològica rica en probiòtics.',
    'tipus': 'kombuches',
    'allergens': [],
    'price': 3.75,
    'calories': 45,
    'additionalInfo': '100% natural, sense sucres afegits.',
    'img': 'img/kombucha_fruits.png',
    'isAlcoholic': false,
  };
  final Beguda begudaJson = Beguda.fromJSON(jsonBeguda);

  // 4. Llista polimòrfica de Producte
  final List<Producte> cartaDemo = [entrantManual, principalJson, begudaJson];

  print('Imprimint les entitats mitjançant el mètode visual toStringSmart():\n');
  for (final producte in cartaDemo) {
    print('Tipus d\'objecte detectat via getClass(): \x1B[1m${producte.getClass()}\x1B[0m');
    print(producte.toStringSmart());
    print('');
  }

  print('\x1B[32m✔ Totes les entitats de domini funcionen i renderitzen perfectament!\x1B[0m');
}
