# Memorix 💊⚡🏃
> **Asistente Móvil de Tratamientos Farmacológicos y Rehabilitación Muscular Guiada**  
> *Proyecto Intermodular — 2º DAM (Curso 2026/2027)*  
> **Alumno:** Kevin Muñoz Córcoles ([Kaik180](https://github.com/Kaik180))

---

## 🎨 1. Identidad Visual y Sistema de Contrastes

El nombre de la aplicación es **Memorix**. La imagen y el logotipo combinan dos conceptos clave del proyecto:
- **Isotipo:** Una pastilla/cápsula unida a pistas de circuitos electrónicos, representando la unión entre la salud/medicación y la tecnología móvil al servicio de la memoria.
- **Sistema de Contrastes:** Cuenta con cuatro combinaciones cromáticas de alto contraste (fondo oscuro, blanco, azul eléctrico y verde menta), pensadas para cumplir los estándares de accesibilidad visual y facilitar la lectura a personas mayores o con principios de Alzheimer.

![Sistema de Contrastes Memorix](contrastes.png)
*Figura 1: Logotipo y variantes de contraste de Memorix.*

---

## 📌 2. Resumen del Proyecto

**Memorix** es una propuesta de aplicación móvil multiplataforma (Android e iOS) diseñada para resolver dos problemas habituales del día a día:
1. **Los olvidos y confusiones con los medicamentos** en personas mayores, pacientes polimedicados o con problemas de memoria temprana.
2. **El abandono de los ejercicios de rehabilitación física en casa**, proporcionando rutinas sencillas y guiadas para fortalecer músculos dañados por sobrecargas, dolores de espalda o traumatismos.

---

## 🚨 3. Problema o Necesidad Detectada

- **¿Qué ocurre?** Muchos tratamientos no funcionan bien porque el paciente se olvida de tomar las pastillas a su hora o duda de si ya las ha tomado. Además, los prospectos tienen letra diminuta y palabras difíciles de comprender. Por otro lado, cuando una persona sufre una lesión muscular o dolor de espalda, las hojas con ejercicios que da el médico o fisioterapeuta se acaban perdiendo o no se sabe bien cómo hacer la postura, por lo que se dejan de hacer.
- **¿A quién afecta?** 
  - Personas de edad avanzada que toman varias pastillas al día.
  - Pacientes con fases iniciales de Alzheimer o deterioro cognitivo leve.
  - Cuidadores y familiares que viven preocupados por controlar las tomas de sus seres queridos.
  - Personas de cualquier edad en recuperación de una lesión o con dolores musculares.
- **¿Por qué debería mejorarse?** Un error con medicamentos para la tensión o el azúcar puede acabar en urgencias, y una rehabilitación mal hecha puede hacer que una lesión se cronifique. Usando el móvil podemos sustituir los papeles por avisos hablados y vídeos de ejercicios, ayudando a la autonomía del paciente y apoyando los objetivos **ODS 3 (Salud y Bienestar)** y **ODS 10 (Reducción de las Desigualdades)**.

---

## 📱 4. Solución Digital

Una aplicación móvil con interfaz sencilla y botones grandes (**"Modo Fácil"**) que incluye:
- **Alarmas con Locución:** Avisos sonoros que leen en voz alta qué medicamento toca y cómo tomarlo.
- **Confirmación con Aviso a Cuidadores:** Botón grande para registrar la toma. Si pasan 20 minutos sin confirmarse, se manda una alerta al móvil del familiar.
- **Módulo de Fisioterapia y Ejercicios:** Rutinas de ejercicios por zonas (hombros, cuello, espalda, piernas) con temporizador y explicaciones visuales.

![Prototipo de Interfaz Memorix](mockup_memorix.jpg)
*Figura 2: Pantalla de alarma médica con audio (izquierda) y sesión guiada de ejercicios musculares (derecha).*

---

## ⚡ 5. Tabla de Funcionalidades Principales

| Funcionalidad | Descripción |
| :--- | :--- |
| **Perfiles de Paciente y Cuidador** | Modo fácil para el usuario y vinculación con el móvil del familiar para supervisión a distancia. |
| **Alarmas con Locución por Voz** | Avisos sonoros que leen en voz alta el nombre del medicamento, dosis y consejos de toma. |
| **Confirmación de Toma y Registro** | Botón táctil grande para marcar la pastilla como tomada y guardar la hora exacta. |
| **Aviso de Seguridad al Cuidador** | Envío automático de alerta al familiar si pasan 20 minutos sin confirmación de la toma. |
| **Ejercicios Musculares Guiados** | Rutinas visuales para dolores o traumatismos con temporizador, series y descansos. |
| **Modo Contraste Accesible** | Paleta de colores contrastados pensada para personas mayores o con problemas de visión. |

---

## 🚀 6. Mejoras Futuras

1. **Visión Artificial con la Cámara Frontal:** Comprobar la postura del usuario mientras hace los ejercicios de rehabilitación delante del móvil para corregir fallos y evitar lesiones.
2. **Conexión con Pulseras Inteligentes:** Avisar de las tomas mediante vibración en la muñeca y detectar caídas accidentales.
3. **Escaneo de Cajas de Medicamentos:** Añadir tratamientos automáticamente enfocando la caja con la cámara.

---

## 📂 7. Entregables del Repositorio

- 📄 [`Tarea0_Memorix_Kevin.docx`](./Tarea0_Memorix_Kevin.docx): Documento oficial en Word (portada con logo + 2 páginas de contenido, Calibri 14pt títulos, Calibri 12pt texto, interlineado 1.5, cabecera, pie con número dinámico, índice enlazable, tabla de funcionalidades, fuentes y enlaces).
- 📊 [`Tarea0_Memorix_Presentacion.pptx`](./Tarea0_Memorix_Presentacion.pptx): Presentación en PowerPoint de exactamente 3 diapositivas visuales (Problema, Solución y Valor Añadido).
- 🎨 [`contrastes.png`](./contrastes.png): Imagen oficial del logotipo y contrastes de Memorix.
- 📱 [`mockup_memorix.jpg`](./mockup_memorix.jpg): Prototipo visual de la interfaz de la aplicación.
- ⚙️ [`generate_word.py`](./generate_word.py): Script en Python para construir el documento Word.
- ⚙️ [`generate_slides.py`](./generate_slides.py): Script en Python para construir la presentación PowerPoint.

---

## 📚 8. Fuentes Consultadas

- [Organización Mundial de la Salud (OMS) — Informe de adherencia a tratamientos](https://www.who.int/es/publications/i/item/9241545992)
- [Sociedad Española de Geriatría y Gerontología (SEGG) — Guía sobre polimedicación](https://www.segg.es)
- [Naciones Unidas — ODS 3: Salud y Bienestar](https://www.un.org/sustainabledevelopment/es/health/)
