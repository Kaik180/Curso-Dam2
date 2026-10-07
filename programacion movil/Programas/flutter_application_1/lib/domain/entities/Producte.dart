enum TipoClase {
  starter,
  main,
  drink,
}

abstract class Producte {
  String id;
  String nombre;
  String descripcion;
  String tipo;
  List<String> alergenos;
  double precio;
  int calorias;
  String informacionAdicional;
  String imagen;

  Producte({
    required this.id,
    required this.nombre,
    required this.descripcion,
    required this.tipo,
    required this.alergenos,
    required this.precio,
    required this.calorias,
    required this.informacionAdicional,
    required this.imagen,
  });

  TipoClase obtenerTipoClase();
  String toStringSmart();

  @override
  String toString() {
    return 'ID: $id, Nombre: $nombre, Precio: $precio';
  }
}