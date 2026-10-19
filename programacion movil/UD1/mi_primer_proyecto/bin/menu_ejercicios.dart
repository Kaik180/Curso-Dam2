import 'dart:io';

void main() async {
  bool eixir = false;

  while (!eixir) {
    print('\x1B[2J\x1B[0;0H');
    print('\x1B[32m================================================================');
    print('       CURS DART - 2n DAM PROGRAMACIÓ MULTIMÈDIA I MÒBIL');
    print('               MENÚ D\'EXERCICIS RESOLTS (UD2)');
    print('================================================================\x1B[0m');
    print('1. [UD 2.1 - Act 1] Any de traspàs (Leap Year Checker & Loop)');
    print('2. [UD 2.2 - Act 1] Gestió d\'Aules i Alumnes (Map & Set)');
    print('3. [UD 2.2 - Act 2] Les 60 Preguntes de Programació Funcional');
    print('4. [UD 2.4 - Act 1 & 2] Demostracions Asíncrones (Futures, Async, Streams)');
    print('5. [UD 2.3 & 2.5 - Projecte Final] Restaurant Healthys CLI (API REST)');
    print('6. [Documentació] Consultar resum del Mapa Conceptual Dart vs Java');
    print('0. Eixir');
    print('----------------------------------------------------------------');
    stdout.write('Selecciona quin exercici vols executar [0-6]: ');

    final String? opcio = stdin.readLineSync()?.trim();

    switch (opcio) {
      case '1':
        await _executarScript('bin/leap_year.dart');
        break;
      case '2':
        await _executarScript('bin/gestio_aules.dart');
        break;
      case '3':
        await _executarScript('bin/the_sixty_questions.dart');
        break;
      case '4':
        await _executarScript('bin/exercicis_async.dart');
        break;
      case '5':
        await _executarScript('bin/healthys_cli.dart');
        break;
      case '6':
        _mostrarDocumentacio();
        break;
      case '0':
        print('\n\x1B[32mFinalitzant el llançador d\'exercicis. Fins prompte!\x1B[0m');
        eixir = true;
        break;
      default:
        print('\x1B[31m[Error] Opció invàlida. Tria entre 0 i 6.\x1B[0m');
        _pausa();
    }
  }
}

Future<void> _executarScript(String scriptRelatiu) async {
  print('\n\x1B[33m--- Llançant $scriptRelatiu... ---\x1B[0m\n');
  final Process proc = await Process.start(
    'dart',
    [scriptRelatiu],
    mode: ProcessStartMode.inheritStdio,
  );
  await proc.exitCode;
  _pausa();
}

void _mostrarDocumentacio() {
  print('\n\x1B[36m================================================================');
  print('    MAPA CONCEPTUAL I COMPARATIVA DART VS JAVA (UD 2.1)');
  print('================================================================\x1B[0m');
  print('''
El document complet està disponible a:
doc/mapa_conceptual_dart_vs_java.md

Punts Clau destacats:
1. PUNT D'ENTRADA:
   - Dart: void main() lliure a nivell de fitxer.
   - Java: public static void main(String[] args) dins d'una classe.

2. SOUND NULL SAFETY:
   - Dart: Natiu per defecte (int no admet null, int? sí).
     Operadors: ?, !, ??, ??=, ?.
   - Java: No natiu; qualsevol referència pot causar NullPointerException.

3. IMMUTABILITAT:
   - const: Immutable en temps de compilació.
   - final: Immutable en temps d'execució (referència constant).

4. CONCURRÈNCIA:
   - Dart: Un sol fil d'execució gestionat per Event Loop (MicroTask i Event Queue).
   - Java: Multithreading natiu amb fils del sistema operatiu (Thread, Pool).
''');
  _pausa();
}

void _pausa() {
  stdout.write('\nPrem [ENTER] per continuar...');
  stdin.readLineSync();
}
