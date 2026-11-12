# PROPUESTA DE TRABAJO EN LA NUBE PARA UNA PEQUEÑA EMPRESA
## Plan Integral de Implementación de Cloud Computing para EduPlus Academy

- **Nombre del Alumno:** Kevin
- **Rol en el Proyecto:** Rebeca (Cofundadora y docente de EduPlus Academy)
- **Destinatario Interno:** Samuel (Cofundador y docente de EduPlus Academy)
- **Módulo:** Digitalización Aplicada al Sistema Productivo (Tema 4: Cloud Computing y Edge Computing)
- **Curso:** 2º DAM (Desarrollo de Aplicaciones Multiplataforma)
- **Formato del Documento Oficial (.docx / .pdf):** Portada, Tabla de Contenido, Títulos y Subtítulos, Texto en Calibri 11, justificado, interlineado 1.5.

---

## Tabla de Contenido
1. Introducción y Diagnóstico de la Situación Actual en EduPlus Academy
   1.1. Presentación de EduPlus Academy: Historia, Equipo y Oferta Formativa
   1.2. Diagnóstico del Modelo Tradicional Local: Problemas Operativos y Riesgos de Pérdida de Datos
   1.3. El Dilema Estratégico entre Rebeca y Samuel: Transformación vs. Resistencia al Cambio
2. Tarea 1: ¿Qué tipo de servicio en la nube va a ser necesario?
   2.1. ¿Para qué funciones concretas se utilizará la nube en EduPlus Academy?
   2.2. Comparativa entre el Alojamiento Tradicional Local de la Academia y el Modelo Cloud
   2.3. ¿Qué modelo de nube (IaaS, PaaS o SaaS) será más adecuado? Justificación Técnica
   2.4. Niveles de Nube (Pública, Privada, Híbrida) y Rol del Edge/Fog/Mist Computing en el Aula
3. Tarea 2: Análisis de Ventajas e Inconvenientes (Argumentario para Convencer a Samuel)
   3.1. Enfoque del Argumentario: Empatía, Datos Reales y Mitigación de Temores
   3.2. Tabla Oficial de la Tarea 2: Cambios Económicos, en los Empleados y Medioambientales
   3.3. Desarrollo Razonado de Respuestas a las Objeciones de Samuel (Seguridad, Caídas y Curva)
4. Tarea 3: Estudio Comparativo de Proveedores de Servicios en la Nube
   4.1. Análisis de los Tres Proveedores Líderes: Microsoft Azure, Google Cloud e IBM Cloud
   4.2. Tabla Oficial de la Tarea 3: Resumen de Servicios Relevantes para EduPlus Academy
   4.3. Toma de Decisiones: Selección de la Arquitectura Ganadora y Estrategia de Redundancia
5. Plan de Implementación, Hoja de Ruta y Presupuesto Estimado
   5.1. Fases de Implantación Gradual sin Interrumpir las Clases (Plan de 4 Semanas)
   5.2. Presupuesto Económico y Retorno de la Inversión (ROI) para EduPlus Academy
6. Valoración Final y Conclusiones del Proyecto
7. Defensa del Proyecto: Presentación Ejecutiva y Enlace de Acceso

---

## Resumen de las Tareas Desarrolladas

### Tarea 1: ¿Qué tipo de servicio va a ser necesario?
1. **Funciones concretas de la nube en EduPlus Academy:**
   - **Almacenamiento de materiales de clase (PDF, vídeos, presentaciones):** Repositorio centralizado en unidades compartidas por niveles (Primaria, ESO, Bachillerato, PAU, Cambridge, Técnicas de Estudio).
   - **Gestión de horarios, reservas de tutorías y asistencia:** Calendarios sincronizados en la nube para aulas y grupos reducidos, portal de reserva online de tutorías para familias y control digital de asistencia.
   - **Comunicación con familias y estudiantes:** Sustitución del WhatsApp personal por canales institucionales seguros (Classroom / Teams / Correo corporativo) cumpliendo el RGPD.
   - **Registro de notas, tareas y evaluaciones:** Cuaderno de evaluación en la nube, exámenes autocorregibles (Forms) y boletines trimestrales automatizados en PDF.
   - **Acceso remoto para estudiantes y profesorado:** Disponibilidad 24/7 desde cualquier ordenador, tablet o smartphone con conexión a Internet.
   - **Copias de seguridad de informes y documentos importantes:** Autoguardado cada 5 segundos (caso Sonia frente a Marcos del Tema 4), historial de versiones y backups cifrados contra fallos mecánicos, errores humanos o virus.
   - **Plataforma para clases online y trabajos colaborativos:** Entorno LMS unificado con videollamadas HD, pizarra digital y edición simultánea de documentos.
