import 'dart:io';

/// UNITAT 2.2 - ACTIVITAT 1: GESTIÓ D'AULES I ALUMNES (MAP I SET)
///
/// - Map<String, List<String>> per gestionar aula -> llista d'alumnes
/// - Menú complet amb altes, baixes, consultes
/// - Ús de Set per obtenir la llista d'alumnes únics de tot l'institut

Map<String, List<String>> aules = {
  'INFO01': ['Marc Garcia', 'Anna Soler', 'Joan Puig'],
  'INFO02': ['Laura Marti', 'Marc Garcia', 'Carles Vidal'],
  'DAM01': ['Elena Gomez', 'David Navarro', 'Anna Soler'],
};

void main() {
  bool eixir = false;

  while (!eixir) {
    print('\n======================================================');
    print('   UD 2.2 - ACT 1: GESTIÓ D\'AULES I ALUMNES (MAP & SET)');
    print('======================================================');
    print('1. Afegir una nova aula');
    print('2. Afegir un alumne a una aula existent');
    print('3. Veure totes les aules amb els seus alumnes');
    print('4. Veure tots els alumnes d\'una aula concreta');
    print('5. Eliminar un alumne d\'una aula concreta');
    print('6. Eliminar una aula i tots els seus alumnes');
    print('7. Mostrar tots els alumnes de l\'institut (sense duplicats, via Set)');
    print('0. Tornar / Eixir');
    print('------------------------------------------------------');
    stdout.write('Tria una opció [0-7]: ');

    final String? opcio = stdin.readLineSync()?.trim();

    switch (opcio) {
      case '1':
        afegirAula();
        break;
      case '2':
        afegirAlumneAAula();
        break;
      case '3':
        veureTotesAules();
        break;
      case '4':
        veureAlumnesAula();
        break;
      case '5':
        eliminarAlumneAula();
        break;
      case '6':
        eliminarAula();
        break;
      case '7':
        mostrarTotsAlumnesInstitut();
        break;
      case '0':
        print('\n\x1B[32mSortint de la gestió d\'aules... Adéu!\x1B[0m');
        eixir = true;
        break;
      default:
        print('\x1B[31m[Error] Opció no vàlida (0-7).\x1B[0m');
    }
  }
}

void afegirAula() {
  stdout.write('\nIntrodueix el codi de la nova aula (ex: INFO03): ');
  final String? nomAula = stdin.readLineSync()?.trim().toUpperCase();

  if (nomAula == null || nomAula.isEmpty) {
    print('\x1B[31m[Error] El nom de l\'aula no pot estar buit.\x1B[0m');
    return;
  }

  if (aules.containsKey(nomAula)) {
    print('\x1B[33m[Avís] L\'aula "$nomAula" ja existeix.\x1B[0m');
  } else {
    aules[nomAula] = <String>[];
    print('\x1B[32m✔ Aula "$nomAula" creada amb èxit.\x1B[0m');
  }
}

void afegirAlumneAAula() {
  if (aules.isEmpty) {
    print('\x1B[33m[Avís] No hi ha cap aula registrada encara.\x1B[0m');
    return;
  }

  stdout.write('\nIntrodueix el nom de l\'aula a la qual vols afegir alumnes: ');
  final String? nomAula = stdin.readLineSync()?.trim().toUpperCase();

  if (nomAula == null || !aules.containsKey(nomAula)) {
    print('\x1B[31m[Error] L\'aula "$nomAula" no existeix. Aules: ${aules.keys.join(', ')}\x1B[0m');
    return;
  }

  bool afegirMes = true;
  while (afegirMes) {
    stdout.write('Introdueix el nom de l\'alumne: ');
    final String? alumne = stdin.readLineSync()?.trim();

    if (alumne != null && alumne.isNotEmpty) {
      aules[nomAula]!.add(alumne);
      print('\x1B[32m✔ Alumne "$alumne" afegit correctament a $nomAula.\x1B[0m');
    } else {
      print('\x1B[31m[Error] El nom no pot estar buit.\x1B[0m');
    }

    stdout.write('Vols afegir un altre alumne a $nomAula? (s/n): ');
    final String? resposta = stdin.readLineSync()?.trim().toLowerCase();
    if (resposta != 's' && resposta != 'si' && resposta != 'sí') {
      afegirMes = false;
    }
  }
}

