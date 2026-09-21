# MEMORIA TÉCNICA DE PRÁCTICAS
## Unidad 01: Instalación, Configuración del Entorno Flutter y Primer Proyecto Multiplataforma

---

**Ciclo Formativo:** Formación Profesional de Grado Superior en Desarrollo de Aplicaciones Multiplataforma (2º DAM)  
**Módulo Profesional:** Programación Móvil / Desarrollo de Interfaces  
**Curso Académico:** 2026-2027  
**Sistema Operativo del Entorno:** Microsoft Windows 11 / 10 (x64)  
**Autor:** Kevin  
**Fecha:** Septiembre de 2026  

---

## 1. Introducción y Fundamentos del Desarrollo Multiplataforma

### 1.1. Contexto: Desarrollo Nativo frente a Multiplataforma
En el desarrollo de software móvil tradicional, la creación de aplicaciones requería programar de forma independiente para cada sistema operativo objetivo utilizando sus tecnologías específicas (*desarrollo nativo*):
- **Android**: Java o Kotlin junto con el SDK de Android y Gradle.
- **iOS / macOS**: Objective-C o Swift junto con Xcode y Cocoa Touch.

Aunque el enfoque nativo ofrece el máximo rendimiento y acceso directo e inmediato a todas las APIs del hardware, presenta importantes inconvenientes para las empresas: duplicación de costes, necesidad de mantener dos equipos de desarrollo especializados, desfase temporal en el lanzamiento de nuevas características y dificultad para sincronizar la lógica de negocio.

Para resolver este desafío han surgido diversas aproximaciones multiplataforma (*cross-platform*):

| Paradigma | Tecnologías Representativas | Mecanismo de Ejecución | Ventajas | Inconvenientes |
| :--- | :--- | :--- | :--- | :--- |
| **Web Responsive** | HTML5, CSS3, JavaScript | Navegador web móvil estándar | Código 100% único, sin instalación | Sin acceso profundo a hardware, menor fluidez |
| **Híbridas (WebView)** | Apache Cordova, Ionic | Aplicación web empaquetada dentro de un componente `WebView` nativo | Facilidad de desarrollo con frameworks web (Angular, React, Vue) | Sobrecarga de rendimiento debida al puente JS-WebView, experiencia no 100% nativa |
| **Progressive Web Apps (PWAs)** | Service Workers, Web App Manifest | Navegador con capacidades de caché y acceso a ciertas APIs | Instalables sin pasar por tiendas, ligeras | Restricciones de integración en iOS y limitaciones de sensores avanzados |
| **Compiladas / Puente Nativo** | React Native, NativeScript | Motor JavaScript que controla widgets nativos del sistema | Buen aspecto visual nativo | Cuello de botella en el puente (*bridge*) entre JS y el hilo nativo |
| **Renderizado Directo Multiplataforma** | **Flutter** (Google) | Código Dart compilado a código máquina nativo con motor gráfico propio (Skia / Impeller) | **Rendimiento nativo real (60/120 fps)**, UI idéntica y consistente en todas las plataformas, Stateful Hot Reload | Mayor tamaño inicial del binario |

### 1.2. ¿Qué es Flutter y por qué Dart?
**Flutter** es un SDK y framework de código abierto creado por Google en 2017. A diferencia de otras soluciones, Flutter no utiliza los widgets del sistema operativo ni delega en un `WebView`. En su lugar, Flutter incluye su propio motor gráfico de alto rendimiento (**Skia** o el moderno **Impeller**), dibujando cada píxel directamente en la pantalla del dispositivo mediante la GPU.

El lenguaje elegido por Google para Flutter es **Dart** (creado en 2011), debido a características arquitectónicas esenciales:
1. **Compilación dual**:
   - **JIT (Just-In-Time)** en modo desarrollo: Permite la recarga en caliente con conservación del estado en memoria (**Stateful Hot Reload**), acelerando radicalmente el ciclo de diseño y depuración.
   - **AOT (Ahead-Of-Time)** en modo release: Compila el código directamente a código máquina ARM o x86 optimizado, garantizando un arranque ultrarrápido y ejecuciones sin caídas de frames.
2. **Modelo reactivo basado en Widgets**: En Flutter, *absolutamente todo es un widget* (desde un botón hasta el padding o la alineación). Se diferencian principalmente dos tipos:
   - `StatelessWidget`: Componentes inmutables cuyo estado visual no cambia a lo largo del tiempo.
   - `StatefulWidget`: Componentes que mantienen un objeto `State` dinámico, permitiendo redibujar la interfaz cuando los datos cambian mediante llamadas a `setState()`.

