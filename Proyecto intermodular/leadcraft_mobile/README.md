# 🚀 LeadCraft AI - Aplicación Móvil (Flutter / Dart)

Proyecto de aplicación móvil multiplataforma (Android, Web y Desktop) desarrollado con **Flutter 3.x / Dart** para el Proyecto Intermodular de 2º DAM.

---

## 📱 Estructura de la Aplicación

La aplicación implementa fielmente los 4 módulos funcionales definidos en el Hito 1:

- **🗺️ Módulo 1: Explorador de Leads & Auditoría Express (`lib/screens/explore_screen.dart`)**
  - Mapa interactivo con vector rendering (`CustomPainter`), pins con estados de salud digital.
  - Filtros por sector comercial (Peluquerías/Barberías, Talleres mecánicos, Fisioterapia/Salud).
  - Cálculo del **Score de Salud Digital (45%)** y detección de carencias críticas (sin web propia, sin citas 24/7).

- **🤖 Módulo 2: Generador IA y Previsualización Web (`lib/screens/generator_screen.dart`)**
  - Simulación de generación asistida con IA (Gemini API) a partir del perfil de Google Maps.
  - Visualización del sitio web generado en tiempo real.
  - Widget interactivo de reserva de citas (elección de servicio, fecha y hora).

- **💬 Módulo 3: Propuesta Comercial & Handoff WhatsApp (`lib/screens/proposal_screen.dart`)**
  - Comparativa de valor *Antes vs Después*.
  - Desglose del plan de servicio mensual para PYMEs (39 €/mes).
  - Guion de contacto personalizado con enlace a la demo funcional y botón de apertura directa en WhatsApp.

- **📊 Módulo 4: Panel de Control del Negocio (`lib/screens/merchant_dashboard_screen.dart`)**
  - Panel simplificado para el comerciante local (ej. *Barbería Clásica*).
  - Indicadores clave (Citas de hoy, facturación estimada, captación fuera de horario).
  - Agenda interactiva con cambio de estados (*Confirmada*, *Completada*) y llamada directa.
  - Formulario modal para registrar citas presenciales o telefónicas manuales.

---

## 🛠️ Requisitos e Instalación

### Requisitos previos
- Flutter SDK 3.24+ (instalado en tu equipo).
- Google Chrome, Microsoft Edge o emulador Android / dispositivo físico conectado.

### Cómo ejecutar la aplicación

Abre una terminal en esta carpeta y ejecuta:

```bash
# 1. Ejecutar en el navegador web (Google Chrome)
flutter run -d chrome

# 2. Ejecutar como aplicación de escritorio Windows nativa
flutter run -d windows

# 3. Ejecutar en emulador o móvil Android conectado
flutter run -d android
```

Para verificar que el código cumple con los estándares de calidad de Dart y Flutter:
```bash
flutter analyze
```
*(Resultado actual: `No issues found!`)*
