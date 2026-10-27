import 'dart:convert';
import 'package:http/http.dart' as http;

// ============================================================================
// 1. CLASE CURSO
// ============================================================================
class Curso {
  final String codigo;
  final String nombre;
  final String descripcion;

  Curso({
    required this.codigo,
    required this.nombre,
    required this.descripcion,
  });

  // Constructor con nombre (factory) para deserializar desde JSON / Map
  factory Curso.fromJson(Map<String, dynamic> json) {
    return Curso(
      codigo: json['codigo'] ?? '',
      nombre: json['nombre'] ?? '',
      descripcion: json['descripcion'] ?? '',
    );
  }

  Map<String, dynamic> toJson() => {
        'codigo': codigo,
        'nombre': nombre,
        'descripcion': descripcion,
      };

  @override
  String toString() => 'Curso [$codigo] $nombre: $descripcion';
}

// ============================================================================
// 2. CLASE ESTUDIANTE (SUPERCLASE)
// ============================================================================
class Estudiante {
  final String nombre;
  final String apellido;
  final String dni;
  final DateTime fechaNacimiento;
  Curso curso;

  Estudiante({
    required this.nombre,
    required this.apellido,
    required this.dni,
    required this.fechaNacimiento,
    required this.curso,
  });

  // Método GET para obtener la edad usando DateTime.now()
  int get edad {
    final DateTime ahora = DateTime.now();
    int calculoEdad = ahora.year - fechaNacimiento.year;
    // Si todavía no ha cumplido años este año, restamos 1
    if (ahora.month < fechaNacimiento.month ||
        (ahora.month == fechaNacimiento.month && ahora.day < fechaNacimiento.day)) {
      calculoEdad--;
    }
    return calculoEdad;
  }

  @override
  String toString() {
    return '$nombre $apellido (DNI: $dni | Edad: $edad años | Curso: ${curso.nombre})';
  }
}

// ============================================================================
// 3. SUBCLASE DELEGADO (HEREDA DE ESTUDIANTE)
// ============================================================================
class Delegado extends Estudiante {
  final String claseGestionada;

  Delegado({
    required super.nombre,
    required super.apellido,
    required super.dni,
    required super.fechaNacimiento,
    required super.curso,
    required this.claseGestionada,
  });

  // Nota: Sintaxis alternativa compatible con versiones anteriores:
  // Delegado({
  //   required String nombre,
  //   required String apellido,
  //   required String dni,
  //   required DateTime fechaNacimiento,
  //   required Curso curso,
  //   required this.claseGestionada,
  // }) : super(nombre: nombre, apellido: apellido, dni: dni, fechaNacimiento: fechaNacimiento, curso: curso);

  @override
  String toString() {
    return '${super.toString()} [DELEGADO de $claseGestionada]';
  }
}

// ============================================================================
// 4. SUBCLASE ESTUDIANTE DE INTERCAMBIO (HEREDA DE ESTUDIANTE)
// ============================================================================
class EstudianteIntercambio extends Estudiante {
  final String paisOrigen;
  final String duracionEstancia; // Por ejemplo "6 meses" o "1 cuatrimestre"

  EstudianteIntercambio({
    required super.nombre,
    required super.apellido,
    required super.dni,
    required super.fechaNacimiento,
    required super.curso,
    required this.paisOrigen,
    required this.duracionEstancia,
  });

  @override
  String toString() {
    return '${super.toString()} [INTERCAMBIO de $paisOrigen, estancia: $duracionEstancia]';
  }
}

// ============================================================================
// 5. CLASE MATRÍCULA
// ============================================================================
class Matricula {
  final int anio;
  final List<Estudiante> alumnos;
  final Curso curso;

  Matricula({
    required this.anio,
    required this.alumnos,
    required this.curso,
  });

  void matricularAlumno(Estudiante estudiante) {
    alumnos.add(estudiante);
  }

  @override
  String toString() {
    return '''
============================================================
 Matrícula Año $anio - ${curso.nombre} (${curso.codigo})
 Total alumnos inscritos: ${alumnos.length}
============================================================
${alumnos.map((a) => '  * $a').join('\n')}
''';
  }
}

// ============================================================================
// 6. GESTOR DE SERVICIOS / MÉTODOS DE CARGA DE CURSOS DESDE API
// ============================================================================
class CursoService {
  static const String endpoint = 'https://api.asociacion/cursos';

  // --------------------------------------------------------------------------
  // FORMA 1: ASÍNCRONA
  // Opción 1.A: Con Future y .then() (Callback no bloqueante)
  // --------------------------------------------------------------------------
  static void cargarCursosConThen(
    List<Curso> listaDestino, {
    void Function(List<Curso>)? alTerminar,
    void Function(Object error)? alFallar,
  }) {
    print('[ASYNC .then] Solicitando cursos al API...');
    http.get(Uri.parse(endpoint)).then((response) {
      if (response.statusCode == 200) {
        final String decodedBody = utf8.decode(response.bodyBytes);
        final List<dynamic> jsonList = jsonDecode(decodedBody) as List;
        listaDestino.clear();
        listaDestino.addAll(jsonList.map((e) => Curso.fromJson(e as Map<String, dynamic>)));
        print('[ASYNC .then] ¡Cursos cargados con éxito! (${listaDestino.length} elementos)');
        alTerminar?.call(listaDestino);
      } else {
        print('[ASYNC .then] Error en respuesta HTTP: ${response.statusCode}');
      }
    }).catchError((error) {
      print('[ASYNC .then] Falló la conexión (normal si la URL es simulada): $error');
      alFallar?.call(error);
    });
  }

