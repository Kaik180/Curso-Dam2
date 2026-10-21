// UNITAT 2.4 - EXERCICI 2: Future.wait (PARAL·LELISME CONCURRENT)
//
// Permet llançar múltiples tasques asíncrones en paral·lel
// i esperar a que totes finalitzen, garantint l'ordre original de la llista.

Future<String> descarregarFitxer(String nom, int segons) {
  return Future.delayed(Duration(seconds: segons), () {
    print('  ➜ Fitxer "$nom" descarregat després de $segons s.');
    return 'Contingut de $nom';
  });
}

void main() async {
  print('================================================================');
  print('   UD 2.4 - EXERCICI 2: Future.wait (EXECUCIÓ CONCURRENT)');
  print('================================================================\n');

  print('Iniciant 3 descàrregues simultànies (2s, 1s, 3s)...');

  final Future<String> f1 = descarregarFitxer('imatge.png (2s)', 2);
  final Future<String> f2 = descarregarFitxer('dades.json (1s)', 1);
  final Future<String> f3 = descarregarFitxer('manual.pdf (3s)', 3);

  final Stopwatch cronometre = Stopwatch()..start();

  // Future.wait executa concurrentment i retorna una llista amb els resultats
  final List<String> resultats = await Future.wait([f1, f2, f3]);
  cronometre.stop();

  print('\n\x1B[32m✔ Totes les descàrregues han acabat en ~${(cronometre.elapsedMilliseconds / 1000).toStringAsFixed(2)}s (no en 6s suma)!');
  print('Resultats en l\'ordre original: $resultats\x1B[0m');
  print('\n--- Fi de l\'exercici 2 de Future.wait ---');
}
