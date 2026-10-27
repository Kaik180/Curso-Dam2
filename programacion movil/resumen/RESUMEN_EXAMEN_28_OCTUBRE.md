# 🎯 Guía Definitiva de Preparación: Examen PMDM (28 de Octubre)

Documento completo de estudio y simulacro para el examen de la Unidad 1 de **Programación Multimedia y Dispositivos Móviles (2º DAM)**.

---

## 📊 Estructura de Puntuación (10 Puntos)

| Bloque | Contenido | Ponderación | Puntos |
|---|---|:---:|:---:|
| **Bloque 1** | Teoría sobre Flutter (Definición, PWAs, ficheros de configuración, JIT vs AOT) | 20% | **2.0 pts** |
| **Bloque 2** | Teoría sobre Dart (Null Safety `?` y `!`, argumentos nombrados `{}`, `final` vs `const`) | 20% | **2.0 pts** |
| **Bloque 3** | Práctica: Modelado de datos (Asociación de Estudiantes, POO, getter `edad`, API REST) | 40% | **4.0 pts** |
| **Bloque 4** | Práctica: 6 Preguntas de Programación Funcional y Colecciones | 20% | **2.0 pts** |
| **Total** | | **100%** | **10.0 pts** |

---

## 🚀 Bloque 1: Flutter Teórico (20% - 2 Puntos)

### 1. ¿Qué es Flutter?
- **Definición:** Es un **SDK (Software Development Kit)** y framework de código abierto creado por **Google en 2017** para desarrollar aplicaciones multiplataforma a partir de un **único código base**.
- **Lenguaje:** **Dart** (creado por Google en 2011).
- **Motor / Núcleo:** Desarrollado en **C++** con su propio motor de renderizado (**Skia** o **Impeller**).
- **Diferencia clave con otros frameworks:** **No usa WebViews ni componentes nativos OEM**. Flutter toma el control del lienzo (*Canvas*) y dibuja directamente cada píxel en pantalla a 60 o 120 FPS.

### 2. Comparativa de Enfoques y ¿Qué es una PWA?

| Tipo de Aplicación | Tecnologías | Rendimiento | Acceso a Hardware | Características |
|---|---|:---:|:---:|---|
| **Nativa** | Kotlin/Java (Android), Swift (iOS) | Máximo | 100% directo | Código específico para cada SO; coste doble de desarrollo. |
| **Web Responsive** | HTML5, CSS3, JavaScript | Bajo | Limitado | Corre dentro del navegador web del dispositivo. |
| **Híbrida** (Ionic, Cordova) | Web envuelta en un **WebView** | Medio | Puenteado por plugins | Es un navegador camuflado sin barra de navegación. |
| **PWA (Progressive Web App)** | Web + **Service Workers** + Manifest | Medio-Alto | Notificaciones, caché offline | Explicada abajo. |
| **Compilada (Flutter)** | Dart + Canvas nativo | Casi nativo | 100% mediante plugins | Mismo código compilado a binario nativo (ARM/x86). |

> [!IMPORTANT]
> **Definición de PWA para el examen:**  
> Una **PWA (Progressive Web Application)** es una aplicación web enriquecida que, mediante **Service Workers** (scripts que se ejecutan en segundo plano en el navegador de forma independiente a la página) y un archivo `manifest.json`, proporciona características propias de una app nativa:
> 1. Capacidad de **funcionar sin conexión (offline)** gracias a la caché local.
> 2. Envío y recepción de **notificaciones push** del sistema.
> 3. Capacidad de **instalarse en la pantalla de inicio** sin tener que pasar por Google Play Store ni Apple App Store.

### 3. Archivos de Configuración de un Proyecto
- **`pubspec.yaml`**: Archivo principal de configuración en formato YAML. Define:
  - Metadatos del proyecto (`name`, `description`, `version`).
  - Restricciones del SDK de Dart/Flutter (`environment`).
  - Librerías y dependencias externas (`dependencies: http: ^1.2.2`).
  - Dependencias de desarrollo (`dev_dependencies: lints: ^4.0.0`).
  - Recursos estáticos (*assets* como imágenes, fuentes y ficheros de datos).
