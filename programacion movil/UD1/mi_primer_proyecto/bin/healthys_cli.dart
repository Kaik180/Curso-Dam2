import 'dart:io';
import 'package:mi_primer_proyecto/data/repositories/carta_repository.dart';
import 'package:mi_primer_proyecto/domain/entities/beguda.dart';
import 'package:mi_primer_proyecto/domain/entities/entrant.dart';
import 'package:mi_primer_proyecto/domain/entities/principal.dart';

final CartaRepository repo = CartaRepository();

void main() async {
  bool eixir = false;

  print('\x1B[2J\x1B[0;0H'); // Neteja la pantalla
  print('\x1B[32m===============================================================');
  print('          RESTAURANT HEALTHYS EXPRESS - CARTA CLI');
  print('===============================================================\x1B[0m');

  while (!eixir) {
    print('\n\x1B[1m--- MENÚ PRINCIPAL ---\x1B[0m');
    print('1. Consultar Entrants (Starters)');
    print('2. Consultar Begudes (Drinks)');
    print('3. Consultar Plats Principals (Main Dishes)');
    print('4. Veure tota la carta completa');
    print('0. Eixir de l\'aplicació');
    print('---------------------------------------------------------------');
    stdout.write('Selecciona una opció [0-4]: ');

    final String? opcio = stdin.readLineSync()?.trim();

    switch (opcio) {
      case '1':
        await menuEntrants();
        break;
      case '2':
        await menuBegudes();
        break;
      case '3':
        await menuPrincipals();
        break;
      case '4':
        await mostrarTotaLaCarta();
        break;
      case '0':
        print('\n\x1B[32mGràcies per consultar la carta de Healthys Express. Bon profit!\x1B[0m');
        eixir = true;
        break;
      default:
        print('\x1B[31m[Error] Opció no vàlida. Introdueix un valor entre 0 i 4.\x1B[0m');
    }
  }
}

/// Submenú per gestionar els entrants
Future<void> menuEntrants() async {
  bool tornar = false;

  while (!tornar) {
    print('\n\x1B[35m=== MENÚ ENTRANTS ===\x1B[0m');
    print('1. Llistar tots els entrants');
    print('2. Filtrar per subtipus (amanides, tartars, rotllets, altres...)');
    print('0. Tornar al menú principal');
    stdout.write('Tria una opció [0-2]: ');

    final String? opcio = stdin.readLineSync()?.trim();

    switch (opcio) {
      case '1':
        print('\nCarregant tots els entrants des de l\'API...');
        final List<Entrant> llista = await repo.getEntrants();
        _mostrarLlista(llista, 'TOTS ELS ENTRANTS');
        break;
      case '2':
        await _filtrarEntrantsPerSubtipus();
        break;
      case '0':
        tornar = true;
        break;
      default:
        print('\x1B[31m[Error] Opció invàlida.\x1B[0m');
    }
  }
}

/// Filtre avançat de subtipus d'entrants
Future<void> _filtrarEntrantsPerSubtipus() async {
  print('Obtenint categories disponibles...');
  final List<String> subtipus = await repo.getSubtipusEntrants();

  if (subtipus.isEmpty) {
    print('\x1B[33mNo s\'han trobat subtipus d\'entrants.\x1B[0m');
    return;
  }

  print('\n\x1B[36mSubtipus d\'entrants disponibles:\x1B[0m');
  for (int i = 0; i < subtipus.length; i++) {
    print('  ${i + 1}. ${subtipus[i]}');
  }
  print('  0. Cancel·lar');
  stdout.write('Tria el número del subtipus: ');

  final String? input = stdin.readLineSync()?.trim();
  final int? index = int.tryParse(input ?? '');

  if (index == null || index < 0 || index > subtipus.length) {
    print('\x1B[31m[Error] Selecció invàlida.\x1B[0m');
    return;
  }

  if (index == 0) return;

  final String escollit = subtipus[index - 1];
  print('\nCarregant entrants del tipus "$escollit"...');
  final List<Entrant> filtrats = await repo.getEntrants(escollit);
  _mostrarLlista(filtrats, 'ENTRANTS - SUBTIPUS: ${escollit.toUpperCase()}');
}

/// Submenú per gestionar les begudes
Future<void> menuBegudes() async {
  bool tornar = false;

  while (!tornar) {
    print('\n\x1B[36m=== MENÚ BEGUDES ===\x1B[0m');
    print('1. Llistar totes les begudes');
    print('2. Filtrar per subtipus (aigües, sucs, kombuches, cerveses...)');
    print('0. Tornar al menú principal');
    stdout.write('Tria una opció [0-2]: ');

    final String? opcio = stdin.readLineSync()?.trim();

    switch (opcio) {
      case '1':
        print('\nCarregant totes les begudes des de l\'API...');
        final List<Beguda> llista = await repo.getBegudes();
        _mostrarLlista(llista, 'TOTES LES BEGUDES');
        break;
      case '2':
        await _filtrarBegudesPerSubtipus();
        break;
      case '0':
        tornar = true;
        break;
      default:
        print('\x1B[31m[Error] Opció invàlida.\x1B[0m');
    }
  }
}

