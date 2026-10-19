/// Enumeració amb els tipus de classes de producte suportats al domini
enum TipusProducte {
  entrant,
  principal,
  beguda,
}

/// Classe abstracta que representa el model base de qualsevol producte del restaurant "Healthys".
abstract class Producte {
  final String id;
  final String name;
  final String description;
  final String tipus;
  final List<String> allergens;
  final double price;
  final int calories;
  final String additionalInfo;
  final String img;

  /// Constructor amb paràmetres amb nom
  Producte({
    required this.id,
    required this.name,
    required this.description,
    required this.tipus,
    required this.allergens,
    required this.price,
    required this.calories,
    required this.additionalInfo,
    required this.img,
  });

  /// Mètode que retorna el tipus de classe concreta
  TipusProducte getClass();

  /// Representació estàndard en cadena
  @override
  String toString() {
    return 'Producte(id: $id, name: $name, tipus: $tipus, price: $price€, calories: $calories kcal)';
  }

  /// Representació amigable multilínia amb codis de colors ANSI
  String toStringSmart() {
    const String colorCyan = '\x1B[36m';
    const String colorGreen = '\x1B[32m';
    const String colorYellow = '\x1B[33m';
    const String colorReset = '\x1B[0m';

    final String alLergensStr =
        allergens.isEmpty ? 'Cap' : allergens.join(', ');

    return '''
$colorCyan┌────────────────────────────────────────────────────────┐
│ [$id] $name$colorReset
$colorCyan├────────────────────────────────────────────────────────┤$colorReset
│ Tipus: $tipus
│ Descripció: $description
│ Al·lèrgens: $colorYellow$alLergensStr$colorReset
│ Calories: $calories kcal
│ Preu: $colorGreen${price.toStringAsFixed(2)} €$colorReset
│ Info addicional: $additionalInfo
│ Imatge: $img
$colorCyan└────────────────────────────────────────────────────────┘$colorReset''';
  }
}