- **`pubspec.lock`**: Archivo generado automáticamente por el gestor `pub`. Registra la **versión exacta y fija** descargada de cada librería y sus dependencias transitivas, garantizando que todo el equipo trabaje con el mismo entorno reproducible.
- **`analysis_options.yaml`**: Configuración de análisis estático del código (`dart analyze`). Aplica paquetes de reglas oficiales como `lints` o `flutter_lints` para detectar errores potenciales, convenciones de estilo y advertencias de compilación.
- **`.metadata`**: Archivo oculto generado por las herramientas de Flutter para rastrear el tipo de proyecto y plugins instalados.
- **`.gitignore`**: Lista de archivos y carpetas que Git no debe rastrear (como `build/`, `.dart_tool/`).

### 4. Compilación en Flutter: JIT vs AOT
- **JIT (Just-In-Time):** Utilizado durante la fase de **desarrollo (debug)**. El código se compila dinámicamente sobre la marcha en la máquina virtual, lo que hace posible el **Stateful Hot Reload** (aplicar cambios en milisegundos sin perder el estado ni reiniciar la app).
- **AOT (Ahead-Of-Time):** Utilizado para **producción (release)**. El código Dart se compila antes de ejecutarse directamente a código máquina nativo (binario ARM o x86), ofreciendo arranque instantáneo y máximo rendimiento.

---

## 🛡️ Bloque 2: Dart Teórico (20% - 2 Puntos)

### 1. Sound Null Safety: Operadores `?` y `!`
Dart implementa **Sound Null Safety** (seguridad estricta ante nulos): por defecto, ningún tipo puede almacenar `null`.

- **El operador `?` (Declaración Nullable):** Permite explícitamente que una variable o propiedad admita el valor `null`.
  ```dart
  String? nombre; // Puede ser un String o puede valer null
  int? edad;
  ```
- **El operador `!` (Null Assertion Operator):** Se utiliza para obligar a tratar una variable nullable como no-nullable. Le garantiza al compilador: *"Te aseguro que este valor no es null en este momento"*.
  ```dart
  String? textoNulo;
  String seguro = textoNulo!; // ⚠️ Si en tiempo de ejecución resulta ser null, arroja TypeError (NullError).
  ```
- **Operadores de nulos relacionados:**
  - `??` (Null Coalescing): `final actual = valor ?? "Por defecto";` (devuelve la izquierda si no es nulo, o la derecha si es nulo).
  - `??=` (Asignación condicional): `variable ??= 10;` (asigna 10 solo si la variable vale `null`).
  - `?.` (Acceso seguro): `cadena?.length` (si `cadena` es `null`, devuelve `null` sin lanzar excepción).

### 2. Argumentos Nombrados vs Posicionales

| Tipo de Argumento | Sintaxis en Función | Invocación | Características |
|---|---|---|---|
| **Posicional Obligatorio** | `void fn(int a, String b)` | `fn(1, "DAM")` | El orden es estricto y todos son requeridos. |
| **Posicional Opcional** | `void fn(int a, [int b = 0])` | `fn(1)` o `fn(1, 2)` | Se definen con corchetes `[]`. |
| **Nombrado Opcional** | `void fn({String? id, int n = 1})` | `fn(n: 5, id: "A1")` | Se definen con llaves `{}`. El orden es indiferente. |
| **Nombrado Obligatorio** | `void fn({required String id})` | `fn(id: "A1")` | Llevan la palabra clave `required`. El orden es indiferente pero obligatorio nombrarlo. |

**¿Por qué se usan los argumentos nombrados en Flutter?**  
Porque mejoran drásticamente la legibilidad en componentes con decenas de propiedades configurables (como `Text`, `Container`, `Scaffold`), evitando confusiones de orden.

### 3. Diferencia entre `final` y `const`
- **`const` (Tiempo de compilación):** Se resuelve y congela en memoria **antes de que arranque el programa**. Es inmutable tanto en referencia como en contenido.
  ```dart
  const double pi = 3.14159;
  ```
- **`final` (Tiempo de ejecución):** Se inicializa **una sola vez cuando la línea se ejecuta**. Una vez asignada su referencia, no se puede reasignar.
  ```dart
  final DateTime ahora = DateTime.now(); // No se puede saber en compilación
  ```

---

## 🏛️ Bloque 3: Modelado Práctico - Asociación de Estudiantes (40% - 4 Puntos)