/// Filtre avançat de subtipus de begudes
Future<void> _filtrarBegudesPerSubtipus() async {
  print('Obtenint categories disponibles...');
  final List<String> subtipus = await repo.getSubtipusBegudes();

  if (subtipus.isEmpty) {
    print('\x1B[33mNo s\'han trobat subtipus de begudes.\x1B[0m');
    return;
  }

  print('\n\x1B[36mSubtipus de begudes disponibles:\x1B[0m');
  for (int i = 0; i < subtipus.length; i++) {
    print('  ${i + 1}. ${subtipus[i]}');
  }
  print('  0. Cancel·lar');
  stdout.write('Tria el número del subtipus: ');

  final String? input = stdin.readLineSync()?.trim();
  final int? index = int.tryParse(input ?? '');

  if (index == null || index < 0 || index > subtipus.length) {
    print('\x1B[31m[Error] Selecció invàlida.\x1B[0m');
    return;
  }

  if (index == 0) return;

  final String escollit = subtipus[index - 1];
  print('\nCarregant begudes del tipus "$escollit"...');
  final List<Beguda> filtrats = await repo.getBegudes(escollit);
  _mostrarLlista(filtrats, 'BEGUDES - SUBTIPUS: ${escollit.toUpperCase()}');
}

/// Submenú per gestionar els plats principals
Future<void> menuPrincipals() async {
  bool tornar = false;

  while (!tornar) {
    print('\n\x1B[34m=== MENÚ PLATS PRINCIPALS ===\x1B[0m');
    print('1. Llistar tots els plats principals');
    print('2. Filtrar per subtipus (pokes, bowls, wraps, carns, peixos...)');
    print('0. Tornar al menú principal');
    stdout.write('Tria una opció [0-2]: ');

    final String? opcio = stdin.readLineSync()?.trim();

    switch (opcio) {
      case '1':
        print('\nCarregant tots els plats principals des de l\'API...');
        final List<Principal> llista = await repo.getPrincipals();
        _mostrarLlista(llista, 'TOTS ELS PLATS PRINCIPALS');
        break;
      case '2':
        await _filtrarPrincipalsPerSubtipus();
        break;
      case '0':
        tornar = true;
        break;
      default:
        print('\x1B[31m[Error] Opció invàlida.\x1B[0m');
    }
  }
}

/// Filtre avançat de subtipus de plats principals
Future<void> _filtrarPrincipalsPerSubtipus() async {
  print('Obtenint categories disponibles...');
  final List<String> subtipus = await repo.getSubtipusPrincipals();

  if (subtipus.isEmpty) {
    print('\x1B[33mNo s\'han trobat subtipus de plats principals.\x1B[0m');
    return;
  }

  print('\n\x1B[36mSubtipus de plats principals disponibles:\x1B[0m');
  for (int i = 0; i < subtipus.length; i++) {
    print('  ${i + 1}. ${subtipus[i]}');
  }
  print('  0. Cancel·lar');
  stdout.write('Tria el número del subtipus: ');

  final String? input = stdin.readLineSync()?.trim();
  final int? index = int.tryParse(input ?? '');

  if (index == null || index < 0 || index > subtipus.length) {
    print('\x1B[31m[Error] Selecció invàlida.\x1B[0m');
    return;
  }

  if (index == 0) return;

  final String escollit = subtipus[index - 1];
  print('\nCarregant plats principals del tipus "$escollit"...');
  final List<Principal> filtrats = await repo.getPrincipals(escollit);
  _mostrarLlista(filtrats, 'PLATS PRINCIPALS - SUBTIPUS: ${escollit.toUpperCase()}');
}

/// Mostra tota la carta completa simultàniament usant Future.wait
Future<void> mostrarTotaLaCarta() async {
  print('\nCarregant tota la carta en paral·lel...');
  final Stopwatch sw = Stopwatch()..start();

  final results = await Future.wait([
    repo.getEntrants(),
    repo.getPrincipals(),
    repo.getBegudes(),
  ]);
  sw.stop();

  final List<Entrant> entrants = results[0] as List<Entrant>;
  final List<Principal> principals = results[1] as List<Principal>;
  final List<Beguda> begudes = results[2] as List<Beguda>;

  print('\x1B[32m✔ Carta descarregada en ${sw.elapsedMilliseconds} ms\x1B[0m');
  _mostrarLlista(entrants, '1. SECCIÓ D\'ENTRANTS (${entrants.length} plats)');
  _mostrarLlista(principals, '2. SECCIÓ DE PLATS PRINCIPALS (${principals.length} plats)');
  _mostrarLlista(begudes, '3. SECCIÓ DE BEGUDES (${begudes.length} begudes)');
}

/// Mostra una llista d'elements utilitzant el mètode toStringSmart de cadascun
void _mostrarLlista(List<dynamic> llista, String titol) {
  print('\n\x1B[1m============================= $titol =============================\x1B[0m');
  if (llista.isEmpty) {
    print('\x1B[33mNo hi ha cap producte disponible en aquesta secció.\x1B[0m');
    return;
  }

  for (final item in llista) {
    print(item.toStringSmart());
  }
}