---

## 2. Instalación y Configuración de Android Studio y Android SDK

Para poder compilar y desplegar aplicaciones en el ecosistema Android, Flutter requiere disponer de las herramientas del SDK de Android. La forma estándar y más completa de obtenerlas es mediante la instalación de **Android Studio**.

### 2.1. Descarga e Instalación de Android Studio
1. Se accede a la web oficial de desarrolladores de Android: `https://developer.android.com/studio`.
2. Se descarga el instalador oficial para Windows (`android-studio-...-windows.exe`).
3. Durante el proceso de instalación, se selecciona la ruta deseada en el equipo. En nuestro caso, la instalación se ha estructurado en una unidad dedicada:
   - **Ruta de Android Studio:** `D:\aplicaciones`
   - **Ruta del Android SDK:** `%LOCALAPPDATA%\Android\Sdk` (ej. `C:\Users\kevin\AppData\Local\Android\Sdk`)
4. Al abrir Android Studio por primera vez, el asistente de bienvenida descarga e inicializa los paquetes esenciales:
   - `Android SDK Platform` (versiones API 34 a 37).
   - `Android SDK Build-Tools`.
   - `Android SDK Platform-Tools` (que incluye el binario `adb.exe`).
   - `Android Emulator`.

### 2.2. Instalación de Android SDK Command-line Tools (Componente Crítico)
Por defecto, las versiones modernas de Android Studio no instalan las herramientas de línea de comandos requeridas por Flutter. Si este paso se omite, `flutter doctor` alertará con un error del tipo `Android toolchain - develop for Android devices (Android SDK version ...) [!] Android SDK is missing command line tools`.

Para solucionarlo:
1. En la pantalla inicial de Android Studio (*Welcome to Android Studio*), pulsar en **More Actions** (o en el menú superior *Tools*) y abrir el **SDK Manager**.
2. Ir a la pestaña **SDK Tools**.
3. Marcar la casilla **Android SDK Command-line Tools (latest)**.
4. Pulsar **Apply** y confirmar la descarga e instalación.

### 2.3. Variables de Entorno del Sistema
Para que tanto la consola como las extensiones del editor encuentren las herramientas de Android desde cualquier ubicación, se configuran las siguientes variables de entorno:
- `ANDROID_HOME`: `C:\Users\kevin\AppData\Local\Android\Sdk`
- En la variable `Path` del sistema/usuario se añaden:
  - `%ANDROID_HOME%\platform-tools`
  - `%ANDROID_HOME%\cmdline-tools\latest\bin`
  - `%ANDROID_HOME%\emulator`

### 2.4. Aceptación de Licencias de Android
Una vez instaladas las herramientas de línea de comandos, es obligatorio aceptar las licencias de uso de Google mediante el siguiente comando en PowerShell:
```powershell
flutter doctor --android-licenses
```
Se van confirmando los términos pulsando `y` (yes) en cada una de las licencias mostradas hasta completar la validación.

---

## 3. Instalación y Verificación de Flutter SDK

### 3.1. Requisitos Previos (Git y Entorno)
Flutter depende estrechamente del sistema de control de versiones **Git** para descargar paquetes, resolver dependencias y gestionar sus propios canales de actualización.
- En sistemas Windows se requiere disponer de Git en el PATH (instalable vía `Git for Windows` o mediante el cliente integrado de GitHub Desktop ubicado en `AppData\Local\GitHubDesktop\app-...\resources\app\git\cmd`).
- Se requiere PowerShell 5.0 o superior (disponible de forma nativa en Windows 10/11).