### Enunciado del Examen
- Asociación de estudiantes:
  - **`Estudiante`**: Almacena `nombre`, `apellido`, `dni`, `fechaNacimiento` (`DateTime`) y `curso` (`Curso`).
  - **`Delegado`** (subclase de `Estudiante`): Añade la propiedad `claseGestionada`.
  - **`EstudianteIntercambio`** (subclase de `Estudiante`): Añade `paisOrigen` y `duracionEstancia`.
  - **`Curso`**: Almacena `codigo`, `nombre` y `descripcion`.
  - **`Matricula`**: Almacena `anio`, una lista de alumnos (`List<Estudiante>`) y el `curso` (`Curso`).
- **Método GET `edad`:** Calcula y devuelve la edad del alumno usando `DateTime.now()`.
- **Carga de cursos desde API (`https://api.asociacion/cursos`):**
  - Primero de forma **asíncrona** (`.then` o `async/await`).
  - Después de forma **síncrona** (comportamiento secuencial con `await` o parseo síncrono local).

### Código Completo en Dart

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

// 1. CLASE CURSO
class Curso {
  final String codigo;
  final String nombre;
  final String descripcion;

  Curso({
    required this.codigo,
    required this.nombre,
    required this.descripcion,
  });

  // Constructor factoría para deserializar desde JSON
  factory Curso.fromJson(Map<String, dynamic> json) {
    return Curso(
      codigo: json['codigo'] ?? '',
      nombre: json['nombre'] ?? '',
      descripcion: json['descripcion'] ?? '',
    );
  }

  @override
  String toString() => '[$codigo] $nombre';
}

// 2. CLASE ESTUDIANTE (SUPERCLASE)
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

  // MÉTODO GET: Obtiene la edad usando DateTime.now()
  int get edad {
    final DateTime ahora = DateTime.now();
    int calculoEdad = ahora.year - fechaNacimiento.year;
    // Comprobamos si todavía no ha cumplido años este año
    if (ahora.month < fechaNacimiento.month ||
        (ahora.month == fechaNacimiento.month && ahora.day < fechaNacimiento.day)) {
      calculoEdad--;
    }
    return calculoEdad;
  }

  @override
  String toString() => '$nombre $apellido (DNI: $dni | Edad: $edad | Curso: ${curso.nombre})';
}

// 3. SUBCLASE DELEGADO (Hereda de Estudiante)
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

  @override
  String toString() => '${super.toString()} [DELEGADO de $claseGestionada]';
}

// 4. SUBCLASE ESTUDIANTE DE INTERCAMBIO (Hereda de Estudiante)
class EstudianteIntercambio extends Estudiante {
  final String paisOrigen;
  final String duracionEstancia;

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
  String toString() => '${super.toString()} [INTERCAMBIO: $paisOrigen ($duracionEstancia)]';
}

// 5. CLASE MATRÍCULA
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
}
```

### Métodos de Carga de Cursos desde la API

#### 1. Carga Asíncrona (Con `.then()` o `async/await`)
```dart
// Opción A: Con Future y .then() (no bloquea el hilo):
void cargarCursosAsyncConThen(List<Curso> listaDestino) {
  final url = Uri.parse('https://api.asociacion/cursos');
  http.get(url).then((response) {
    if (response.statusCode == 200) {
      final List rawJson = jsonDecode(utf8.decode(response.bodyBytes)) as List;
      listaDestino.clear();
      listaDestino.addAll(rawJson.map((e) => Curso.fromJson(e as Map<String, dynamic>)));
      print('Cursos cargados asíncronamente: ${listaDestino.length}');
    }
  }).catchError((error) => print('Error asíncrono: $error'));
}

// Opción B: Con async / await:
Future<List<Curso>> cargarCursosAsync() async {
  final response = await http.get(Uri.parse('https://api.asociacion/cursos'));
  if (response.statusCode == 200) {
    final List rawJson = jsonDecode(utf8.decode(response.bodyBytes)) as List;
    return rawJson.map((e) => Curso.fromJson(e as Map<String, dynamic>)).toList();
  }
  throw Exception('Error en respuesta HTTP: ${response.statusCode}');
}
```

#### 2. Carga Síncrona (Comportamiento secuencial con `await` o parseo en memoria)
```dart
// Comportamiento "síncrono" (espera secuencial con await según el temario):
Future<void> cargarCursosSincrono(List<Curso> listaDestino) async {
  print('Iniciando espera secuencial...');
  final response = await http.get(Uri.parse('https://api.asociacion/cursos')); // Pausa aquí
  if (response.statusCode == 200) {
    final List rawJson = jsonDecode(utf8.decode(response.bodyBytes)) as List;
    listaDestino.clear();
    listaDestino.addAll(rawJson.map((e) => Curso.fromJson(e as Map<String, dynamic>)));
    print('Carga secuencial completada.');
  }
}

