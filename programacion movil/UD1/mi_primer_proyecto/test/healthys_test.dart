import 'package:mi_primer_proyecto/data/repositories/carta_repository.dart';
import 'package:mi_primer_proyecto/domain/entities/entrant.dart';
import 'package:mi_primer_proyecto/domain/entities/principal.dart';
import 'package:mi_primer_proyecto/domain/entities/beguda.dart';
import 'package:mi_primer_proyecto/domain/entities/producte.dart';

void main() async {
  print('Iniciant verificació de repositori i entitats...');
  final CartaRepository repo = CartaRepository();

  // Test Entrants
  final List<Entrant> entrants = await repo.getEntrants();
  assert(entrants.isNotEmpty, 'La llista d\'entrants no hauria d\'estar buida');
  assert(entrants.first.getClass() == TipusProducte.entrant);
  print('✔ Entrants verificats: ${entrants.length} plats.');

  // Test Principals
  final List<Principal> principals = await repo.getPrincipals();
  assert(principals.isNotEmpty, 'La llista de principals no hauria d\'estar buida');
  assert(principals.first.getClass() == TipusProducte.principal);
  print('✔ Plats principals verificats: ${principals.length} plats.');

  // Test Begudes
  final List<Beguda> begudes = await repo.getBegudes();
  assert(begudes.isNotEmpty, 'La llista de begudes no hauria d\'estar buida');
  assert(begudes.first.getClass() == TipusProducte.beguda);
  print('✔ Begudes verificades: ${begudes.length} begudes.');

  // Test Subtipus
  final List<String> subEntrants = await repo.getSubtipusEntrants();
  print('✔ Subtipus d\'entrants disponibles: $subEntrants');

  print('\x1B[32m✔ Totes les assercions han passat satisfactòriament!\x1B[0m');
}
