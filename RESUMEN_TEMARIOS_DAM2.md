# 📚 Resúmenes y Guía de Estudio Integral - 2º DAM
**Curso Académico:** 2026-2027  
**Centro:** IES Mutxamel / Generalitat Valenciana  
**Ciclo Formativo:** CFGS Desarrollo de Aplicaciones Multiplataforma (DAM)

---

## 📑 Índice de Contenidos
1. [Mapa General del Curso y Estado de las Materias](#mapa-general-del-curso)
2. [Sistema de Gestión Empresarial (SGE)](#1-sistema-de-gestión-empresarial-sge)
   - [UD00: Python 3 Básico para Odoo](#ud-00-python-3-básico-para-odoo)
   - [UD01 / UD02: Sistemas ERP - CRM - BI](#ud-01--ud-02-sistemas-erp---crm---bi)
   - [UD01 (Práctica) / UD03: Docker, Contenedores y Kubernetes](#ud-01-itinerario-práctico--ud-03-virtualización-docker-y-kubernetes)
   - [UD04: Implantación de un ERP en la Empresa](#ud-04-implantación-de-un-erp-en-la-empresa)
   - [UD05: Entorno de Desarrollo y Primer Módulo Odoo](#ud-05-entorno-de-desarrollo-y-primer-módulo-odoo)
   - [UD06: Desarrollo de Módulos: Modelo y Vista (ORM)](#ud-06-desarrollo-de-módulos-modelo-y-vista-orm)
   - [UD07: Lógica de Negocio, Herencia y Web Controllers](#ud-07-lógica-de-negocio-herencia-y-web-controllers)
   - [UD08: Cliente Web de Odoo (OWL)](#ud-08-cliente-web-de-odoo-owl)
3. [Programación Multimedia y Dispositivos Móviles (PMDM)](#2-programación-multimedia-y-dispositivos-móviles-pmdm)
   - [UNIT 01: Flutter & Dart - Desarrollo Multiplataforma](#unit-01-flutter--dart-desarrollo-multiplataforma)
4. [Digitalización Aplicada al Sistema Productivo](#3-digitalización-aplicada-al-sistema-productivo)
   - [Tema 1: Digitalización y Transformación Digital (IT / OT)](#tema-1-digitalización-y-transformación-digital-en-los-sistemas-productivos)
5. [Desarrollo de Interfaces (DIW)](#4-desarrollo-de-interfaces-diw)
   - [Guía Docente y Plan de Evaluación](#guía-docente-y-plan-de-evaluación)
   - [UT01: Accesibilidad y Guía de Estilos](#ut01-accesibilidad-y-guía-de-estilos)
6. [Proyecto Intermodular (2º DAM)](#5-proyecto-intermodular-2º-dam)
   - [Estructura, Metodología y Normas](#organización-y-metodología)
   - [Matriz de Requisitos Técnicos por Materia](#matriz-de-requisitos-técnicos-por-materia)
   - [Tarea 0: Precisión de Código y Mecanografía](#tarea-0-precisión-y-manejo-del-teclado)
7. [Asignaturas Pendientes de Carga de Material](#6-asignaturas-pendientes-de-material-específico)

---

## 🗺️ Mapa General del Curso

| Asignatura | Código / Horas | Docente de Referencia | Temarios Disponibles en el Repositorio |
| :--- | :---: | :--- | :--- |
| **Sistema de Gestión Empresarial (SGE)** | 100h | José Castillo / Sergi García | 🟢 **UD00 a UD08 completas** (Teoría, Docker, Odoo y Podcasts) |
| **Programación Móvil (PMDM)** | - | Adaptación Joamuran | 🟢 **UNIT 01 completa** (Flutter, Dart, Emuladores, CLI, FVM) |
| **Digitalización Aplicada** | - | Editorial Editex (2024) | 🟢 **Tema 1 completo** (Digitalización vs TD, IT/OT, ERPs, Ciberseguridad) |
| **Desarrollo de Interfaces (DIW)** | 0488 (166h) | Juan Sanz Moya | 🟢 **Presentación del Módulo** y **UT01** (Accesibilidad y Guía de Estilos) |
| **Proyecto Intermodular** | 100h (3h/sem) | Silvia Diánez Juan | 🟢 **Presentación oficial**, matriz transversal y **Tarea 0** |
| **Acceso a Datos (AD)** | - | - | 🟡 *Requisitos técnicos integrados en Proyecto Intermodular* |
| **Prog. Servicios y Procesos (PSP)** | - | - | 🟡 *Requisitos de concurrencia en Proyecto Intermodular* |
| **Sostenibilidad / Inglés / BD** | - | - | 🟡 *Lineamientos de eco-diseño y arquitectura integrados* |

---

## 1. Sistema de Gestión Empresarial (SGE)

Ubicación de archivos: [`Sistema gestion empresarial/UD1/ApuntesSistemasGestionEmpresarial`](file:///c:/Users/kevin/OneDrive/Documentos/GitHub/Curso-Dam2/Sistema%20gestion%20empresarial/UD1/ApuntesSistemasGestionEmpresarial)

> ℹ️ **Estructura del repositorio:**
> - En **castellano**: UD01 corresponde a teoría general de ERP-CRM-BI.
> - En **valenciano** (Prof. Sergi García): UD00 es Python, UD01 es Docker y UD02 es ERP-CRM-BI.

### UD 00: Python 3 Básico para Odoo
* **Propósito:** Base de programación para desarrollar módulos sobre el ORM de Odoo.
* **Contenidos clave:**
  * Sintaxis básica, tipado dinámico, colecciones (`list`, `tuple`, `dict`, `set`).
  * Estructuras de control de flujo (`if-elif-else`, `for`, `while`).
  * Manejo de funciones, argumentos posicionales y por clave (`*args`, `**kwargs`).
  * Programación Orientada a Objetos: clases, herencia, métodos mágicos (`__init__`, `__str__`).
  * Preparación del entorno de desarrollo y hoja de trucos (*Python 3 CheatSheet*).

### UD 01 / UD 02: Sistemas ERP - CRM - BI
* **Definiciones fundamentales:**
  * **ERP (*Enterprise Resource Planning*):** Software de gestión empresarial integrada. Centraliza los datos y la operativa de toda la organización (contabilidad, inventario, compras, ventas, RRHH) en una única base de datos.
  * **CRM (*Customer Relationship Management*):** Software de gestión de relaciones con clientes. Automatiza el ciclo comercial, preventa, seguimiento de clientes y campañas de marketing.
  * **BI (*Business Intelligence*):** Inteligencia de negocio. Herramientas de visualización y análisis de datos históricos y presentes para proyectar tendencias futuras y respaldar la toma de decisiones informadas.
* **Ventajas e Inconvenientes de un ERP:**
  * *Ventajas:* Única instalación y mantenimiento; base de datos unificada sin silos de información; modularidad mediante plugins/módulos; seguridad centralizada; informes de BI coherentes.
  * *Desventajas:* Coste inicial y tiempo de parametrización elevado; riesgo de sobredimensionamiento en pequeñas empresas; punto único de fallo (si se vulnera el sistema, peligra toda la información corporativa); resistencia de usuarios si la interfaz es compleja.
* **Desarrollo a medida vs. Parametrización/Personalización:**
  * El desarrollo desde cero es costoso, lento y arriesgado.
  * La opción recomendada es **personalizar un ERP existente** (como Odoo), aprovechando un motor estable y maduro adaptando módulos según necesidad.
* **Licencias de Software:**
  * *Privativas (SAP, Microsoft Dynamics 365, Oracle JD Edwards):* Alto coste recurrente y dependencia estricta del fabricante (*vendor lock-in*).
  * *Libres / Código Abierto (Odoo Community, OpenBravo, AbanQ):* Independencia técnica, código auditable y libertad para cambiar de proveedor de servicios.
* **Retos de Implantación:**
  * Problemas técnicos de infraestructura.
  * Migración y saneamiento de datos previos (duplicidades, codificaciones incoherentes).
  * Mentalidad directiva (hacer ver el ERP como inversión estratégica).
  * Resistencia de los empleados al cambio (solución: formación de calidad dentro de la jornada laboral y comunicación transparente).
* **Glosario Empresarial Básico:**
  * *Persona física vs. Persona jurídica:* La física (autónomo) responde con sus bienes personales; la jurídica (sociedades, fundaciones) responde con el patrimonio de la entidad.
  * *Facturas:* Completa (con todos los datos fiscales y desglose de IVA) vs. Simplificada o Ticket (datos reducidos) vs. Proforma (oferta o presupuesto previo, sin validez contable ni tributaria).
  * *Producción y Logística:* Línea de producción (secuencia operativa), Orden de producción (concreción de producto, fecha y cantidad), Stock/Inventario (existencias) y Logística (cadena de distribución).

### UD 01 (Itinerario Práctico) / UD 03: Virtualización, Docker y Kubernetes
* **Fundamentos de Docker:** Contenedores vs. máquinas virtuales (compartición de kernel del host, mayor ligereza y arranque instantáneo).
* **Elementos principales:** Imágenes (`docker pull`, `docker build`), Contenedores (`docker run`, `docker stop`, `docker ps`), Volúmenes para persistencia (`-v`) y Redes (`bridge`).
* **Despliegue con Docker Compose (`docker-compose.yml`):**
  * Orquestación de dos servicios dependientes: **Odoo 18** y **PostgreSQL**.
  * Variables de entorno (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`).
  * Mapeo de puertos (`8069:8069`) y montaje de volúmenes para el código personalizado de *addons*.
  * Diferencias entre configuraciones de desarrollo (recarga de código, modo depuración) y producción.
* **Kubernetes Comic:** Lectura conceptual sobre orquestación de contenedores en clústeres a gran escala (pods, deployments, autoescalado).

### UD 04: Implantación de un ERP en la Empresa
* Fases de implantación: consultoría inicial, diseño funcional, parametrización, migración de datos, pruebas de aceptación y puesta en marcha (*go-live*).
* Prácticas con persistencia real de datos en Odoo y respaldo de bases de datos.

### UD 05: Entorno de Desarrollo y Primer Módulo Odoo
* Estructura física de un módulo en Odoo:
  * Archivo descriptor `__manifest__.py` (nombre, versión, dependencias, ficheros de datos).
  * Fichero de inicialización `__init__.py`.
  * Carpetas estándar: `models/`, `views/`, `security/`, `controllers/`, `data/`, `static/`.
* Uso de la herramienta CLI de Odoo para scaffolding: `odoo-bin scaffold <nombre_modulo> <directorio>`.
* Ejemplos prácticos del repositorio: *Hola Mundo* y *Lista de Tareas*.

### UD 06: Desarrollo de Módulos: Modelo y Vista (ORM)
* **Modelos ORM (`models.Model`):**
  * Atributos de clase: `_name`, `_description`, `_order`.
  * Campos básicos: `fields.Char`, `fields.Text`, `fields.Integer`, `fields.Float`, `fields.Boolean`, `fields.Date`, `fields.Datetime`, `fields.Selection`.
  * Campos relacionales:
    * `Many2one`: relación muchos a uno (ej. pedido pertenece a un cliente).
    * `One2many`: relación uno a muchos (ej. un pedido contiene varias líneas).
    * `Many2many`: relación muchos a muchos (ej. artículos y etiquetas/categorías).
* **Vistas en XML:**
  * Vistas lista/árbol (`<list>` o `<tree>`): visualización tabular de registros.
  * Vistas formulario (`<form>`): alta y edición detallada, organizadas con `<sheet>`, `<notebook>`, `<page>`, `<group>`.
  * Vistas de búsqueda (`<search>`): filtros rápidos y agrupación (`group_by`).
  * Acciones de ventana (`ir.actions.act_window`) y elementos de menú (`<menuitem>`).

### UD 07: Lógica de Negocio, Herencia y Web Controllers
* **Herencia de modelos y vistas:** Extensión mediante `_inherit` para añadir campos o modificar comportamientos de módulos existentes sin alterar su código fuente.
* **Decoradores y Lógica:**
  * `@api.depends`: cálculo reactivo de campos computados (`compute='_compute_total'`).
  * `@api.onchange`: actualización de campos en la interfaz en tiempo real tras la interacción del usuario.
  * `@api.constrains`: validación estricta de datos en backend antes de guardar en la base de datos.
* **Controladores Web (`odoo.http.Controller`):**
  * Decorador `@http.route`: creación de rutas URL públicas o privadas.
  * Respuestas en HTML (renderizado de plantillas QWeb) o en formato JSON (APIs para conectar con apps móviles o clientes externos).

### UD 08: Cliente Web de Odoo (OWL)
* Arquitectura del frontend moderno de Odoo basada en **OWL (Odoo Web Library)**.
* Creación de componentes reactivos JavaScript, manejo de estado, templates XML en frontend y personalización de vistas complejas.

---

## 2. Programación Multimedia y Dispositivos Móviles (PMDM)

Ubicación de archivos: [`programacion movil/UD1/UNIT 01`](file:///c:/Users/kevin/OneDrive/Documentos/GitHub/Curso-Dam2/programacion%20movil/UD1/UNIT%2001)

### UNIT 01: Flutter & Dart - Desarrollo Multiplataforma
* **Paradigmas de desarrollo móvil:**
  * *Nativo:* Swift/Objective-C para iOS; Kotlin/Java para Android. Máxima integración hardware, pero obliga a programar y mantener dos bases de código distintas.
  * *Web Responsive:* HTML, CSS y JS en el navegador móvil. Bajo coste, pero sin acceso fluido a componentes del hardware.
  * *Híbridas (Ionic, Cordova):* Web enmarcada dentro de un WebView con estética nativa. Limitaciones de rendimiento.
  * *PWAs (Progressive Web Apps):* Tecnologías web con Service Workers para trabajo offline y notificaciones.
  * *Multiplataforma compilada (React Native, Flutter):* Una única base de código que se compila a código nativo de la plataforma destino (Android, iOS, Windows, macOS, Linux y Web).
* **¿Qué es Flutter?**
  * SDK de código abierto creado por Google en 2017.
  * Motor gráfico propio de renderizado en C++ (evita el puente o *bridge* JavaScript de otras soluciones).
  * Lenguaje **Dart** (creado por Google):
    * Compilación **JIT (*Just-In-Time*)**: usada en desarrollo para habilitar el *Stateful Hot Reload* (recarga casi instantánea del código sin perder el estado de la app).
    * Compilación **AOT (*Ahead-Of-Time*)**: usada al generar la versión de producción (*release*), compilando directamente a lenguaje máquina optimizado (ARM / x86).
* **Instalación y Configuración del Entorno:**
  * Comprobación del sistema con el comando de diagnóstico: `flutter doctor`.
  * Instalación de Android Studio: configuración de Android SDK, SDK Command-line Tools y licencias (`flutter doctor --android-licenses`).
  * Configuración en **Visual Studio Code**: extensiones oficiales de *Flutter* y *Dart*.
* **Emuladores y Dispositivos:**
  * Uso de emuladores ligeros con **Genymotion Desktop** (basados en VirtualBox/Hyper-V).
  * Conexión y depuración en dispositivos Android físicos por cable USB (activación de opciones de desarrollo y depuración USB).
  * Conexión inalámbrica a través de red local (*ADB over Wi-Fi*).
  * Visualización y control de la pantalla del terminal en el monitor del PC mediante **scrcpy**.
* **Gestión de Proyectos y CLI:**
  * Estructura estándar de un proyecto:
    * `lib/main.dart`: punto de entrada principal del código Dart.
    * `pubspec.yaml`: manifiesto del proyecto, gestión de dependencias, assets y fuentes.
    * `android/`, `ios/`, `web/`: proyectos nativos generados que envuelven la app.
  * Comandos habituales:
    * `flutter create nombre_app`
    * `flutter devices`
    * `flutter run` (teclas `r` para hot reload, `R` para hot restart, `q` para salir).
    * `flutter build apk`
* **Control de versiones con FVM (*Flutter Version Manager*):**
  * Permite instalar y alternar entre múltiples versiones del SDK de Flutter por proyecto para evitar incompatibilidades de dependencias (`fvm install <version>`, `fvm use <version>`).

---

## 3. Digitalización Aplicada al Sistema Productivo

Ubicación del archivo: [`digitalizacion-productivo/UD1/TEMA 1 - Digitalización aplicada al sistema productivo.pdf`](file:///c:/Users/kevin/OneDrive/Documentos/GitHub/Curso-Dam2/digitalizacion-productivo/UD1/TEMA%201%20-%20Digitalizaci%C3%B3n%20aplicada%20al%20sistema%20productivo.pdf)

### Tema 1: Digitalización y Transformación Digital en los Sistemas Productivos

#### 1. Digitalización vs. Transformación Digital
* **Digitalización:** Conversión de datos, documentos físicos en papel y procesos manuales a representaciones y formatos digitales. Su objetivo es la eficiencia operativa y la manipulación electrónica a corto plazo.
* **Transformación Digital:** Cambio profundo e integral en la estrategia, procesos y cultura de una organización que aprovecha la tecnología para reinventar el modelo de negocio y obtener ventajas competitivas sostenibles a largo plazo.
* **Plan de Digitalización en 6 fases:**
  1. *Diagnóstico y evaluación:* Análisis del estado actual de procesos y cultura.
  2. *Definición de objetivos:* Metas medibles y claras.
  3. *Alineación estratégica:* Coherencia con la visión de la empresa.
  4. *Asignación de recursos:* Financiación, tecnología y capacitación.
  5. *Gestión del cambio:* Estrategias para superar la resistencia de las personas.
  6. *Evaluación continua:* Métricas de efectividad y corrección de desviaciones.
* **Índice DESI (*Digital Economy and Society Index*):** Indicador de la Unión Europea que evalúa la conectividad, el capital humano digital, el uso de servicios públicos digitales y la integración de tecnologías en empresas (donde España ocupa posiciones destacadas en conectividad y servicios públicos).

#### 2. Implantación de Tecnología en la Empresa
* **Grado de integración:** Bajo (externalización o *outsourcing* para tareas puntuales) vs. Alto (equipos internos de desarrollo, mantenimiento de sistemas y analítica de datos).
* **Automatización:**
  * *Pros:* Incremento de productividad, eliminación de tareas repetitivas, minimización del error humano y liberación de personal para tareas estratégicas.
  * *Cons:* Inversión inicial considerable y riesgo de dependencia tecnológica.
* **Top 5 de sistemas ERP más utilizados en España:**
  1. *SAP Business One:* Líder robusto en medianas y grandes empresas.
  2. *Microsoft Dynamics 365:* Alta integración con el ecosistema Microsoft y flexibilidad en la nube.
  3. *Sage 200:* Amplia presencia tradicional en pymes españolas y solvencia contable/fiscal.
  4. *Odoo:* Destacado por su modelo de código abierto, modularidad y facilidad de personalización.
  5. *Oracle Cloud ERP / NetSuite:* Orientado a corporaciones globales de gran escala.
* **Cultura organizativa y Ciberseguridad:**
  * La resistencia al cambio se combate con comunicación clara, formación dentro del horario laboral y fomento de la innovación.
  * **Pirámide de Ciberseguridad:**
    * *Base:* Dispositivos y servicios especializados de protección.
    * *Cuerpo central:* Protocolos de seguridad y configuraciones de datos.
    * *Cúspide:* Formación y concienciación del empleado contra ataques de ingeniería social/phishing.

#### 3. Entornos IT y OT (Convergencia)
* **IT (*Information Technology* - Tecnología de la Información):**
  * Ámbito: Redes de oficinas, servidores corporativos, ERP, bases de datos y desarrollo de software.
  * Prioridad: Protección de datos (confidencialidad, integridad y disponibilidad).
* **OT (*Operational Technology* - Tecnología Operativa):**
  * Ámbito: Maquinaria de fábrica, líneas de ensamblaje, sensores, PLCs y sistemas SCADA.
  * Prioridad: Operaciones en tiempo real, seguridad física de operarios e indisponibilidad cero.
* **Convergencia IT-OT:** Integración de los datos generados en la planta de fabricación directamente con los sistemas de gestión (ERP/BI) para tomar decisiones operativas en tiempo real.

#### 4. Tecnologías de Digitalización en Planta y Negocio
* **En Planta (Operativo):** Automatización robótica, IoT y sensores, Gemelos Digitales (*Digital Twins* para simulación virtual de líneas físicas), Realidad Aumentada/Virtual (guiado en mantenimiento) y gestión inteligente de activos.
* **En Negocio (Empresarial):** Sistemas ERP, Inteligencia Artificial, Computación en la Nube (*Cloud Computing*), Analítica Avanzada (*Big Data*) y Blockchain para trazabilidad.

#### 5. Metamorfosis hacia la Empresa Digital Integral
Evolución escalonada: *Operaciones manuales tradicionales ➔ Integración digital de sistemas ➔ Automatización de tareas ➔ Análisis avanzado de datos ➔ Empresa digital ágil y competitiva*.

---

## 4. Desarrollo de Interfaces (DIW)

Ubicación de archivos: [`desarrollo de interfaces/UD1`](file:///c:/Users/kevin/OneDrive/Documentos/GitHub/Curso-Dam2/desarrollo%20de%20interfaces/UD1)

### Guía Docente y Plan de Evaluación
* **Profesor:** Juan Sanz Moya (`j.sanzmoya@edu.gva.es`).
* **Carga horaria:** 166 horas anuales (5 horas a la semana).
* **Unidades de Trabajo (UT) y Ponderación de Resultados de Aprendizaje (RA):**
  * **UT01. Diseño en Figma** (RA4) ➔ **6%** (2 semanas)
  * **UT02. Desarrollo en FlutterFlow I** (RA1) ➔ **25%** (8 semanas)
  * **UT03. Desarrollo en FlutterFlow II** (RA2, RA3, RA5) ➔ **45%** (6 semanas)
  * **UT04. Documentación** (RA6) ➔ **8%** (2 semanas)
  * **UT05. Testing** (RA8) ➔ **10%** (2 semanas)
  * **UT06. Distribución** (RA7) ➔ **6%** (2 semanas)
* **Criterios de calificación:**
  * En cada unidad: Examen teórico-práctico (**70%**) + Actividades y proyectos (**30%**).
  * Ambos apartados deben tener nota $\ge 5,0$.
  * Para aprobar el módulo es **obligatorio superar todos y cada uno de los RAs**. Si falla uno, el módulo completo queda no superado.
  * Pérdida de evaluación continua si se supera el 15% de faltas injustificadas.

### UT01: Accesibilidad y Guía de Estilos
* **Accesibilidad Digital:**
  * Desarrollar software comprensible y operable por cualquier usuario, incluyendo personas con limitaciones visuales, motoras o cognitivas (lectores de pantalla, uso exclusivo de teclado).
  * *Premisa fundamental:* «La accesibilidad no es un extra del diseño; no implementarla es un error del propio diseño».
* **Estándar WCAG (*Web Content Accessibility Guidelines*):**
  * **Nivel A:** Accesibilidad mínima recomendada solo para pruebas de concepto (PoC) o prototipos (MVP).
  * **Nivel AA (Estándar legal y profesional obligatorio):** Contraste suficiente de colores, navegación accesible por teclado, foco visible en campos interactivos, textos alternativos para imágenes (`alt`) y atributos ARIA mínimos.
  * **Nivel AAA:** Máximo grado de accesibilidad especializada.
* **Estructura de una Guía de Estilos:**
  * Documento maestro para mantener la coherencia visual independientemente del desarrollador que programe cada pantalla.
  * **1. Temática y Propósito:** Definir la identidad según el sector (tecnológico, sobrio/lujoso, cálido/artesanal).
  * **2. Logotipo y Variantes:** Definición del logotipo principal, versión monocroma/negativa y adaptaciones responsivas (isotipo).
  * **3. Paleta de Colores:** Máximo 4 a 5 colores. Evitar colores sobresaturados.
    * **Regla 60-30-10:**
      * **60%:** Color dominante/neutro (fondos, espacios amplios).
      * **30%:** Color secundario (tarjetas, cabeceras, menús).
      * **10%:** Color de acento (botones principales de acción *CTA*, enlaces, alertas).
    * Herramientas recomendadas: Coolors, Adobe Color.
  * **4. Tipografía y Jerarquía:**
    * Selección de fuentes legibles (Google Fonts).
    * Contraste estricto entre color de tipografía y fondo.
    * Jerarquía visual: títulos principales en negrita (*bold*), subtítulos medianos, párrafos en peso regular, espaciado adecuado de línea (`line-height`) y caracteres (`letter-spacing`).
  * **5. Iconografía e Imágenes:**
    * Iconos uniformes en grosor de trazo, tamaño y estilo de relleno (FontAwesome, SVGRepo, Google Material Symbols).
    * Fotografías e ilustraciones coherentes con la gama cromática y temática (Freepik, Pixabay).

---

## 5. Proyecto Intermodular (2º DAM)

Ubicación de archivos: [`Proyecto intermodular/UD1`](file:///c:/Users/kevin/OneDrive/Documentos/GitHub/Curso-Dam2/Proyecto%20intermodular/UD1)

### Organización y Metodología
* **Profesora responsable:** Silvia Diánez Juan (`s.dianezjuan@edu.gva.es`).
* **Dedica:** 100 horas totales (3 horas semanales: miércoles tarde y jueves tarde).
* **Marco legal:** Ley Orgánica 3/2022, Real Decreto 659/2023 y Orden 8/2025 de la Generalitat Valenciana.
* **Metodología activa basada en retos:** Resolución de un problema real planteado por el profesorado o empresas colaboradoras mediante aprendizaje colaborativo y tutorización continua.
* **Fases del proyecto:**
  1. *Planteamiento del reto:* Definición del problema y alcance.
  2. *Diseño del proyecto:* Arquitectura, herramientas y resultados de aprendizaje implicados.
  3. *Planificación por hitos:* Fechas límite, asignación de tareas y roles del equipo.
  4. *Ejecución:* Desarrollo técnico del software y documentación.
  5. *Seguimiento continuo:* Tutorización y control periódico de avances.
  6. *Presentación final:* Defensa pública obligatoria del proyecto ante tribunal.
* **Normas del aula:**
  * Asistencia obligatoria $\ge 85\%$ (con un 15% de faltas injustificadas se pierde la evaluación continua).
  * Puntualidad rigurosa (tolerancia máxima de retraso: 4 minutos).
  * Comunicaciones oficiales canalizadas por Webfamilia, Ítaca y correo corporativo `@edu.gva.es`.

### Matriz de Requisitos Técnicos por Materia
El proyecto de fin de ciclo no es una aplicación aislada, sino un sistema integrado donde cada módulo de 2º DAM evalúa requisitos específicos:

| Módulo Implicado | Requisitos Mínimos Exigidos en el Proyecto |
| :--- | :--- |
| **Acceso a Datos (AD)** | API backend funcional con endpoints **CRUD** completos sobre las entidades del modelo. Persistencia real en base de datos (**SQL o NoSQL**) con pruebas unitarias y de integración. Capa de acceso a datos limpia, autenticación/autorización y documentación de la API (OpenAPI/Swagger). |
| **Desarrollo de Interfaces (DIW)** | Frontend usable y accesible conforme al estándar **WCAG 2.1 AA** (contraste, navegación por teclado, foco visible, atributos ARIA). Diseño **responsivo mobile-first** con guía de estilos coherente. Arquitectura clara de rutas, validación exhaustiva de formularios y mensajes de error comprensibles. |
| **Prog. Multimedia y Móviles (PMDM)** | Desarrollo de una **aplicación móvil completa** (Android/iOS mediante Flutter). Casos de uso reales: autenticación, formularios, navegación fluida, persistencia local/remota e integración con la API desarrollada en Acceso a Datos. |
| **Prog. Servicios y Procesos (PSP)** | Implementación de **servicios concurrentes** (hilos, tareas asíncronas). Uso correcto de mecanismos de sincronización (**locks, semáforos**). Ejemplo: servidor concurrente que atienda múltiples clientes simultáneamente. |
| **Digitalización Aplicada (DA)** | Despliegue en **servicios en la nube (*Cloud*)**, almacenamiento y/o autenticación externa. Gestión de código fuente con **Git** (GitHub/GitLab) aplicando buenas prácticas de ramas (*branching*), issues, pull requests e integración continua (CI/CD). |
| **Sostenibilidad** | Criterios de **eco-diseño digital**: optimización y eficiencia del código para reducir el consumo energético de procesador y servidores, minimización de transferencias innecesarias de datos en red y uso responsable de recursos en la nube. |
| **Empresa e Iniciativa Emprendedora (EIE)** | Modelo de negocio, viabilidad del proyecto y memoria organizativa según indicaciones de la asignatura. |

### Tarea 0: Precisión y Manejo del Teclado
* Tarea diagnóstica inicial orientada a garantizar agilidad y precisión mecanográfica con el teclado al escribir código técnico: sintaxis JSON, consultas SQL con condiciones (`WHERE`, operadores de comparación), expresiones regulares, cadenas de conexión y caracteres especiales (`{}`, `[]`, `()`, `|`, `&`, `\`, `@`).

---

## 6. Asignaturas Pendientes de Material Específico

Actualmente las siguientes materias no contienen aún apuntes subidos en sus carpetas, pero sus líneas maestras ya están trazadas a través de los requisitos del Proyecto Intermodular:

* **Acceso a Datos:** Se centrará en la construcción de servicios backend, conexiones JDBC/Hibernate/Spring Boot o NodeJS, consultas optimizadas, ORMs y exposición de APIs seguras.
* **Programación de Servicios y Procesos:** Abarcará programación multihilo en Java/C, comunicación entre procesos mediante sockets de red, programación reactiva/asíncrona y seguridad en comunicaciones.
* **Sostenibilidad e Inglés Técnico:** Contenidos transversales orientados a la reducción de la huella de carbono digital y la redacción de documentación técnica profesional en inglés.

---

*Documento generado automáticamente a partir de los materiales del curso disponibles en el repositorio. Se actualizará conforme se incorporen nuevas unidades didácticas y tareas.*