// Carga síncrona pura a partir de una cadena JSON (sin peticiones de red):
List<Curso> parsearCursosSincrono(String jsonString) {
  final List rawJson = jsonDecode(jsonString) as List;
  return rawJson.map((e) => Curso.fromJson(e as Map<String, dynamic>)).toList();
}
```

---

## ⚡ Bloque 4: Programación Funcional y Colecciones (20% - 2 Puntos)

### Colecciones base de prueba:
```dart
final List<int> numeros = [-3, 2, -1, 0, 4, 23, 17, -90, 8, 12];
final List<String> palabras = ['Dart', 'Flutter', 'DAM', 'Asociacion', 'Examen', 'Movil'];
final List<Map<String, dynamic>> productos = [
  {'nombre': 'Portátil', 'precio': 1200.0, 'categoria': 'Electrónica', 'stock': 5},
  {'nombre': 'Ratón', 'precio': 15.0, 'categoria': 'Accesorios', 'stock': 25},
  {'nombre': 'Teclado', 'precio': 85.0, 'categoria': 'Accesorios', 'stock': 0},
  {'nombre': 'Monitor', 'precio': 350.0, 'categoria': 'Electrónica', 'stock': 8},
];
```

### 1. Filtrado con `where`
> **Pregunta:** *"Obtener una nueva lista con los números que sean pares y estrictamente mayores que cero."*
```dart
final paresPositivos = numeros.where((n) => n > 0 && n % 2 == 0).toList();
// Resultado: [2, 4, 8, 12]
```

### 2. Transformación con `map`
> **Pregunta:** *"Convertir cada palabra a mayúsculas indicando además su número de caracteres."*
```dart
final palabrasMayus = palabras.map((p) => '${p.toUpperCase()} (${p.length} chars)').toList();
// Resultado: [DART (4 chars), FLUTTER (7 chars), DAM (3 chars), ...]
```

### 3. Reducción con `reduce`
> **Pregunta:** *"Calcular el valor máximo de la lista numérica usando únicamente la función `reduce`."*
```dart
final maximo = numeros.reduce((actualMax, n) => n > actualMax ? n : actualMax);
// Resultado: 23
```

### 4. Acumulación con tipo con `fold`
> **Pregunta:** *"Calcular el valor total en inventario de todos los productos (precio * stock) usando `fold`."*
```dart
final totalInventario = productos.fold<double>(
  0.0,
  (acumulador, item) => acumulador + ((item['precio'] as double) * (item['stock'] as int)),
);
// Resultado: 9175.00
```

### 5. Comprobación booleana con `every` y `any`
> **Pregunta:** *"Comprobar si existe algún producto sin stock (`stock == 0`) y si todos los productos tienen un precio superior a 0."*
```dart
bool hayAgotados = productos.any((p) => p['stock'] == 0);          // true
bool todosTienenPrecio = productos.every((p) => p['precio'] > 0);  // true
```

### 6. Encadenamiento funcional combinado (`where` + `map` + `join`)
> **Pregunta:** *"Obtener una cadena de texto separada por comas con los nombres de productos de 'Electrónica' que tengan stock disponible."*
```dart
final nombresEnStock = productos
    .where((p) => p['categoria'] == 'Electrónica' && (p['stock'] as int) > 0)
    .map((p) => p['nombre'] as String)
    .join(', ');
// Resultado: "Portátil, Monitor"
```

---

## 🛠️ Comandos de Prueba en la Terminal

Dentro de la carpeta `programacion movil/resumen`:
```bash
# 1. Ejecutar el caso práctico completo de la Asociación de Estudiantes:
dart run practica_asociacion_estudiantes.dart

# 2. Ejecutar las 6 preguntas de programación funcional:
dart run seis_preguntas_funcionales.dart

# 3. Comprobar que no existen errores de análisis:
dart analyze
```
