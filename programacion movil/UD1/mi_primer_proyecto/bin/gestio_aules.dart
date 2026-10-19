import 'dart:io';

/// Mapa principal: La clau és el codi de l'aula (ex: "INFO01"),
/// i el valor és la llista de noms dels alumnes d'aquella aula.
Map<String, List<String>> aules = {
  'INFO01': ['Marc Garcia', 'Anna Soler', 'Joan Puig'],
  'INFO02': ['Laura Marti', 'Marc Garcia', 'Carles Vidal'],
  'DAM01': ['Elena Gomez', 'David Navarro', 'Anna Soler'],
};

void main() {
  bool eixir = false;

  while (!eixir) {
    print('\n======================================================');
    print('      SISTEMA DE GESTIÓ D\'AULES I ALUMNES (UD2)');
    print('======================================================');
    print('1. Afegir una nova aula');
    print('2. Afegir un alumne a una aula existent');
    print('3. Veure totes les aules amb els seus alumnes');
    print('4. Veure tots els alumnes d\'una aula concreta');
    print('5. Eliminar un alumne d\'una aula concreta');
    print('6. Eliminar una aula i tots els seus alumnes');
    print('7. Mostrar tots els alumnes de l\'institut (sense duplicats, via Set)');
    print('0. Eixir');
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
        print('\x1B[31m[Error] Opció no vàlida. Introdueix un número entre 0 i 7.\x1B[0m');
    }
  }
}

/// 1. Afegir una nova aula
void afegirAula() {
  stdout.write('\nIntrodueix el codi de la nova aula (ex: INFO03): ');
  final String? nomAula = stdin.readLineSync()?.trim().toUpperCase();

  if (nomAula == null || nomAula.isEmpty) {
    print('\x1B[31m[Error] El nom de l\'aula no pot estar buit.\x1B[0m');
    return;
  }

  if (aules.containsKey(nomAula)) {
    print('\x1B[33m[Avís] L\'aula "$nomAula" ja existeix actualment.\x1B[0m');
  } else {
    aules[nomAula] = <String>[];
    print('\x1B[32m✔ Aula "$nomAula" creada amb èxit.\x1B[0m');
  }
}

/// 2. Afegir un alumne a una aula existent amb bucle per afegir-ne més
void afegirAlumneAAula() {
  if (aules.isEmpty) {
    print('\x1B[33m[Avís] No hi ha cap aula registrada encara.\x1B[0m');
    return;
  }

  stdout.write('\nIntrodueix el nom de l\'aula a la qual vols afegir alumnes: ');
  final String? nomAula = stdin.readLineSync()?.trim().toUpperCase();

  if (nomAula == null || !aules.containsKey(nomAula)) {
    print('\x1B[31m[Error] L\'aula "$nomAula" no existeix. Aules disponibles: ${aules.keys.join(', ')}\x1B[0m');
    return;
  }

  bool afegirMes = true;
  while (afegirMes) {
    stdout.write('Introdueix el nom de l\'alumne: ');
    final String? alumne = stdin.readLineSync()?.trim();

    if (alumne != null && alumne.isNotEmpty) {
      aules[nomAula]!.add(alumne);
      print('\x1B[32m✔ Alumne "$alumne" afegit correctament a l\'aula $nomAula.\x1B[0m');
    } else {
      print('\x1B[31m[Error] El nom de l\'alumne no pot estar buit.\x1B[0m');
    }

    stdout.write('Vols afegir un altre alumne a l\'aula $nomAula? (s/n): ');
    final String? resposta = stdin.readLineSync()?.trim().toLowerCase();
    if (resposta != 's' && resposta != 'si' && resposta != 'sí') {
      afegirMes = false;
    }
  }
}

/// 3. Veure totes les aules amb els seus alumnes
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

/// 4. Veure tots els alumnes d'una aula concreta
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
    alumnes.asMap().forEach((idx, alumne) {
      print('  ${idx + 1}. $alumne');
    });
  }
}

/// 5. Eliminar un alumne d'una aula concreta
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

  stdout.write('Introdueix el nom exacte de l\'alumne a donar de baixa: ');
  final String? alumneAEliminar = stdin.readLineSync()?.trim();

  if (alumneAEliminar != null && alumnes.contains(alumneAEliminar)) {
    alumnes.remove(alumneAEliminar);
    print('\x1B[32m✔ Alumne "$alumneAEliminar" eliminat de l\'aula $nomAula amb èxit.\x1B[0m');
  } else {
    print('\x1B[31m[Error] No s\'ha trobat l\'alumne "$alumneAEliminar" a l\'aula $nomAula.\x1B[0m');
  }
}

/// 6. Eliminar una aula i tots els seus alumnes
void eliminarAula() {
  stdout.write('\nIntrodueix el codi de l\'aula que vols suprimir completament: ');
  final String? nomAula = stdin.readLineSync()?.trim().toUpperCase();

  if (nomAula == null || !aules.containsKey(nomAula)) {
    print('\x1B[31m[Error] L\'aula "$nomAula" no existeix.\x1B[0m');
    return;
  }

  stdout.write('Segur que vols eliminar l\'aula $nomAula amb tots els seus alumnes? (s/n): ');
  final String? confirm = stdin.readLineSync()?.trim().toLowerCase();
  if (confirm == 's' || confirm == 'si' || confirm == 'sí') {
    aules.remove(nomAula);
    print('\x1B[32m✔ Aula $nomAula i tots els seus registres eliminats correctament.\x1B[0m');
  } else {
    print('\x1B[33mOperació cancel·lada.\x1B[0m');
  }
}

/// 7. Mostrar tots els alumnes de l'institut (usant un Set per evitar duplicats)
void mostrarTotsAlumnesInstitut() {
  print('\n--- TOTS ELS ALUMNES DE L\'INSTITUT (SET SENSE DUPLICATS) ---');

  // Utilitzem un Set per fusionar tots els alumnes sense repeticions
  final Set<String> totsElsAlumnes = <String>{};

  for (final List<String> llistaAula in aules.values) {
    totsElsAlumnes.addAll(llistaAula);
  }

  if (totsElsAlumnes.isEmpty) {
    print('\x1B[33mNo hi ha cap alumne registrat a tot l\'institut.\x1B[0m');
    return;
  }

  // Ordenem alfabèticament per millor visualització
  final List<String> ordenats = totsElsAlumnes.toList()..sort();

  print('\x1B[32mTotal alumnes únics matriculats: ${ordenats.length}\x1B[0m');
  for (int i = 0; i < ordenats.length; i++) {
    // Esbrinem a quines aules està matriculat cada alumne
    final List<String> aulesMatriculat = aules.entries
        .where((entry) => entry.value.contains(ordenats[i]))
        .map((entry) => entry.key)
        .toList();

    print('${i + 1}. ${ordenats[i]} -> [Aules: ${aulesMatriculat.join(', ')}]');
  }
}
