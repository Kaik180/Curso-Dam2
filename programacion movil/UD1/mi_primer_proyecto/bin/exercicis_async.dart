import 'dart:async';
import 'dart:io';

/// Simula una funció asíncrona que triga un temps determinat en retornar un String
Future<String> simularTascaAsincrona(String nomTasca, int segons) {
  return Future.delayed(Duration(seconds: segons), () {
    print('  \x1B[33m➜ Tasca "$nomTasca" completada després de $segons segon(s).\x1B[0m');
    return 'Resultat de $nomTasca';
  });
}

/// 1. Demostració bàsica de Futures amb .then()
Future<void> demoFutureBasic() async {
  print('\n--- DEMO 1: Futures bàsics amb .then() ---');
  print('Inici de la crida...');

  final Completer<void> completer = Completer<void>();

  final Future<String> futur = simularTascaAsincrona('ConsultaBD', 2);
  print('Instància del Future rebuda immediatament: $futur');

  futur.then((data) {
    print('Valor resolt al callback .then(): \x1B[32m$data\x1B[0m');
    completer.complete();
  }).catchError((error) {
    print('\x1B[31mError capturat: $error\x1B[0m');
    completer.complete();
  });

  print('L\'execució principal continua sense bloquejar-se...');
  await completer.future;
  print('--- Fi Demo 1 ---\n');
}

/// 2. Demostració de Future.wait (tasques simultànies i ordre garantit)
Future<void> demoFutureWait() async {
  print('\n--- DEMO 2: Future.wait (Paral·lelisme concurrent) ---');
  print('Iniciant 3 tasques amb temps distints (2s, 1s, 3s)...');

  final Future<String> f1 = simularTascaAsincrona('Tasca 1 (2s)', 2);
  final Future<String> f2 = simularTascaAsincrona('Tasca 2 (1s)', 1);
  final Future<String> f3 = simularTascaAsincrona('Tasca 3 (3s)', 3);

  final Stopwatch stopwatch = Stopwatch()..start();
  final List<String> resultats = await Future.wait([f1, f2, f3]);
  stopwatch.stop();

  print('\x1B[32m✔ Totes les tasques han finalitzat en ~${(stopwatch.elapsedMilliseconds / 1000).toStringAsFixed(2)}s!\x1B[0m');
  print('Resultats en l\'ordre de declaració original: $resultats');
  print('--- Fi Demo 2 ---\n');
}

/// 3. Demostració de sintaxi Async / Await
Future<void> demoAsyncAwait() async {
  print('\n--- DEMO 3: Async / Await ---');
  print('Iniciant procés seqüencial amb await...');

  final String r1 = await simularTascaAsincrona('Pas 1', 1);
  print('Rebut: $r1');

  final String r2 = await simularTascaAsincrona('Pas 2', 1);
  print('Rebut: $r2');

  print('\x1B[32m✔ Execució seqüencial completada correctament amb await.\x1B[0m');
  print('--- Fi Demo 3 ---\n');
}

/// 4. Demostració de l'Event Loop (MicroTask queue vs Event queue)
Future<void> demoEventLoop() async {
  print('\n--- DEMO 4: Event Loop de Dart ---');
  print('Explicació: La cua de MicroTasks té prioritat absoluta sobre la cua d\'Events.');
  print('1. Inici en fil principal síncron');

  final Completer<void> completer = Completer<void>();

  // Event a la cua d'Events (fins i tot amb delay 0ms)
  Future.delayed(const Duration(milliseconds: 0), () {
    print('4. \x1B[36m[Event Queue]\x1B[0m Executat des de la cua d\'events (Future.delayed 0ms)');
    completer.complete();
  });

  // Tasca a la cua de Microtasks (màxima prioritat)
  scheduleMicrotask(() {
    print('3. \x1B[35m[MicroTask Queue]\x1B[0m Executat des de la cua de microtasques');
  });

  print('2. Fi del codi síncron de la funció');

  await completer.future;
  print('--- Fi Demo 4 ---\n');
}

/// 5. Demostració de Streams i StreamController
Future<void> demoStreams() async {
  print('\n--- DEMO 5: Streams i StreamController (Programació Reactiva) ---');
  final StreamController<String> controller = StreamController<String>();

  // Subscripció al stream
  final StreamSubscription<String> sub = controller.stream.listen(
    (item) => print('  \x1B[32m[Stream Dades]\x1B[0m Rebut: $item'),
    onError: (error) => print('  \x1B[31m[Stream Error]\x1B[0m Capturat: $error'),
    onDone: () => print('  \x1B[36m[Stream Tancat]\x1B[0m El canal s\'ha completat.'),
  );

  print('Afegint paquet 1...');
  controller.add('Dada 1: Connexió inicial');

  print('Afegint paquet 2...');
  controller.add('Dada 2: Transmissió activa');

  print('Generant un error de prova al Stream...');
  controller.addError('Error de comunicació 404');

  print('Afegint paquet 3...');
  controller.add('Dada 3: Reconnexió');

  await Future.delayed(const Duration(milliseconds: 50));

  print('Tancant el controlador del stream...');
  await controller.close();

  // Cancel·lem la subscripció
  await sub.cancel();
  print('--- Fi Demo 5 ---\n');
}

void main() async {
  bool eixir = false;

  while (!eixir) {
    print('======================================================');
    print('     EXERCICIS I DEMOSTRACIONS ASÍNCRONES (UD2.4)');
    print('======================================================');
    print('1. Future bàsic amb resolució .then() i catchError');
    print('2. Future.wait (Execució concurrent en paral·lel)');
    print('3. Sintaxi Async / Await');
    print('4. Event Loop (Cua MicroTask vs Cua d\'Events)');
    print('5. Streams i StreamController (Cinta transportadora)');
    print('6. Executar totes les demostracions');
    print('0. Tornar / Eixir');
    print('------------------------------------------------------');
    stdout.write('Tria una opció [0-6]: ');

    final String? opcio = stdin.readLineSync()?.trim();

    switch (opcio) {
      case '1':
        await demoFutureBasic();
        break;
      case '2':
        await demoFutureWait();
        break;
      case '3':
        await demoAsyncAwait();
        break;
      case '4':
        await demoEventLoop();
        break;
      case '5':
        await demoStreams();
        break;
      case '6':
        await demoFutureBasic();
        await demoFutureWait();
        await demoAsyncAwait();
        await demoEventLoop();
        await demoStreams();
        break;
      case '0':
        print('\n\x1B[32mFinalitzant mòdul asíncron.\x1B[0m');
        eixir = true;
        break;
      default:
        print('\x1B[31m[Error] Opció invàlida.\x1B[0m');
    }
  }
}