void veureTotesAules() {
  print('\n--- LLISTAT DE TOTES LES AULES I ALUMNES ---');
  if (aules.isEmpty) {
    print('\x1B[33mNo hi ha cap aula registrada.\x1B[0m');
    return;
  }

  aules.forEach((aula, alumnes) {
    print('\x1B[36m➤ Aula: $aula (${alumnes.length} alumnes)\x1B[0m');
    if (alumnes.isEmpty) {
      print('   (Sense alumnes matriculats)');
    } else {
      for (int i = 0; i < alumnes.length; i++) {
        print('   ${i + 1}. ${alumnes[i]}');
      }
    }
  });
}

void veureAlumnesAula() {
  stdout.write('\nIntrodueix el codi de l\'aula que vols consultar: ');
  final String? nomAula = stdin.readLineSync()?.trim().toUpperCase();

  if (nomAula == null || !aules.containsKey(nomAula)) {
    print('\x1B[31m[Error] L\'aula "$nomAula" no s\'ha trobat.\x1B[0m');
    return;
  }

  final List<String> alumnes = aules[nomAula]!;
  print('\n\x1B[36mAlumnes de l\'aula $nomAula (Total: ${alumnes.length}):\x1B[0m');
  if (alumnes.isEmpty) {
    print('  (Aula buida, sense alumnes)');
  } else {
    for (int i = 0; i < alumnes.length; i++) {
      print('  ${i + 1}. ${alumnes[i]}');
    }
  }
}

void eliminarAlumneAula() {
  stdout.write('\nIntrodueix el codi de l\'aula: ');
  final String? nomAula = stdin.readLineSync()?.trim().toUpperCase();

  if (nomAula == null || !aules.containsKey(nomAula)) {
    print('\x1B[31m[Error] L\'aula "$nomAula" no existeix.\x1B[0m');
    return;
  }

  final List<String> alumnes = aules[nomAula]!;
  if (alumnes.isEmpty) {
    print('\x1B[33m[Avís] L\'aula $nomAula no té alumnes per eliminar.\x1B[0m');
    return;
  }

  stdout.write('Introdueix el nom exacte de l\'alumne a eliminar: ');
  final String? alumneAEliminar = stdin.readLineSync()?.trim();

  if (alumneAEliminar != null && alumnes.contains(alumneAEliminar)) {
    alumnes.remove(alumneAEliminar);
    print('\x1B[32m✔ Alumne "$alumneAEliminar" eliminat de $nomAula.\x1B[0m');
  } else {
    print('\x1B[31m[Error] No s\'ha trobat l\'alumne "$alumneAEliminar".\x1B[0m');
  }
}

void eliminarAula() {
  stdout.write('\nIntrodueix el codi de l\'aula que vols suprimir: ');
  final String? nomAula = stdin.readLineSync()?.trim().toUpperCase();

  if (nomAula == null || !aules.containsKey(nomAula)) {
    print('\x1B[31m[Error] L\'aula "$nomAula" no existeix.\x1B[0m');
    return;
  }

  stdout.write('Segur que vols eliminar l\'aula $nomAula? (s/n): ');
  final String? confirm = stdin.readLineSync()?.trim().toLowerCase();
  if (confirm == 's' || confirm == 'si' || confirm == 'sí') {
    aules.remove(nomAula);
    print('\x1B[32m✔ Aula $nomAula eliminada correctament.\x1B[0m');
  }
}

void mostrarTotsAlumnesInstitut() {
  print('\n--- TOTS ELS ALUMNES DE L\'INSTITUT (SET SENSE DUPLICATS) ---');
  final Set<String> totsElsAlumnes = <String>{};

  for (final List<String> llistaAula in aules.values) {
    totsElsAlumnes.addAll(llistaAula);
  }

  if (totsElsAlumnes.isEmpty) {
    print('\x1B[33mNo hi ha cap alumne registrat a tot l\'institut.\x1B[0m');
    return;
  }

  final List<String> ordenats = totsElsAlumnes.toList()..sort();
  print('\x1B[32mTotal alumnes únics matriculats: ${ordenats.length}\x1B[0m');
  for (int i = 0; i < ordenats.length; i++) {
    final List<String> aulesMatriculat = aules.entries
        .where((entry) => entry.value.contains(ordenats[i]))
        .map((entry) => entry.key)
        .toList();

    print('${i + 1}. ${ordenats[i]} -> [Aules: ${aulesMatriculat.join(', ')}]');
  }
}
