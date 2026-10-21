import 'dart:io';

/// UNITAT 2.1 - ACTIVITAT 1: COMPROVADOR D'ANYS DE TRASPÀS
///
/// Regles:
/// - Un any és de traspàs si és múltiple de 4.
/// - Excepte si és múltiple de 100, en aquest cas NO ho és,
///   llevat que també siga múltiple de 400.
/// - Bucle continu fins a introduir 'EXIT'.
/// - Gestió d'errors i Null Safety.
bool isLeapYear(int year) {
  if (year % 4 != 0) {
    return false;
  } else if (year % 100 != 0) {
    return true;
  } else {
    return year % 400 == 0;
  }
}

int nextLeapYear(int year) {
  int next = year + 1;
  while (!isLeapYear(next)) {
    next++;
  }
  return next;
}

void main() {
  print('================================================================');
  print('   UD 2.1 - ACTIVITAT 1: COMPROVADOR D\'ANYS DE TRASPÀS');
  print('   (Introdueix "EXIT" per finalitzar)');
  print('================================================================\n');

  bool keepRunning = true;

  while (keepRunning) {
    stdout.write('Introdueix un any (o "EXIT"): ');
    final String? input = stdin.readLineSync();
    final String sanitized = (input ?? '').trim();

    if (sanitized.isEmpty) {
      print('\x1B[33m[Avís] No has introduït cap valor. Torna-ho a provar.\x1B[0m\n');
      continue;
    }

    if (sanitized.toUpperCase() == 'EXIT') {
      print('\n\x1B[32mSortint de l\'exercici d\'anys de traspàs. Adéu!\x1B[0m');
      keepRunning = false;
      break;
    }

    try {
      final int year = int.parse(sanitized);
      if (year <= 0) {
        print('\x1B[31m[Error] Introdueix un any positiu vàlid.\x1B[0m\n');
        continue;
      }

      if (isLeapYear(year)) {
        print('\x1B[32m✔ L\'any $year ÉS un any de traspàs (366 dies).\x1B[0m\n');
      } else {
        final int next = nextLeapYear(year);
        print('\x1B[31m✘ L\'any $year NO és de traspàs.\x1B[0m');
        print('\x1B[36m➜ El següent any de traspàs serà el $next.\x1B[0m\n');
      }
    } on FormatException {
      print('\x1B[31m[Error] "$sanitized" no és un número enter vàlid.\x1B[0m\n');
    }
  }
}
