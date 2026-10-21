import 'dart:async';

/// UNITAT 2.4 - EXERCICI 5: STREAMS I STREAMCONTROLLER
///
/// Els Streams funcionen com una "cinta transportadora" reactiva d'esdeveniments
/// en el temps. Aquest exercici demostra:
/// - Creació d'un StreamController<String>
/// - Subscripció amb .listen (onData, onError, onDone)
/// - Emissió de dades i errors
/// - Tancament controlat

void main() async {
  print('================================================================');
  print('   UD 2.4 - EXERCICI 5: STREAMS I STREAMCONTROLLER');
  print('================================================================\n');

  final StreamController<String> controller = StreamController<String>();

  // Definim l'escolta (listener)
  final StreamSubscription<String> sub = controller.stream.listen(
    (dades) {
      print('  \x1B[32m[Stream Rebut]\x1B[0m Paquet: "$dades"');
    },
    onError: (error) {
      print('  \x1B[31m[Stream Error]\x1B[0m Error capturat: "$error"');
    },
    onDone: () {
      print('  \x1B[36m[Stream Tancat]\x1B[0m El canal s\'ha tancat satisfactòriament.');
    },
  );

  print('1. Emetent esdeveniments al stream...');
  controller.add('Missatge 1: Sensor de temperatura activat');
  controller.add('Missatge 2: Lectura a 24.5 ºC');

  print('2. Emetent un error de prova...');
  controller.addError('Error 503: Sensor temporalment descalibrat');

  print('3. Emetent l\'últim missatge de restabliment...');
  controller.add('Missatge 3: Sensor estabilitzat');

  // Petita pausa per permetre que la cua processe les emissions
  await Future.delayed(const Duration(milliseconds: 50));

  print('4. Tancant el controlador...');
  await controller.close();

  // Cancel·lem la subscripció
  await sub.cancel();

  print('\n\x1B[32m✔ El Stream s\'ha executat i tancat seguint el patró reactiu!\x1B[0m');
  print('\n--- Fi de l\'exercici 5 de Streams ---');
}
