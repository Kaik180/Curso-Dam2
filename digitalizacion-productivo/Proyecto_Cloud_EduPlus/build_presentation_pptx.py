import os
import sys
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def create_presentation():
    prs = Presentation()
    # Formato panorámico Widescreen 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Paleta de colores corporativa (Azul Académico / Cloud + Morado y Verde para las tareas)
    C_DARK = RGBColor(18, 53, 91)        # #12355B Azul marino académico
    C_MID = RGBColor(30, 86, 138)        # #1E568A Azul medio cloud
    C_ACCENT = RGBColor(43, 122, 184)    # #2B7AB8 Azul cielo intenso
    C_PURPLE = RGBColor(123, 31, 162)    # #7B1FA2 Morado (Tarea 2)
    C_GREEN = RGBColor(78, 140, 43)      # #4E8C2B Verde (Tarea 3)
    C_TEXT = RGBColor(36, 36, 36)        # Gris carbón para lectura cómoda
    C_MUTED = RGBColor(90, 98, 108)      # Gris secundario
    C_CARD_BG = RGBColor(242, 246, 250)  # Fondo tarjeta azul muy suave
    C_BORDER = RGBColor(195, 212, 228)   # Borde sutil
    C_WHITE = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="DIGITALIZACIÓN APLICADA AL SISTEMA PRODUCTIVO · TEMA 4: CLOUD COMPUTING"):
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_c = tf_cat.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.name = "Calibri"
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = C_ACCENT

        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.65))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_t = tf_title.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_DARK

    def create_card(slide, left, top, width, height, title, items, subtitle="", title_color=None, bg_color=None, border_color=None):
        t_col = title_color if title_color else C_DARK
        b_col = bg_color if bg_color else C_CARD_BG
        l_col = border_color if border_color else C_BORDER

        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = b_col
        shape.line.color.rgb = l_col
        shape.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(left + Inches(0.22), top + Inches(0.18), width - Inches(0.44), height - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_head = tf.paragraphs[0]
        p_head.text = title
        p_head.font.name = "Calibri"
        p_head.font.size = Pt(13.5)
        p_head.font.bold = True
        p_head.font.color.rgb = t_col
        p_head.space_after = Pt(2)

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.name = "Calibri"
            p_sub.font.size = Pt(9.5)
            p_sub.font.italic = True
            p_sub.font.color.rgb = C_MID
            p_sub.space_after = Pt(6)
        else:
            p_head.space_after = Pt(6)

        for bullet in items:
            p_b = tf.add_paragraph()
            p_b.font.name = "Calibri"
            p_b.font.size = Pt(10.5)
            p_b.space_after = Pt(4)

            if ":" in bullet:
                b_part, r_part = bullet.split(":", 1)
                run_b = p_b.add_run()
                run_b.text = "• " + b_part + ":"
                run_b.font.bold = True
                run_b.font.color.rgb = t_col
                run_r = p_b.add_run()
                run_r.text = r_part
                run_r.font.color.rgb = C_TEXT
            else:
                run_txt = p_b.add_run()
                run_txt.text = "• " + bullet
                run_txt.font.color.rgb = C_TEXT

    # =========================================================================
    # DIAPOSITIVA 1: PORTADA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)

    left_rect = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.0), Inches(4.3), Inches(5.5))
    left_rect.fill.solid()
    left_rect.fill.fore_color.rgb = C_DARK
    left_rect.line.fill.background()

    tb_l = s1.shapes.add_textbox(Inches(1.1), Inches(1.5), Inches(3.7), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p_l1 = tf_l.paragraphs[0]
    p_l1.text = "EduPlus\nAcademy"
    p_l1.font.name = "Calibri"
    p_l1.font.size = Pt(34)
    p_l1.font.bold = True
    p_l1.font.color.rgb = C_WHITE
    p_l1.space_after = Pt(14)

    p_l2 = tf_l.add_paragraph()
    p_l2.text = "Centro de formación y clases particulares online y presenciales"
    p_l2.font.name = "Calibri"
    p_l2.font.size = Pt(14)
    p_l2.font.color.rgb = RGBColor(180, 215, 245)
    p_l2.space_after = Pt(22)

    p_l3 = tf_l.add_paragraph()
    p_l3.text = "Fundado en 2018 por Samuel y Rebeca\n6 Docentes · Más de 120 Alumnos\nPrimaria · ESO · Bachillerato · PAU · Cambridge"
    p_l3.font.name = "Calibri"
    p_l3.font.size = Pt(11)
    p_l3.font.color.rgb = C_WHITE

    tb_r = s1.shapes.add_textbox(Inches(5.5), Inches(1.2), Inches(7.0), Inches(5.1))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr_cat = tf_r.paragraphs[0]
    pr_cat.text = "PROYECTO DE DIGITALIZACIÓN APLICADA AL SISTEMA PRODUCTIVO"
    pr_cat.font.name = "Calibri"
    pr_cat.font.size = Pt(12)
    pr_cat.font.bold = True
    pr_cat.font.color.rgb = C_ACCENT
    pr_cat.space_after = Pt(12)

    pr_t = tf_r.add_paragraph()
    pr_t.text = "Propuesta de Trabajo en la Nube para EduPlus Academy"
    pr_t.font.name = "Calibri"
    pr_t.font.size = Pt(28)
    pr_t.font.bold = True
    pr_t.font.color.rgb = C_DARK
    pr_t.space_after = Pt(16)

    pr_desc = tf_r.add_paragraph()
    pr_desc.text = (
        "Estudio estratégico para migrar del modelo tradicional en papel y archivos locales hacia una "
        "arquitectura SaaS en la nube: segura, colaborativa, económica y preparada para la docencia híbrida."
    )
    pr_desc.font.name = "Calibri"
    pr_desc.font.size = Pt(13)
    pr_desc.font.color.rgb = C_MUTED
    pr_desc.space_after = Pt(26)

    pr_meta = tf_r.add_paragraph()
    pr_meta.text = (
        "Alumno: Kevin (Asumiendo el rol de Rebeca, cofundadora)\n"
        "Curso: 2º DAM · Tema 4: Cloud Computing y Edge Computing\n"
        "Defensa del proyecto ante Samuel y el equipo docente"
    )
    pr_meta.font.name = "Calibri"
    pr_meta.font.size = Pt(12)
    pr_meta.font.bold = True
    pr_meta.font.color.rgb = C_MID

    # =========================================================================
    # DIAPOSITIVA 2: CONTEXTO Y PROBLEMAS DEL MODELO LOCAL ACTUAL
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Diagnóstico Inicial: ¿Por qué EduPlus Academy necesita la nube?")

    create_card(s2, Inches(0.8), Inches(1.65), Inches(3.7), Inches(5.2),
        "Nuestra Academia Hoy",
        [
            "Fundada en 2018: Creada por Samuel y Rebeca con vocación pedagógica.",
            "Crecimiento Real: Ya somos 6 docentes y superamos los 120 alumnos.",
            "Oferta Educativa: Refuerzo en Primaria, ESO y Bachillerato, talleres de técnicas de estudio y orientación.",
            "Exámenes Oficiales: Preparación de PAU, Cambridge y pruebas de acceso.",
            "Cuello de Botella: Hemos crecido en alumnos, pero seguimos gestionando todo como el primer día."
        ],
        "Actividades y dimensión del centro"
    )

    create_card(s2, Inches(4.8), Inches(1.65), Inches(3.7), Inches(5.2),
        "Riesgos del Modelo Local Actual",
        [
            "Papel y Dispersión: Informes y exámenes en carpetas físicas o repartidos en distintos ordenadores.",
            "Caos en envíos: Tareas y apuntes enviados por WhatsApp o email sin orden.",
            "Pérdida de Datos (Tema 4): Peligro ante error humano, corte de luz (caso Marcos) o rotura de disco duro.",
            "Multas AEPD (RGPD): Manejar datos de 120 menores en USBs o WhatsApp expone a sanciones de hasta 60.000 €.",
            "Lección de la Pandemia: Clases online improvisadas sin plataforma común."
        ],
        "Peligros de trabajar sin la nube"
    )

    create_card(s2, Inches(8.8), Inches(1.65), Inches(3.7), Inches(5.2),
        "Rebeca vs. Samuel: El Reto",
        [
            "Visión de Rebeca: Implementar un sistema moderno en la nube que unifique materiales, comunicación y clases.",
            "Temor de Samuel: Miedo a que requiera demasiado tiempo, sea caro y cueste mucho formar a los 6 profesores.",
            "Dato Clave (Tema 4): El 80 % de las empresas tienen una visión positiva en los primeros 6 meses en la nube.",
            "Objetivo de esta Propuesta: Demostrar a Samuel una solución sencilla, casi gratuita y sin complejidad técnica."
        ],
        "Alineando a los dos fundadores"
    )

    # =========================================================================
    # DIAPOSITIVA 3: TAREA 1 (PARTE A) - LAS 7 FUNCIONES DE LA NUBE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. Tarea 1 (I): ¿Para qué funciones concretas usaremos la nube?")

    create_card(s3, Inches(0.8), Inches(1.65), Inches(5.7), Inches(2.5),
        "1. Materiales, Copias de Seguridad y Acceso Remoto",
        [
            "Almacenamiento centralizado: Todos los PDFs, vídeos y presentaciones de Primaria, ESO, Bachillerato, PAU y Cambridge en un solo lugar.",
            "Copias de seguridad automáticas (Backup): Guardado cada 5 segundos (como Sonia en el Tema 4); cero pérdidas por cortes de luz o fallos mecánicos.",
            "Acceso remoto 24/7: Los 6 profesores y 120 alumnos acceden desde cualquier ordenador, tablet o móvil, en el aula o teletrabajando."
        ]
    )

    create_card(s3, Inches(6.8), Inches(1.65), Inches(5.7), Inches(2.5),
        "2. Horarios, Tutorías y Comunicación con Familias",
        [
            "Gestión de horarios y aulas: Calendarios en la nube sincronizados para asignar aulas de grupos reducidos sin solapamientos.",
            "Reserva online de tutorías: Las familias eligen hueco en el calendario desde su móvil sin cruzar decenas de mensajes.",
            "Comunicación institucional y RGPD: Fin del WhatsApp personal; avisos oficiales, asistencia y circulares por plataforma segura."
        ]
    )

    create_card(s3, Inches(0.8), Inches(4.35), Inches(11.7), Inches(2.5),
        "3. Evaluación Trimestral, Tareas y Plataforma de Clases Online Colaborativas",
        [
            "Registro de notas y evaluaciones: Entrega de tareas en el aula virtual con control de fecha, test autocorregibles (Forms) para practicar PAU/Cambridge y generación automática de los informes trimestrales en PDF privado para cada familia (adiós a las carpetas físicas).",
            "Plataforma unificada de clases online: Videollamadas integradas con pizarra digital y edición colaborativa en tiempo real para clases particulares a distancia y talleres de técnicas de estudio, evitando para siempre la improvisación sufrida en la pandemia."
        ]
    )

    # =========================================================================
    # DIAPOSITIVA 4: TAREA 1 (PARTE B) - ELECCIÓN DEL MODELO (IaaS, PaaS, SaaS)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. Tarea 1 (II): ¿Qué modelo de nube (IaaS, PaaS o SaaS) es el adecuado?")

    create_card(s4, Inches(0.8), Inches(1.65), Inches(3.6), Inches(5.2),
        "IaaS (Infraestructura)",
        [
            "Qué es: Alquilar servidores virtuales, discos y redes (ej. AWS EC2, Google Compute Engine).",
            "Símil de la Pizza: Hacer la pizza en casa comprando ingredientes y horneando.",
            "Perfil: Administradores de Sistemas (SysAdmin), como BinagorWorld.",
            "¿Para EduPlus?: NO. No tenemos informáticos para mantener servidores."
        ],
        "Infrastructure as a Service"
    )

    create_card(s4, Inches(4.7), Inches(1.65), Inches(3.6), Inches(5.2),
        "PaaS (Plataforma)",
        [
            "Qué es: Alquilar el entorno para programar tus propias aplicaciones (ej. Google App Engine).",
            "Símil Coche / Pizza: Echar gasolina y conducir / Pizza a medida en restaurante.",
            "Perfil: Desarrolladores de software, como la empresa TorcalMet.",
            "¿Para EduPlus?: NO. Nuestros 6 docentes enseñan, no programan software."
        ],
        "Platform as a Service"
    )

    create_card(s4, Inches(8.6), Inches(1.65), Inches(3.9), Inches(5.2),
        "SaaS (EL ELEGIDO)",
        [
            "Qué es: Aplicaciones listas para usar en Internet (Google Workspace, Microsoft 365).",
            "Símil de la Pizza: Pedir la pizza lista a domicilio; el proveedor hace todo.",
            "Por qué es perfecto para EduPlus: El proveedor gestiona hardware, seguridad y actualizaciones (como DragonTel).",
            "Respuesta a Samuel: Cero mantenimiento técnico, curva de aprendizaje mínima y planes educativos gratuitos."
        ],
        "Software as a Service · Modelo Óptimo",
        title_color=C_GREEN,
        bg_color=RGBColor(243, 248, 238),
        border_color=RGBColor(165, 198, 144)
    )

    # =========================================================================
    # DIAPOSITIVA 5: TAREA 2 - VENTAJAS, INCONVENIENTES Y RESPUESTAS A SAMUEL
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. Tarea 2: Ventajas, Inconvenientes y Respuestas para Convencer a Samuel")

    create_card(s5, Inches(0.8), Inches(1.65), Inches(3.7), Inches(5.2),
        "1. Cambios Económicos",
        [
            "Ventajas: Sin inversión inicial en servidores (CAPEX 0), pago por uso escalable, ahorro en papel/tóner/luz y evita multas AEPD de 60.000 €.",
            "Inconvenientes (Samuel): Posible cuota mensual recurrente y necesitar buena fibra óptica.",
            "Respuesta de Rebeca: Las licencias educativas (Google/Microsoft Education) cuestan 0 € (o <25 €/mes en planes ampliados), ahorrando más de 180 €/mes en papel y tiempo."
        ],
        "Rentabilidad desde el minuto uno",
        title_color=C_PURPLE,
        bg_color=RGBColor(249, 242, 250),
        border_color=RGBColor(210, 180, 222)
    )

    create_card(s5, Inches(4.8), Inches(1.65), Inches(3.7), Inches(5.2),
        "2. Cambios en los Empleados",
        [
            "Ventajas: Autoguardado cada 5 s (caso Sonia), coedición de exámenes, teletrabajo fluido y fin del caos de WhatsApp.",
            "Inconvenientes (Samuel): Tiempo de formación de los 6 docentes, pasar archivos a la nube y miedo a que caiga Internet (caso AWS).",
            "Respuesta de Rebeca: Con SaaS usan apps que ya conocen (Drive/Docs); haremos 2 talleres de 45 min, migración gradual y activaremos el Modo Sin Conexión (Offline)."
        ],
        "Comodidad para los 6 docentes",
        title_color=C_PURPLE,
        bg_color=RGBColor(249, 242, 250),
        border_color=RGBColor(210, 180, 222)
    )

    create_card(s5, Inches(8.8), Inches(1.65), Inches(3.7), Inches(5.2),
        "3. Cambios Medioambientales",
        [
            "Ventajas: Academia 'Papel Cero' (120 informes y miles de fichas digitales), menos viajes en coche y sin servidores locales 24/7.",
            "Inconvenientes (Samuel): Gasto energético de los grandes centros de datos y tráfico de red.",
            "Respuesta de Rebeca: Los centros cloud usan energía 100 % renovable y, al procesar en la nube, alargamos años la vida de nuestros ordenadores actuales sin generar basura electrónica."
        ],
        "Sostenibilidad real en la academia",
        title_color=C_PURPLE,
        bg_color=RGBColor(249, 242, 250),
        border_color=RGBColor(210, 180, 222)
    )

    # =========================================================================
    # DIAPOSITIVA 6: TAREA 3 - ESTUDIO DE PROVEEDORES
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "5. Tarea 3: Estudio de Proveedores (Microsoft Azure, Google Cloud, IBM Cloud)")

    create_card(s6, Inches(0.8), Inches(1.65), Inches(3.7), Inches(5.2),
        "Microsoft Azure (+ M365)",
        [
            "Teams para Educación (SaaS): Aulas virtuales, videollamadas, tareas y notas (usado por docentes en la C. Valenciana).",
            "OneDrive y SharePoint: 1 TB por profesor y carpetas departamentales con Word/Excel Online.",
            "Bookings y Forms: Reserva automática de tutorías para familias y exámenes autocorregibles.",
            "Azure Backup & Blob Storage: Copias de seguridad inmutables en Europa (RGPD) y líder en nube híbrida."
        ],
        "Ecosistema Microsoft",
        title_color=C_GREEN,
        bg_color=RGBColor(243, 248, 238),
        border_color=RGBColor(165, 198, 144)
    )

    create_card(s6, Inches(4.8), Inches(1.65), Inches(3.7), Inches(5.2),
        "Google Cloud (+ Workspace)",
        [
            "Google Classroom (SaaS): Gestión súper intuitiva de grupos de Primaria, ESO, Bachillerato, PAU y Cambridge.",
            "Drive, Docs, Sheets y Slides: Unidades compartidas, autoguardado cada 5 s y modo sin conexión.",
            "Meet, Calendar y Forms: Clases online HD, horarios de aulas y test.",
            "Cloud Storage, GKE y Cloud AI: Pionero en contenedores Kubernetes y asistencia IA (Gemini) para crear materiales."
        ],
        "Ecosistema Google (Opción Principal)",
        title_color=C_GREEN,
        bg_color=RGBColor(243, 248, 238),
        border_color=RGBColor(165, 198, 144)
    )

    create_card(s6, Inches(8.8), Inches(1.65), Inches(3.7), Inches(5.2),
        "IBM Cloud",
        [
            "IBM Cloud Object Storage: Copias de seguridad con cifrado bancario para blindar expedientes de menores (AEPD).",
            "IBM watsonx Assistant (IA): Chatbot en la web de EduPlus para responder dudas de familias 24/7 sobre horarios y matrículas.",
            "IBM Cloud Private & OpenShift: Referente del Tema 4 en nube privada/híbrida y contenedores seguros.",
            "Virtual Servers / Code Engine: Alojamiento seguro de la web de la academia."
        ],
        "Seguridad empresarial e IA",
        title_color=C_GREEN,
        bg_color=RGBColor(243, 248, 238),
        border_color=RGBColor(165, 198, 144)
    )

    # =========================================================================
    # DIAPOSITIVA 7: PLAN DE IMPLEMENTACIÓN, PRESUPUESTO Y REDUNDANCIA
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "6. Plan de Implementación en 4 Semanas y Presupuesto")

    create_card(s7, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.2),
        "Hoja de Ruta Gradual (Sin agobiar al equipo)",
        [
            "Semana 1 (Estructura y Seguridad): Alta en Google Workspace for Education, creación de cuentas para los 6 docentes y carpetas por nivel (Primaria, ESO, Bachillerato, PAU, Cambridge).",
            "Semana 2 (Formación de 90 min y Horarios): Rebeca imparte 2 talleres prácticos de 45 min a los compañeros. Puesta en marcha del calendario compartido de aulas y tutorías.",
            "Semana 3 (Aulas Virtuales y Boletines): Apertura de clases en Google Classroom y plantillas automáticas de informes trimestrales.",
            "Semana 4 (Familias y Backup Cruzado): Bienvenida a las 120 familias (fin del WhatsApp) y activación del backup semanal en segundo proveedor."
        ],
        "Transición ordenada liderada por Rebeca"
    )

    create_card(s7, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2),
        "Decisión Técnica y Presupuesto Real",
        [
            "Plataforma Diaria (SaaS): Google Workspace for Education (o M365 A1) → Coste 0 €/mes en plan educativo base (o 18 €/mes ampliado).",
            "Solución 'Cuando la nube falla' (Tema 4): Backup automático cruzado en Azure Blob Storage / IBM Cloud Object Storage por solo 3 €/mes.",
            "Dominio corporativo (@eduplusacademy.es): 1 €/mes (12 €/año).",
            "Ahorro Neto Inmediato: Gastamos entre 4 € y 22 €/mes y ahorramos más de 180 €/mes en papel, carpetas, tóner y horas de gestión.",
            "Protección Legal Total: Cumplimiento RGPD/AEPD garantizado."
        ],
        "Máxima seguridad al menor coste posible"
    )

    # =========================================================================
    # DIAPOSITIVA 8: VALORACIÓN FINAL Y CONCLUSIONES
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "7. Valoración Final y Defensa del Proyecto")

    create_card(s8, Inches(0.8), Inches(1.65), Inches(3.7), Inches(5.2),
        "Por qué ganamos todos",
        [
            "Para Samuel: Sin inversión inicial, sin administrar servidores y con respaldo ante cualquier caída.",
            "Para los 6 Docentes: Menos carga burocrática, autoguardado cada 5 s y facilidad para teletrabajar.",
            "Para los 120 Alumnos y Familias: Materiales accesibles 24/7, clases online de calidad y comunicación clara."
        ],
        "Beneficio 360º en EduPlus Academy"
    )

    create_card(s8, Inches(4.8), Inches(1.65), Inches(3.7), Inches(5.2),
        "Conclusión Tecnológica",
        [
            "El modelo SaaS es la clave: Nos permite disfrutar de la potencia de Google Cloud, Azure e IBM sin ser informáticos.",
            "Sostenibilidad y Futuro: Eliminamos miles de fotocopias y alargamos la vida de nuestros ordenadores.",
            "Escalabilidad: EduPlus Academy queda preparada para crecer sin límites."
        ],
        "Síntesis del Tema 4 aplicada"
    )

    create_card(s8, Inches(8.8), Inches(1.65), Inches(3.7), Inches(5.2),
        "Datos de Entrega del Proyecto",
        [
            "Proyecto: Propuesta de Trabajo en la Nube para EduPlus Academy.",
            "Autor: Kevin (Rol: Rebeca) · 2º DAM.",
            "Módulo: Digitalización Aplicada al Sistema Productivo.",
            "Entregables Generados: Informe Completo en Word y PDF (Calibri 11, justificado, interlineado 1.5) + Presentación Ejecutiva PPTX.",
            "¡Muchas gracias por su atención!"
        ],
        "Defensa final"
    )

    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "Presentacion_Cloud_EduPlus_Kevin.pptx")
    prs.save(output_path)
    print(f"Presentación PPTX creada con éxito en: {output_path}")

    parent_dir = os.path.dirname(output_dir)
    parent_copy = os.path.join(parent_dir, "Presentacion_Cloud_EduPlus_Kevin.pptx")
    shutil.copyfile(output_path, parent_copy)
    print(f"Copia guardada en: {parent_copy}")

    return output_path

if __name__ == "__main__":
    create_presentation()
