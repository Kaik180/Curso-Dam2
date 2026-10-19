import 'producte.dart';

/// Entitat de domini que representa una beguda (Drink)
class Beguda extends Producte {
  final bool isAlcoholic;

  /// Constructor amb paràmetres amb nom
  Beguda({
    required super.id,
    required super.name,
    required super.description,
    required super.tipus,
    required super.allergens,
    required super.price,
    required super.calories,
    required super.additionalInfo,
    required super.img,
    required this.isAlcoholic,
  });

  /// Constructor factoria per inicialitzar des de Map / JSON
  factory Beguda.fromJSON(Map<String, dynamic> json) {
    return Beguda(
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
      isAlcoholic: json['isAlcoholic'] as bool? ?? false,
    );
  }

  @override
  TipusProducte getClass() => TipusProducte.beguda;

  @override
  String toString() {
    return 'Beguda(${super.toString()}, isAlcoholic: $isAlcoholic)';
  }

  @override
  String toStringSmart() {
    const String colorCyan = '\x1B[36m';
    const String colorGreen = '\x1B[32m';
    const String colorYellow = '\x1B[33m';
    const String colorRed = '\x1B[31m';
    const String colorReset = '\x1B[0m';

    final String alLergensStr =
        allergens.isEmpty ? 'Cap' : allergens.join(', ');
    final String alcoholStr = isAlcoholic
        ? '$colorRed Amb Alcohol$colorReset'
        : '$colorGreen Sense Alcohol$colorReset';

  return '''
$colorCyan╔════════════════════════════════════════════════════════╗
║ [BEGUDA - $id] $name$colorReset
$colorCyan╠════════════════════════════════════════════════════════╣$colorReset
║ Subtipus: $tipus
║ Descripció: $description
║ Graduació: $alcoholStr
║ Al·lèrgens: $colorYellow$alLergensStr$colorReset
║ Calories: $calories kcal
║ Preu: $colorGreen${price.toStringAsFixed(2)} €$colorReset
║ Info addicional: $additionalInfo
║ URL Imatge: $img
$colorCyan╚════════════════════════════════════════════════════════╝$colorReset''';
  }
}
