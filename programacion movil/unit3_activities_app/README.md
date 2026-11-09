# Unit 3 Activities App • PMDM DAM2

Aplicación completa e interactiva desarrollada en **Flutter 3** y **Dart** que compila y resuelve todas las actividades prácticas, conceptos y patrones de navegación explicados en la **Unidad 3 (Interfaces de Usuario y Navegación en Flutter)** del temario oficial de PMDM.

---

## 📱 Contenido del Proyecto y Actividades Resueltas

El proyecto implementa un cuadro de mando central (*Dashboard*) con acceso interactivo a cada una de las 5 secciones de la Unidad 3:

| Apartado | Pantalla | Descripción y Conceptos Clave |
| :--- | :--- | :--- |
| **3.1 Introducción a Widgets** | `CounterActivityScreen` | **Actividad oficial resuelta:** Contador con 3 botones: Incrementar (`+`), Decrementar (`-`) y Reiniciar (`0`). Interfaz declarativa, `Scaffold`, `StatefulWidget`, `setState()` y disposición con `Row` en `floatingActionButtonLocation.centerFloat`. |
| **3.2 Operaciones Asíncronas** | `FutureBuilderActivityScreen` | Implementación rigurosa de `FutureBuilder<T>` con `RefreshIndicator` (*Pull-to-refresh*). **Buenas prácticas del curso:** inicialización en `initState()` para prevenir el anti-patrón de re-ejecución en cada `build()`, control exhaustivo de `ConnectionState`, `snapshot.hasError` con reintentos y selector para simular caídas de red. |
| **3.3 Navegación y Formularios** | `NavigationFormActivityScreen` & `NavigationDetailScreen` | Formularios validados mediante `GlobalKey<FormState>`, controladores de texto (`TextEditingController`), navegación LIFO con `Navigator.push`, paso de parámetros tipados y captura asíncrona de la respuesta mediante `final res = await Navigator.push(...)` y `Navigator.pop(context, resultado)`. |
| **3.4 Widgets Nav & Diálogos** | `NavWidgetsDialogsActivityScreen` | Diseño responsivo con `NavigationBar` (móviles) y `NavigationRail` (tablets / pantallas anchas), menú lateral con `NavigationDrawer`, pestañas con `DefaultTabController` / `TabBar` / `TabBarView`. Catálogo interactivo de diálogos: `AlertDialog`, `SimpleDialog` y `Dialog` personalizado. |
| **3.5 GoRouter & Hero** | `GoRouterHeroActivityScreen` & `HeroDetailScreen` | Navegación declarativa avanzada con `go_router`, rutas dinámicas con parámetros de URL (`/detail/:id`), paso de objetos `extra` y animaciones de transición compartida **Hero Animations** con tags compartidos. |

---

## 🛠️ Arquitectura y Estructura del Código

```text
unit3_activities_app/
├── lib/
│   ├── main.dart                               # Punto de entrada con MaterialApp.router y temas M3 (claro/oscuro)
│   ├── models/
│   │   └── item_model.dart                     # Modelo inmutable con fromJson, toJson y copyWith
│   ├── routes/
│   │   └── app_router.dart                     # Configuración central de GoRouter y rutas dinámicas
│   └── screens/
│       ├── home_dashboard_screen.dart          # Hub principal con tarjetas de actividad y resumen
│       ├── counter_activity_screen.dart        # Unidad 3.1: Contador extendido
│       ├── future_builder_activity_screen.dart # Unidad 3.2: FutureBuilder & Pull-to-refresh
│       ├── navigation_form_activity_screen.dart# Unidad 3.3: Formulario y envío de datos
│       ├── navigation_detail_screen.dart       # Unidad 3.3: Pantalla receptora y retorno asíncrono
│       ├── nav_widgets_dialogs_activity_screen.dart # Unidad 3.4: NavigationBar/Rail/Tabs/Dialogs
│       ├── gorouter_hero_activity_screen.dart  # Unidad 3.5: Catálogo GoRouter
│       └── hero_detail_screen.dart             # Unidad 3.5: Detalle con animación Hero
├── test/
│   └── widget_test.dart                        # Suite de pruebas unitarias verificadas
└── pubspec.yaml                                # Dependencias (Flutter SDK, go_router)
```

---

## 🚀 Cómo Ejecutar la Aplicación

1. **Abrir una terminal en la carpeta del proyecto:**
   ```bash
   cd "programacion movil/Programas/unit3_activities_app"
   ```

2. **Comprobar dependencias y análisis estático:**
   ```bash
   flutter pub get
   flutter analyze
   flutter test
   ```

3. **Lanzar en la plataforma que prefieras:**
   - **En Windows Escritorio:**
     ```bash
     flutter run -d windows
     ```
   - **En Navegador Web (Chrome/Edge):**
     ```bash
     flutter run -d chrome
     ```
   - **En Emulador o Dispositivo Android:**
     ```bash
     flutter run -d android
     ```