  // --------------------------------------------------------------------------
  // FORMA 1: ASÍNCRONA (Estándar moderno)
  // Opción 1.B: Con async / await
  // --------------------------------------------------------------------------
  static Future<List<Curso>> cargarCursosAsync() async {
    print('[ASYNC await] Petición GET a $endpoint');
    final response = await http.get(Uri.parse(endpoint));
    if (response.statusCode == 200) {
      final String decodedBody = utf8.decode(response.bodyBytes);
      final List<dynamic> jsonList = jsonDecode(decodedBody) as List;
      return jsonList.map((e) => Curso.fromJson(e as Map<String, dynamic>)).toList();
    } else {
      throw Exception('Error HTTP: ${response.statusCode}');
    }
  }

  // --------------------------------------------------------------------------
  // FORMA 2: SÍNCRONA
  // En Dart, el profesor explica en el temario que "comportamiento síncrono"
  // significa forzar la secuencialidad con await para esperar el resultado
  // antes de continuar a la siguiente línea de ejecución:
  // --------------------------------------------------------------------------
  static Future<void> cargarCursosSecuencialSincrono(List<Curso> listaDestino) async {
    print('[SYNC-LIKE await] Iniciando carga con espera secuencial...');
    try {
      final response = await http.get(Uri.parse(endpoint));
      if (response.statusCode == 200) {
        final List<dynamic> jsonList = jsonDecode(utf8.decode(response.bodyBytes)) as List;
        listaDestino.clear();
        listaDestino.addAll(jsonList.map((e) => Curso.fromJson(e as Map<String, dynamic>)));
        print('[SYNC-LIKE await] Cursos asignados a la lista.');
      }
    } catch (e) {
      print('[SYNC-LIKE await] Error de red capturado: $e');
    }
  }

  // --------------------------------------------------------------------------
  // FORMA 2 ALTERNATIVA: CARGA SÍNCRONA PURA (In-Memory / JSON Parse)
  // Si el profesor se refiere a un método puramente síncrono (sin Future),
  // procesa un JSON local o datos estáticos de forma síncrona:
  // --------------------------------------------------------------------------
  static List<Curso> cargarCursosSincronoDesdeJson(String jsonString) {
    print('[SYNC PURA] Procesando cadena JSON en el hilo principal...');
    final List<dynamic> jsonList = jsonDecode(jsonString) as List;
    return jsonList.map((e) => Curso.fromJson(e as Map<String, dynamic>)).toList();
  }
}

// ============================================================================
// DEMOSTRACIÓN DE EJECUCIÓN
// ============================================================================
void main() {
  print('===============================================================');
  print('     SIMULACIÓN PRÁCTICA EXAMEN: ASOCIACIÓN DE ESTUDIANTES     ');
  print('===============================================================\n');

  // 1. Crear cursos de prueba
  final dam2 = Curso(
    codigo: 'DAM-2',
    nombre: 'Desarrollo de Aplicaciones Multiplataforma 2º',
    descripcion: 'Programación Móvil, Sistemas de Gestión y Acceso a Datos.',
  );

  // 2. Crear alumnos de distintos tipos
  final alumno1 = Estudiante(
    nombre: 'Kevin',
    apellido: 'García',
    dni: '12345678A',
    fechaNacimiento: DateTime(2002, 5, 14),
    curso: dam2,
  );

  final delegado = Delegado(
    nombre: 'Lucía',
    apellido: 'Martínez',
    dni: '87654321B',
    fechaNacimiento: DateTime(2001, 11, 20),
    curso: dam2,
    claseGestionada: 'Aula 204 - 2º DAM',
  );

  final intercambio = EstudianteIntercambio(
    nombre: 'Pierre',
    apellido: 'Dubois',
    dni: 'X9876543Y',
    fechaNacimiento: DateTime(2003, 2, 10),
    curso: dam2,
    paisOrigen: 'Francia',
    duracionEstancia: '9 meses (Curso completo)',
  );

  // 3. Probar getters de edad
  print('--- COMPROBACIÓN DE EDADES (Getter edad con DateTime.now()) ---');
  print('${alumno1.nombre}: ${alumno1.edad} años');
  print('${delegado.nombre}: ${delegado.edad} años');
  print('${intercambio.nombre}: ${intercambio.edad} años\n');

  // 4. Crear matrícula
  final matriculaDAM = Matricula(
    anio: 2026,
    alumnos: [alumno1, delegado, intercambio],
    curso: dam2,
  );

  print(matriculaDAM);

  // 5. Demostración de Carga Síncrona vs Asíncrona
  print('--- CARGA DE CURSOS DESDE API ---');

  // Mock de respuesta JSON para comprobar funcionamiento sin depender de servidor real
  const String mockApiResponse = '''[
    {"codigo": "ASIR-1", "nombre": "Admin. Sistemas Informáticos", "descripcion": "Redes y Hardware"},
    {"codigo": "DAM-1", "nombre": "Desarrollo Multiplataforma 1º", "descripcion": "Bases de datos y Java"},
    {"codigo": "DAW-1", "nombre": "Desarrollo Web 1º", "descripcion": "HTML, CSS y JS"}
  ]''';

  // Síncrona pura:
  final List<Curso> cursosSync = CursoService.cargarCursosSincronoDesdeJson(mockApiResponse);
  print('Cursos cargados síncronamente: ${cursosSync.length}');
  for (var c in cursosSync) {
    print('  - $c');
  }

  // Asíncrona con .then:
  List<Curso> listaAsincrona = [];
  CursoService.cargarCursosConThen(listaAsincrona, alFallar: (e) {
    print('Nota: El endpoint simulado falló como era de esperar, pero el método está implementado correctamente.');
  });
}
