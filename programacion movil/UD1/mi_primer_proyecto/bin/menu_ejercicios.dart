import 'dart:io';

void main() async {
  bool eixir = false;

  while (!eixir) {
    print('\x1B[2J\x1B[0;0H');
    print('\x1B[32m================================================================');
    print('     CURS DART - 2n DAM PROGRAMACIÓ MULTIMÈDIA I MÒBIL (PMDM)');
    print('         ÍNDEX D\'EXERCICIS SEPARATS PER ORDRE (UD 2.1 A 2.5)');
    print('================================================================\x1B[0m');
    print('\x1B[1m--- UD 2.1: EL LLENGUATGE DART I SINTAXI ---\x1B[0m');
    print(' 1. [UD 2.1 - Act 1] Any de traspàs (01_any_de_traspas.dart)');
    print('');
    print('\x1B[1m--- UD 2.2: FUNCIONS I COL·LECCIONS ---\x1B[0m');
    print(' 2. [UD 2.2 - Act 1] Gestió d\'Aules i Alumnes (01_gestio_aules.dart)');
    print(' 3. [UD 2.2 - Act 2] Les 60 Preguntes Funcionals Juntes (02_les_60_preguntes.dart)');
    print('');
    print('\x1B[1m--- UD 2.3: PROGRAMACIÓ ORIENTADA A OBJECTES (POO) ---\x1B[0m');
    print(' 4. [UD 2.3 - Act 1] Demostració d\'Entitats de Domini (01_entitats_demostracio.dart)');
    print('');
    print('\x1B[1m--- UD 2.4: PROGRAMACIÓ ASÍNCRONA ---\x1B[0m');
    print(' 5. [UD 2.4 - Act 1] Futures bàsics i .then() (01_futures_basic.dart)');
    print(' 6. [UD 2.4 - Act 1] Future.wait en paral·lel (02_future_wait.dart)');
    print(' 7. [UD 2.4 - Act 2] Sintaxi Async / Await (03_async_await.dart)');
    print(' 8. [UD 2.4 - Act 2] Event Loop: MicroTask vs Event Queue (04_event_loop.dart)');
    print(' 9. [UD 2.4 - Avançat] Streams i StreamController (05_streams.dart)');
    print('');
    print('\x1B[1m--- UD 2.5: PROJECTES DART I API REST HTTP ---\x1B[0m');
    print('10. [UD 2.5 - Act 1] Petició i Descodificació API HTTP (01_peticio_api_http.dart)');
    print('11. [UD 2.5 - Act 2] Restaurant Healthys Express CLI (02_healthys_cli.dart)');
    print('');
    print(' 0. Eixir');
    print('----------------------------------------------------------------');
    stdout.write('Tria quin exercici vols executar [0-11]: ');

    final String? opcio = stdin.readLineSync()?.trim();

    switch (opcio) {
      case '1':
        await _executarScript('bin/ud2_1_basicos/act_01_any_de_traspas.dart');
        break;
      case '2':
        await _executarScript('bin/ud2_2_funcions_coleccions/act_01_gestio_aules.dart');
        break;
      case '3':
        await _executarScript('bin/ud2_2_funcions_coleccions/act_02_les_60_preguntes.dart');
        break;
      case '4':
        await _executarScript('bin/ud2_3_poo/act_01_entitats_demostracio.dart');
        break;
      case '5':
        await _executarScript('bin/ud2_4_asincronia/act_01_futures_basic.dart');
        break;
      case '6':
        await _executarScript('bin/ud2_4_asincronia/act_02_future_wait.dart');
        break;
      case '7':
        await _executarScript('bin/ud2_4_asincronia/act_03_async_await.dart');
        break;
      case '8':
        await _executarScript('bin/ud2_4_asincronia/act_04_event_loop.dart');
        break;
      case '9':
        await _executarScript('bin/ud2_4_asincronia/act_05_streams.dart');
        break;
      case '10':
        await _executarScript('bin/ud2_5_projectes_http/act_01_peticio_api_http.dart');
        break;
      case '11':
        await _executarScript('bin/ud2_5_projectes_http/act_02_healthys_cli.dart');
        break;
      case '0':
        print('\n\x1B[32mFinalitzant el llançador d\'exercicis. Fins prompte!\x1B[0m');
        eixir = true;
        break;
      default:
        print('\x1B[31m[Error] Opció invàlida. Tria entre 0 i 11.\x1B[0m');
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

void _pausa() {
  stdout.write('\nPrem [ENTER] per continuar...');
  stdin.readLineSync();
}
