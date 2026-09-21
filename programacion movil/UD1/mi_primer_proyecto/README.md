# Mi Primer Proyecto con Flutter (2º DAM)

Este proyecto corresponde a la primera práctica del módulo de **Programación Móvil / Desarrollo de Interfaces** (Ciclo Formativo de Grado Superior de Desarrollo de Aplicaciones Multiplataforma - DAM).

## 🚀 Requisitos Previos

- Flutter SDK (versión 3.x o superior) configurado en el PATH.
- Android Studio y Android SDK (API 34/35/36/37) con Android SDK Command-line Tools instalado.
- Emulador de Android configurado o dispositivo físico con Depuración USB habilitada.

## 🛠️ Modificaciones Realizadas sobre la Plantilla Base

Siguiendo las indicaciones de la Unidad 01:
1. **Modificación del título de la barra superior**:
   - `title: 'Exemple d\'aplicació amb Flutter'`
2. **Modificación del texto informativo**:
   - `'Has fet tap al botó el següent nombre de vegades:'`
3. **Cambio de la paleta cromática (Material 3)**:
   - `colorScheme: ColorScheme.fromSeed(seedColor: Colors.amberAccent)`
4. **Comprobación de Stateful Hot Reload**:
   - Se verifica que al incrementar el contador y pulsar la tecla `r` en la terminal tras modificar estilos, el valor del contador se preserva íntegro en memoria.

## 📱 Ejecución del Proyecto

1. Abrir terminal en la raíz del proyecto:
   ```bash
   cd mi_primer_proyecto
   ```
2. Obtener dependencias:
   ```bash
   flutter pub get
   ```
3. Listar dispositivos disponibles:
   ```bash
   flutter devices
   ```
4. Lanzar la aplicación en modo depuración (JIT con Hot Reload):
   ```bash
   flutter run
   ```
5. Comandos interactivos en ejecución:
   - `r`: **Hot Reload** (recarga rápida en caliente preservando estado).
   - `R`: **Hot Restart** (reinicio en caliente reinicializando estado).
   - `q`: Salir de la ejecución.
