import 'dart:io';

/// Funció que determina si un any és de traspàs (leap year).
///
/// Regles:
/// - Un any és de traspàs si és divisible per 4.
/// - Excepte si és divisible per 100, en aquest cas NO ho és,
///   llevat que també siga divisible per 400.
///
/// Exemples:
/// - 2000 i 1996 -> Són de traspàs.
/// - 1900 i 1901 -> NO són de traspàs.
bool isLeapYear(int year) {
  if (year % 4 != 0) {
    return false;
  } else if (year % 100 != 0) {
    return true;
  } else {
    return year % 400 == 0;
  }
}

/// Funció que calcula el següent any de traspàs a partir d'un any donat.
int nextLeapYear(int year) {
  int next = year + 1;
  while (!isLeapYear(next)) {
    next++;
  }
  return next;
}

void main() {
  print('==================================================');
  print('   ACTIVITAT 1: COMPROVADOR D\'ANYS DE TRASPÀS');
  print('   (Introdueix "EXIT" per finalitzar el programa)');
  print('==================================================\n');

  bool keepRunning = true;

  while (keepRunning) {
    stdout.write('Introdueix un any (o "EXIT" per eixir): ');
    
    // Lectura de l'entrada utilitzant Null Safety
    final String? input = stdin.readLineSync();

    // Gestió de valors nuls utilitzant l'operador null-coalescing (??)
    final String sanitizedInput = (input ?? '').trim();

    if (sanitizedInput.isEmpty) {
      print('\x1B[33m[Avís] No has introduït cap valor. Torna-ho a provar.\x1B[0m\n');
      continue;
    }

    if (sanitizedInput.toUpperCase() == 'EXIT') {
      print('\n\x1B[32mGràcies per utilitzar el programa. Adéu!\x1B[0m');
      keepRunning = false;
      break;
    }

    // Gestió d'errors d'entrada no numèrica
    try {
      final int year = int.parse(sanitizedInput);

      if (year <= 0) {
        print('\x1B[31m[Error] Si us plau, introdueix un any positiu vàlid.\x1B[0m\n');
        continue;
      }

      if (isLeapYear(year)) {
        print('\x1B[32m✔ L\'any $year ÉS un any de traspàs (de 366 dies).\x1B[0m\n');
      } else {
        final int next = nextLeapYear(year);
        print('\x1B[31m✘ L\'any $year NO és de traspàs.\x1B[0m');
        print('\x1B[36m➜ El següent any de traspàs serà el $next.\x1B[0m\n');
      }
    } on FormatException {
      print('\x1B[31m[Error] "$sanitizedInput" no és un número enter vàlid. Introdueix un any numèric o "EXIT".\x1B[0m\n');
    } catch (e) {
      print('\x1B[31m[Error inesperat] ${e.toString()}\x1B[0m\n');
    }
  }
}