2. **Modelo de nube más adecuado (IaaS, PaaS o SaaS):**
   - Se selecciona el modelo **SaaS (Software as a Service)** sobre nube pública con enfoque híbrido de seguridad.
   - **Por qué:** Los 6 docentes de EduPlus Academy son especialistas en enseñanza, no administradores de sistemas (que requeriría **IaaS**, como *BinagorWorld*) ni desarrolladores de software (que requeriría **PaaS**, como *TorcalMet*). Con **SaaS** (como *DragonTel*), el proveedor gestiona toda la infraestructura, el mantenimiento, las actualizaciones y la ciberseguridad; las aplicaciones están listas para usar, la curva de aprendizaje es mínima y los planes educativos base tienen coste 0 €.

### Tarea 2: Ventajas e inconvenientes (Convencer a Samuel)
- **Cambios Económicos:** Sin inversión inicial en hardware (CAPEX 0), pago por uso escalable, ahorro en papel/tóner/electricidad y prevención de multas de la AEPD (hasta 60.000 € como en el caso de CC.OO.). Frente al temor de cuotas mensuales, las suites educativas (Google Workspace for Education / Microsoft 365 A1) son gratuitas o de coste simbólico (<25 €/mes en total), ahorrando más de 180 €/mes.
- **Cambios en los Empleados:** Trabajo colaborativo en tiempo real, autoguardado cada 5 segundos, facilidad de teletrabajo y fin del caos de WhatsApp. Frente al temor de Samuel sobre la formación o caídas de red (como el caso de DNS de AWS el 20 de octubre de 2025), se imparten 2 talleres prácticos de 45 min, se migra progresivamente y se activa el **Modo Sin Conexión (Offline)** más backup redundante.
- **Cambios Medioambientales:** Academia "Papel Cero", ahorro energético local y menos desplazamientos. Frente al consumo de los grandes *data centers*, Google, Microsoft e IBM operan con energía 100 % renovable y el procesamiento en la nube alarga años la vida útil de los ordenadores actuales de la academia sin generar basura electrónica (*e-waste*).

### Tarea 3: Estudio de proveedores
- **Microsoft Azure (+ Microsoft 365 Education):** Microsoft Teams para Educación, OneDrive, SharePoint, Office Online, Microsoft Bookings, Forms, Azure Backup, Azure Blob Storage y Microsoft Entra ID (referente en nube híbrida).
- **Google Cloud (+ Google Workspace for Education):** Google Classroom, Google Drive, Docs/Sheets/Slides, Google Meet, Calendar, Forms, Google Cloud Storage, Kubernetes Engine (GKE) y Cloud AI / Gemini Education.
- **IBM Cloud:** IBM Cloud Object Storage (backups inmutables de alta seguridad), IBM watsonx Assistant (chatbot IA 24/7 para familias), IBM Cloud Private / Red Hat OpenShift y Virtual Servers / Code Engine.

---

## Enlace a la Presentación
- **Archivo local y en repositorio:** [Presentacion_Cloud_EduPlus_Kevin.pptx](./Presentacion_Cloud_EduPlus_Kevin.pptx)
- **Informe en Word:** [Propuesta_Cloud_EduPlus_Kevin.docx](./Propuesta_Cloud_EduPlus_Kevin.docx)
- **Informe en PDF:** [Propuesta_Cloud_EduPlus_Kevin.pdf](./Propuesta_Cloud_EduPlus_Kevin.pdf)
