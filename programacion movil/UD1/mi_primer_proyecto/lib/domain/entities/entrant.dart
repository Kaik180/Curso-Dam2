import 'producte.dart';

/// Entitat de domini que representa un entrant (Starter)
class Entrant extends Producte {
  final List<String> dietType;

  /// Constructor amb paràmetres amb nom
  Entrant({
    required super.id,
    required super.name,
    required super.description,
    required super.tipus,
    required super.allergens,
    required super.price,
    required super.calories,
    required super.additionalInfo,
    required super.img,
    required this.dietType,
  });

  /// Constructor factoria per inicialitzar des de Map / JSON
  factory Entrant.fromJSON(Map<String, dynamic> json) {
    return Entrant(
      id: json['id'] as String? ?? '',
      name: json['name'] as String? ?? 'Sense nom',
      description: json['description'] as String? ?? '',
      tipus: json['tipus'] as String? ?? '',
      allergens: (json['allergens'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
      price: (json['price'] as num?)?.toDouble() ?? 0.0,
      calories: (json['calories'] as num?)?.toInt() ?? 0,
      additionalInfo: json['additionalInfo'] as String? ?? '',
      img: json['img'] as String? ?? '',
      dietType: (json['dietType'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
    );
  }

  @override
  TipusProducte getClass() => TipusProducte.entrant;

  @override
  String toString() {
    return 'Entrant(${super.toString()}, dietType: $dietType)';
  }

  @override
  String toStringSmart() {
    const String colorMagenta = '\x1B[35m';
    const String colorGreen = '\x1B[32m';
    const String colorYellow = '\x1B[33m';
    const String colorReset = '\x1B[0m';

    final String alLergensStr =
        allergens.isEmpty ? 'Cap' : allergens.join(', ');
    final String dietsStr = dietType.isEmpty ? 'Cap' : dietType.join(', ');

    return '''
$colorMagenta╔════════════════════════════════════════════════════════╗
║ [ENTRANT - $id] $name$colorReset
$colorMagenta╠════════════════════════════════════════════════════════╣$colorReset
║ Subtipus: $tipus
║ Descripció: $description
║ Tipus de dieta: $colorGreen$dietsStr$colorReset
║ Al·lèrgens: $colorYellow$alLergensStr$colorReset
║ Calories: $calories kcal
║ Preu: $colorGreen${price.toStringAsFixed(2)} €$colorReset
║ Info addicional: $additionalInfo
║ URL Imatge: $img
$colorMagenta╚════════════════════════════════════════════════════════╝$colorReset''';
  }
}
