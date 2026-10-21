// UNITAT 2.4 - EXERCICI 3: SINTAXI ASYNC / AWAIT
//
// L'ús de la paraula clau await permet escriure codi asíncron amb
// la mateixa claredat i llegibilitat seqüencial que el codi síncron.

Future<String> connectarBaseDades() async {
  await Future.delayed(const Duration(seconds: 1));
  return 'Connexió BD OK';
}

Future<String> consultarUsuari(String connexio) async {
  await Future.delayed(const Duration(seconds: 1));
  return 'Usuari: Marta Vidal [Estat: Actiu]';
}

Future<String> tancarConnexio() async {
  await Future.delayed(const Duration(milliseconds: 500));
  return 'Connexió tancada de forma segura';
}

void main() async {
  print('================================================================');
  print('   UD 2.4 - EXERCICI 3: SINTAXI ASYNC / AWAIT');
  print('================================================================\n');

  print('1. Iniciant procés asíncron seqüencial...');

  final String pas1 = await connectarBaseDades();
  print('  ➜ Pas 1 completat: \x1B[36m$pas1\x1B[0m');

  final String pas2 = await consultarUsuari(pas1);
  print('  ➜ Pas 2 completat: \x1B[32m$pas2\x1B[0m');

  final String pas3 = await tancarConnexio();
  print('  ➜ Pas 3 completat: \x1B[33m$pas3\x1B[0m');

  print('\n\x1B[32m✔ Procés completat amb await de manera neta i ordenada sense callbacks aniuats!\x1B[0m');
  print('\n--- Fi de l\'exercici 3 d\'Async/Await ---');
}
