import 'Producte.dart';

class Principal extends Producte {
  List<String> tipoDieta;

  Principal({
    required String id,
    required String nombre,
    required String descripcion,
    required String tipo,
    required List<String> alergenos,
    required double precio,
    required int calorias,
    required String informacionAdicional,
    required String imagen,
    required this.tipoDieta,
  }) : super(
          id: id,
          nombre: nombre,
          descripcion: descripcion,
          tipo: tipo,
          alergenos: alergenos,
          precio: precio,
          calorias: calorias,
          informacionAdicional: informacionAdicional,
          imagen: imagen,
        );

  factory Principal.fromJSON(Map<String, dynamic> json) {
    return Principal(
      id: json['id'] ?? '',
      nombre: json['nombre'] ?? '',
      descripcion: json['descripcion'] ?? '',
      tipo: json['tipo'] ?? '',
      alergenos: List<String>.from(json['alergenos'] ?? []),
      precio: (json['precio'] as num?)?.toDouble() ?? 0.0,
      calorias: json['calorias'] ?? 0,
      informacionAdicional: json['informacionAdicional'] ?? '',
      imagen: json['imagen'] ?? '',
      tipoDieta: List<String>.from(json['tipoDieta'] ?? []),
    );
  }

  @override
  TipoClase obtenerTipoClase() {
    return TipoClase.main;
  }

  @override
  String toString() {
    return 'Principal: $nombre, Precio: $precio, Dietas: $tipoDieta';
  }

  @override
  String toStringSmart() {
    return '''\x1B[35m
=== PLAT PRINCIPAL: $nombre ===\x1B[0m
  \x1B[33mIdentificador:\x1B[0m $id
  \x1B[33mDescripción:\x1B[0m $descripcion
  \x1B[33mTipo:\x1B[0m $tipo
  \x1B[33mAlérgenos:\x1B[0m $alergenos
  \x1B[33mDietas:\x1B[0m $tipoDieta
  \x1B[33mCalorías:\x1B[0m $calorias kcal
  \x1B[33mPrecio:\x1B[0m $precio €
  \x1B[33mInformación adicional:\x1B[0m $informacionAdicional
  \x1B[33mImagen:\x1B[0m $imagen''';
  }
}