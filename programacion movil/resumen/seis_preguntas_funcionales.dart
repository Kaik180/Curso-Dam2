// ============================================================================
// 6 PREGUNTAS CLAVE DE PROGRAMACIÓN FUNCIONAL PARA EXAMEN
// ============================================================================

void main() {
  print('===============================================================');
  print('     6 PREGUNTAS TÍPICAS DE EXAMEN - PROGRAMACIÓN FUNCIONAL    ');
  print('===============================================================\n');

  final List<int> numeros = [-3, 2, -1, 0, 4, 23, 17, -90, 8, 12];
  final List<String> palabras = ['Dart', 'Flutter', 'DAM', 'Asociacion', 'Examen', 'Movil'];
  final List<Map<String, dynamic>> productos = [
    {'nombre': 'Portátil', 'precio': 1200.0, 'categoria': 'Electrónica', 'stock': 5},
    {'nombre': 'Ratón', 'precio': 15.0, 'categoria': 'Accesorios', 'stock': 25},
    {'nombre': 'Teclado', 'precio': 85.0, 'categoria': 'Accesorios', 'stock': 0},
    {'nombre': 'Monitor', 'precio': 350.0, 'categoria': 'Electrónica', 'stock': 8},
  ];

  // --------------------------------------------------------------------------
  // PREGUNTA 1: FILTRADO CON WHERE
  // "Obtener una lista con solo los números pares positivos"
  // --------------------------------------------------------------------------
  print('1. Filtrado (where): Números pares positivos:');
  final paresPositivos = numeros.where((n) => n > 0 && n % 2 == 0).toList();
  print('   Resultado: $paresPositivos\n');

  // --------------------------------------------------------------------------
  // PREGUNTA 2: TRANSFORMACIÓN CON MAP
  // "Obtener una lista con la longitud de cada palabra en mayúsculas"
  // --------------------------------------------------------------------------
  print('2. Transformación (map): Palabras en mayúsculas y su longitud:');
  final mayusculas = palabras.map((p) => '${p.toUpperCase()} (${p.length} chars)').toList();
  print('   Resultado: $mayusculas\n');

  // --------------------------------------------------------------------------
  // PREGUNTA 3: ACUMULACIÓN CON REDUCE
  // "Obtener el número mayor de una lista usando reduce"
  // --------------------------------------------------------------------------
  print('3. Reducción (reduce): Elemento máximo de la lista:');
  final maximo = numeros.reduce((actualMax, n) => n > actualMax ? n : actualMax);
  print('   Resultado máximo: $maximo\n');

  // --------------------------------------------------------------------------
  // PREGUNTA 4: ACUMULACIÓN CON FOLD
  // "Calcular el valor total del inventario (precio * stock) usando fold"
  // --------------------------------------------------------------------------
  print('4. Acumulación (fold): Valor total del stock de productos:');
  final totalInventario = productos.fold<double>(
    0.0,
    (acumulado, item) => acumulado + ((item['precio'] as double) * (item['stock'] as int)),
  );
  print('   Resultado total: \$${totalInventario.toStringAsFixed(2)}\n');

  // --------------------------------------------------------------------------
  // PREGUNTA 5: VALIDACIÓN CONDICIONAL (EVERY Y ANY)
  // "Comprobar si hay algún producto agotado (stock == 0) y si todos tienen precio > 0"
  // --------------------------------------------------------------------------
  print('5. Condicionales booleanos (any / every):');
  final hayAgotados = productos.any((p) => p['stock'] == 0);
  final todosTienenPrecio = productos.every((p) => (p['precio'] as double) > 0);
  print('   ¿Hay algún producto agotado? $hayAgotados');
  print('   ¿Todos los productos tienen precio positivo? $todosTienenPrecio\n');

  // --------------------------------------------------------------------------
  // PREGUNTA 6: ENCADENAMIENTO COMBINADO (WHERE + MAP + REDUCE / JOIN)
  // "Obtener los nombres en una sola cadena separados por comas de productos de Electrónica con stock disponible"
  // --------------------------------------------------------------------------
  print('6. Encadenamiento funcional (where + map + join):');
  final nombresElectronicaEnStock = productos
      .where((p) => p['categoria'] == 'Electrónica' && (p['stock'] as int) > 0)
      .map((p) => p['nombre'] as String)
      .join(', ');
  print('   Resultado: "$nombresElectronicaEnStock"\n');
}
