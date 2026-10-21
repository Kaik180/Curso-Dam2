import 'dart:async';

/// UNITAT 2.4 - EXERCICI 1: FUTURES BÀSICS I RESOLUCIÓ AMB .then()
///
/// Simula una operació asíncrona que es resol al cap d'un temps determinat.

Future<String> obtenirDadesUsuari() {
  return Future.delayed(const Duration(seconds: 2), () {
    print('  [Xarxa] Servidor ha respost després de 2 segons.');
    return 'Dades de l\'usuari: Joan Garcia (ID: 4892)';
  });
}

void main() async {
  print('================================================================');
  print('   UD 2.4 - EXERCICI 1: FUTURES BÀSICS AMB .then()');
  print('================================================================\n');

  print('1. Iniciant la petició del Future...');
  final Completer<void> completer = Completer<void>();

  final Future<String> futur = obtenirDadesUsuari();
  print('2. Instància rebuda immediatament (estat no resolt): $futur');

  futur.then((resultat) {
    print('3. \x1B[32m✔ Valor resolt al callback .then(): "$resultat"\x1B[0m');
    completer.complete();
  }).catchError((error) {
    print('\x1B[31mError produït: $error\x1B[0m');
    completer.complete();
  });

  print('4. El fil principal continua executant altres instruccions...');

  // Esperem a que el callback .then() es resolga abans d'acabar el procés
  await completer.future;
  print('\n--- Fi de l\'exercici 1 de Futures ---');
}