### 3.2. Descarga y Ubicación Recomendada de Flutter
1. Se descarga el archivo comprimido del Flutter SDK (canal `stable`) desde la web oficial `https://docs.flutter.dev/get-started/install/windows/mobile`.
2. **Recomendación clave de instalación en Windows:** Se debe extraer en una carpeta sin espacios, sin caracteres especiales y que no requiera privilegios elevados de Administrador (evitar terminantemente carpetas como `C:\Program Files\`). Las rutas ideales son:
   - `C:\src\flutter`
   - `D:\flutter`
3. Se añade la subcarpeta `bin` de Flutter a la variable de entorno `Path` del usuario:
   ```text
   C:\src\flutter\bin
   ```

### 3.3. Diagnóstico Exhaustivo con `flutter doctor`
Una vez configurado el PATH, se abre una terminal nueva y se ejecuta el comando de diagnóstico:
```bash
flutter doctor -v
```

La salida detallada evalúa cada subsistema:
1. **Flutter**: Comprueba la versión instalada del SDK, canal activo (`stable`), versión del motor Dart y versión de framework.
2. **Android toolchain**: Valida la localización del Android SDK, la presencia de `platform-tools`, `build-tools`, `cmdline-tools` y el estado de aceptación de las licencias.
3. **Chrome - develop for the web**: Detecta el navegador Google Chrome para depuración web.
4. **Visual Studio (Desktop)**: Opcional, necesario únicamente si se desean compilar ejecutables nativos Win32 de escritorio en C++.
5. **Android Studio**: Detecta la instalación del IDE (en nuestro caso en `D:\aplicaciones`), verificando su versión de Java interna (`jbr`) y plugins instalados.
6. **VS Code**: Comprueba la presencia del editor y sus extensiones de soporte.
7. **Connected devices**: Lista los dispositivos físicos, emuladores y navegadores listos para recibir ejecuciones.

### 3.4. Extra: Gestión Avanzada de Versiones con FVM (Flutter Version Manager)
En entornos profesionales o académicos donde distintos proyectos exigen versiones concretas de Flutter, se puede emplear **FVM**:
- Instalación global desde Dart:
  ```bash
  dart pub global activate fvm
  ```
- Instalación de una versión específica del SDK:
  ```bash
  fvm install 3.38.7 --setup
  ```
- Fijación de la versión para el proyecto actual:
  ```bash
  cd mi_proyecto
  fvm use 3.38.7
  ```
  Esto crea el archivo de configuración `.fvm/fvm_config.json`, garantizando reproducibilidad absoluta entre compañeros de equipo.

---

## 4. Configuración del Editor de Código: VS Code frente a Android Studio

A la hora de programar en Flutter, los dos editores de referencia recomendados oficialmente por Google son **Visual Studio Code** y **Android Studio**.

### 4.1. Análisis Comparativo

| Criterio | Visual Studio Code (Opción Ligera) | Android Studio (Opción Completa) |
| :--- | :--- | :--- |
| **Consumo de Memoria RAM** | ~250 MB - 450 MB (Muy bajo) | ~2.5 GB - 4.0 GB (Elevado) |
| **Tiempo de Inicio** | Prácticamente instantáneo (1-2 seg) | Pesado (15-30 seg indexando proyectos) |
| **Filosofía** | Editor de código modular ampliable mediante extensiones | IDE integral específico para desarrollo móvil nativo y Kotlin |
| **Gestión de Emuladores** | Requiere comandos o seleccionar dispositivo en la barra | Interfaz visual directa integrada (*Device Manager*) |
| **Herramientas de Perfilado** | Enlaza con Flutter DevTools en navegador | DevTools integrado + Profilers nativos de memoria/CPU |
| **Recomendación de uso** | **Ideal para el día a día**, portátiles con recursos ajustados (8-16 GB RAM) | Ideal cuando se requiere modificar código nativo Java/Kotlin o depurar Gradle complejo |

### 4.2. Configuración en Visual Studio Code
Para transformar VS Code en un entorno de desarrollo Flutter de primer nivel:
1. Abrir la vista de Extensiones (`Ctrl+Shift+X`).
2. Instalar las extensiones esenciales:
   - **Flutter** (Dart Code): Proporciona integración de comandos, ejecución, depuración con puntos de interrupción, vista de árbol de widgets e inspección en vivo.
   - **Dart**: Provee análisis estático, autocompletado, linting y formateo de código (se instala automáticamente junto con Flutter).
3. Extensiones recomendadas para mejorar la productividad:
   - **Pubspec Assist**: Permite añadir dependencias en `pubspec.yaml` mediante la paleta de comandos sin tener que consultar manualmente las versiones en `pub.dev`.
   - **Awesome Flutter Snippets**: Añade atajos para generar esqueletos de código instantáneos (`stless` para widgets sin estado y `stful` para widgets con estado).
   - **Error Lens**: Resalta errores y advertencias en la misma línea del código en tiempo real.
4. Flujo de trabajo rápido:
   - Abrir la paleta de comandos con `Ctrl+Shift+P`.
   - Escribir `Flutter: New Project` para iniciar el asistente interactivo.
   - En la esquina inferior derecha de la barra de estado se puede hacer clic en el nombre del dispositivo para conmutar entre emuladores, navegadores web o dispositivos físicos.

### 4.3. Configuración en Android Studio
Si se opta por utilizar Android Studio como editor principal:
1. Abrir Android Studio y acceder a **Settings** (icono de engranaje) > **Plugins**.
2. En la pestaña *Marketplace*, buscar e instalar el plugin **Flutter**.
3. El instalador solicitará instalar también el plugin **Dart** como dependencia requerida; aceptar y reiniciar el IDE.
4. Tras el reinicio, en la pantalla principal aparecerá la opción **New Flutter Project**.
5. Al pulsarla, se indica la ruta donde se encuentra instalado el Flutter SDK (`Flutter SDK path`).

---

## 5. Creación, Estructura y Modificación del Primer Proyecto con Flutter

### 5.1. Creación del Proyecto
La creación de un proyecto Flutter puede realizarse desde el asistente del editor o directamente a través de la interfaz de línea de comandos (CLI), siendo esta última la más potente y configurable:
```bash
flutter create --org com.ies.dam mi_primer_proyecto
```

Si únicamente deseamos generar el código para plataformas concretas (por ejemplo Android y Web), optimizando espacio en disco, se utiliza la opción `--platforms`:
```bash
flutter create --platforms android,web mi_primer_proyecto
```

> **Norma de nomenclatura:** El nombre del proyecto debe escribirse estrictamente en formato `snake_case` (letras minúsculas y números separados por guiones bajos), evitando mayúsculas o caracteres especiales para garantizar compatibilidad entre sistemas de archivos.

### 5.2. Estructura de Ficheros y Directorios del Proyecto

```text
mi_primer_proyecto/
├── android/              # Proyecto nativo Android (Gradle, AndroidManifest.xml, MainActivity)
├── ios/                  # Proyecto nativo iOS (Xcode workspace, Podfile, Info.plist)
├── web/                  # Contenedor web (index.html, manifest.json)
├── windows/              # Runner nativo para plataforma de escritorio Windows en C++
├── lib/                  # NÚCLEO DEL PROYECTO: Código fuente en Dart
│   └── main.dart         # Punto de entrada de la aplicación y lógica de widgets
├── test/                 # Pruebas unitarias y de integración de widgets
├── pubspec.yaml          # Fichero manifiesto: dependencias, fuentes tipográficas e imágenes
├── pubspec.lock          # Registro estricto de las versiones exactas instaladas
├── analysis_options.yaml # Reglas de estilo y directivas del linter de Dart
└── README.md             # Documentación descriptiva del repositorio
```

### 5.3. Código del Proyecto Modificado (`lib/main.dart`)
Siguiendo las instrucciones del enunciado de la unidad didáctica, se ha modificado la aplicación de ejemplo del contador para personalizar los textos, cambiar el esquema de colores de la interfaz (Material 3) y verificar el comportamiento del estado en caliente:

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mi Primer Proyecto Flutter - DAM2',
      debugShowCheckedModeBanner: false, // Desactiva la etiqueta 'DEBUG' en la esquina superior
      theme: ThemeData(
        // Modificación del tema visual mediante semilla de color personalizada
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.amberAccent),
        useMaterial3: true,
      ),
      // Título modificado en la cabecera
      home: const MyHomePage(title: 'Exemple d\'aplicació amb Flutter'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  void _resetCounter() {
    setState(() {
      _counter = 0;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Reiniciar comptador',
            onPressed: _resetCounter,
          ),
        ],
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              const Icon(
                Icons.flutter_dash,
                size: 80,
                color: Colors.amber,
              ),
              const SizedBox(height: 24),
              // Texto localizado modificado según las directrices de la práctica
              const Text(
                'Has fet tap al botó el següent nombre de vegades:',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w500,
                ),
              ),
              const SizedBox(height: 16),
              Text(
                '$_counter',
                style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                      color: Colors.amber.shade900,
                      fontWeight: FontWeight.bold,
                      fontSize: 48,
                    ),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Incrementar',
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

### 5.4. Stateful Hot Reload frente a Hot Restart
Durante la ejecución en depuración con `flutter run`:
- **Stateful Hot Reload (tecla `r`)**: Inyecta los cambios del código fuente Dart directamente en la máquina virtual (Dart VM) en ejecución. El árbol de widgets se reconstruye de inmediato (en menos de 500 ms) **conservando exactamente el valor actual del estado** (`_counter`). Si el usuario había pulsado el botón 7 veces, el número 7 continúa en pantalla tras alterar estilos, colores o tipografías.
- **Hot Restart (tecla `R`)**: Reinicia la aplicación completa en la máquina virtual, restableciendo las variables y el estado inicial (`_counter = 0`), pero sin la sobrecarga de recompilar el binario nativo ni reinstalar el APK.
- **Compilación AOT de Producción**:
  ```bash
  flutter build apk --release
  ```
  Genera el archivo `build/app/outputs/flutter-apk/app-release.apk`, compilado de forma anticipada sin la máquina virtual de depuración, optimizado en tamaño y con máxima tasa de refresco.

---

## 6. Conexión y Ejecución en Emuladores

El uso de dispositivos virtuales permite simular múltiples resoluciones de pantalla y versiones del sistema operativo sin necesidad de hardware físico.

### 6.1. Emulador Oficial de Android Studio (AVD)
1. **Creación de un AVD**:
   - En Android Studio, pulsar en **Device Manager** (o *Virtual Device Manager*).
   - Pulsar el botón **+ Create Virtual Device**.
   - Elegir un perfil de hardware representativo (por ejemplo, *Pixel 7* o *Medium Phone*).
   - Seleccionar la imagen de sistema deseada (por ejemplo, *Android 13 / Tiramisu* o *Android 14 / UpsideDownCake*, con ABI `x86_64` y APIs de Google).
   - Finalizar el asistente configurando la memoria RAM asignada (mínimo 2048 MB) y almacenamiento interno.
2. **Aceleración por Hardware**:
   - En Windows es fundamental contar con la característica de virtualización habilitada en BIOS/UEFI (Intel VT-x o AMD-V) y la plataforma de hipervisor de Windows activada.
3. **Gestión desde Línea de Comandos**:
   - Listar emuladores disponibles:
     ```bash
     flutter emulators
     ```
   - Iniciar un emulador concreto sin abrir el entorno gráfico de Android Studio:
     ```bash
     flutter emulators --launch Pixel_7_API_34
     ```
   - Lanzar la aplicación directamente sobre el emulador iniciado:
     ```bash
     flutter run
     ```

### 6.2. Emulador Alternativo: Genymotion Desktop
**Genymotion** es una solución de emulación basada en hipervisores (VirtualBox o QEMU) reconocida en el sector por su ligereza y fluidez en equipos con tarjetas gráficas dedicadas.
1. **Registro y Licencia**:
   - Se crea una cuenta en el portal de Genymotion y se descarga el instalador correspondiente para Windows.
   - En el primer arranque, tras introducir las credenciales, se selecciona la opción **Personal Use** (licencia gratuita para fines educativos y personales).
2. **Creación del Dispositivo**:
   - En la ventana principal, hacer clic en **+ Create**.
   - Se selecciona el modelo de dispositivo (por ejemplo, *Google Pixel 5*) y la versión del sistema (*Android 13*).
   - Se configuran los procesadores y la memoria acorde a las capacidades del PC anfitrión.
   - Se descarga la imagen y se inicia pulsando el botón **Play**.
3. **Detección y Enlace con Flutter**:
   - Genymotion expone una interfaz TCP/IP a través de ADB.
   - Al ejecutar `flutter devices`, el emulador aparece automáticamente reconocido como dispositivo conectado:
     ```text
     Google Pixel 5 (mobile) • 192.168.56.102:5555 • android-x64 • Android 13 (API 33)
     ```
   - La aplicación se lanza con total normalidad mediante `flutter run`.

---

## 7. Conexión y Despliegue en Dispositivo Físico Real

Aunque los emuladores son muy cómodos para el diseño preliminar, probar en hardware físico real es fundamental por múltiples motivos:
- **Rendimiento genuino**: El procesador ARM del móvil y su GPU renderizan la interfaz sin la sobrecarga de la virtualización x86.
- **Acceso fidedigno a sensores**: Cámara de alta resolución, GPS satelital, giróscopo, Bluetooth Low Energy, lector biométrico de huellas y comportamiento real del consumo de batería.
- **Detección de problemas de usabilidad**: Ergonomía real de toques táctiles, legibilidad en exteriores y comportamiento bajo conectividad de datos móviles reales.

### 7.1. Configuración Previa del Dispositivo Android
Para habilitar la comunicación entre el ordenador y el smartphone es necesario desbloquear el modo de depuración:
1. **Activar Opciones de Desarrollador**:
   - Ir a **Ajustes** > **Información del teléfono** (o *Acerca del dispositivo*).
   - Localizar el apartado **Número de compilación** (*Build number*).
   - Tocar **7 veces consecutivas** sobre esta opción hasta que el sistema muestre el aviso: *"¡Ya eres desarrollador!"*.
2. **Habilitar Depuración por USB**:
   - Volver al menú principal de Ajustes y acceder al nuevo apartado **Opciones de desarrollador** (habitualmente dentro de *Sistema* o *Ajustes adicionales*).
   - Activar la casilla **Depuración por USB** (*USB Debugging*) y aceptar el diálogo de advertencia de seguridad.

### 7.2. Conexión por Cable USB
1. Conectar el smartphone al puerto USB del ordenador.
2. En la pantalla del móvil aparecerá una ventana emergente: *“¿Permitir depuración por USB desde este ordenador?”*. Marcar la casilla **“Permitir siempre desde este ordenador”** y pulsar **Aceptar**.
3. Abrir PowerShell y verificar que ADB reconoce el terminal:
   ```powershell
   adb devices
   ```
   Salida esperada:
   ```text
   List of devices attached
   RFCW81ABCD0123    device
   ```
   *(Si aparece `unauthorized`, revisar la pantalla del teléfono para confirmar el diálogo de confianza RSA).*
4. Comprobar que Flutter detecta el dispositivo:
   ```powershell
   flutter devices
   ```
5. Lanzar la aplicación especificando el identificador del dispositivo físico:
   ```powershell
   flutter run -d RFCW81ABCD0123
   ```

> **Resolución de problemas:** Si el comando `adb devices` no lista ningún terminal, verificar que el cable USB soporte transferencia de datos (muchos cables baratos son únicamente de carga) y que en la notificación USB de Android esté seleccionado el modo *Transferencia de archivos / MTP*.

### 7.3. Conexión Inalámbrica (ADB over Wi-Fi)
A partir de Android 11, es posible depurar de forma totalmente inalámbrica sin necesidad de mantener el cable conectado:
1. Asegurarse de que el ordenador y el smartphone están conectados a la **misma red Wi-Fi**.
2. En Android Studio, abrir el **Device Manager** y pulsar en la pestaña **Pair Devices Using Wi-Fi**.
3. En el teléfono móvil, acceder a *Opciones de desarrollador* > *Depuración inalámbrica* > *Vincular dispositivo con código QR*.
4. Escanear con la cámara del teléfono el código QR presentado en la pantalla del ordenador.
5. Una vez vinculado, `flutter devices` mostrará el terminal bajo un identificador del tipo `adb-...-tcp`. La aplicación puede ejecutarse con `flutter run` con idéntica experiencia de recarga en caliente.

### 7.4. Espejo y Control del Dispositivo en el PC con `scrcpy` (Device Mirroring)
Para demostraciones en clase, exposiciones o grabación de tutoriales, la herramienta de código abierto **`scrcpy`** es el estándar indiscutible de la industria:
- **Ventajas:** No requiere instalar ninguna aplicación en el móvil, funciona a través del propio túnel ADB con una latencia mínima (35-70 ms), ofrece resolución nativa y permite controlar el smartphone directamente con el ratón y el teclado del ordenador.
- **Uso básico:**
  ```bash
  scrcpy
  ```
- **Modos avanzados de gran utilidad:**
  ```bash
  # Mantener la ventana siempre visible en primer plano y la pantalla del móvil despierta:
  scrcpy --always-on-top --stay-awake

  # Mostrar toques físicos en pantalla (ideal para grabar vídeos explicativos):
  scrcpy --show-touches

  # Grabar una demostración de la aplicación en formato MP4 de alta calidad:
  scrcpy --record demo_mi_primer_proyecto.mp4
  ```

---

## 8. Conclusiones y Valoración Personal

1. **Robustez del Ecosistema Flutter:** La arquitectura de Flutter basada en renderizado directo sobre lienzo gráfico elimina los problemas históricos de fragmentación visual entre distintas marcas de dispositivos Android y versiones de sistema.
2. **Productividad con Stateful Hot Reload:** La capacidad de modificar la interfaz, fuentes y colores en `main.dart` y observar el resultado de forma instantánea sin perder el valor de las variables de estado en memoria supone un incremento de productividad extraordinario respecto al desarrollo nativo tradicional con Gradle.
3. **Equilibrio de Herramientas:** La combinación de **Visual Studio Code** como editor ágil de programación junto con las herramientas del **Android SDK** (emulador oficial y `scrcpy` para terminales físicos) proporciona un entorno de trabajo potente, eficiente en consumo de recursos y profesional para el desarrollo a lo largo de todo el curso de 2º DAM.
