import 'dart:async';

/// UNITAT 2.4 - EXERCICI 4: L'EVENT LOOP DE DART
///
/// Demostració de la prioritat de les dues cues del model monofil de Dart:
/// 1. MicroTask Queue: Màxima prioritat (scheduleMicrotask).
/// 2. Event Queue: Prioritat normal (Future.delayed, I/O, etc.).
///
/// L'ordre d'execució sempre serà:
///   Codi síncron -> Cua de MicroTasks -> Cua d'Events

void main() async {
  print('================================================================');
  print('   UD 2.4 - EXERCICI 4: EVENT LOOP (MICROTASK VS EVENT QUEUE)');
  print('================================================================\n');

  final Completer<void> completer = Completer<void>();

  print('1. \x1B[1m[Síncron]\x1B[0m Execució directa al fil principal.');

  // Programem un esdeveniment a la cua d'Events (fins i tot amb delay 0 ms)
  Future.delayed(const Duration(milliseconds: 0), () {
    print('4. \x1B[34m[Event Queue]\x1B[0m Executat des de la cua d\'events (Future.delayed 0ms).');
    completer.complete();
  });

  // Programem una microtasca a la cua de MicroTasks
  scheduleMicrotask(() {
    print('3. \x1B[35m[MicroTask Queue]\x1B[0m Executat des de la cua de microtasques (prioritat màxima).');
  });

  print('2. \x1B[1m[Síncron]\x1B[0m Fi del bloc de codi principal síncron.\n');

  await completer.future;

  print('\n\x1B[32m✔ Ordre verificat: El codi síncron s\'executa primer, després la cua MicroTask, i finalment l\'Event Queue.\x1B[0m');
  print('\n--- Fi de l\'exercici 4 de l\'Event Loop ---');
}
