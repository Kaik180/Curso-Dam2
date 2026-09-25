import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank layout

    # Colors
    C_NAVY = RGBColor(10, 37, 64)       # #0A2540
    C_BLUE = RGBColor(13, 110, 253)     # #0D6EFD
    C_TEAL = RGBColor(0, 168, 150)      # #00A896
    C_CORAL = RGBColor(224, 86, 36)     # #E05624
    C_BG_SLIDE = RGBColor(248, 250, 252) # #F8FAFC
    C_CARD_BG = RGBColor(255, 255, 255) # #FFFFFF
    C_BORDER = RGBColor(226, 232, 240)  # #E2E8F0
    C_TEXT_DARK = RGBColor(30, 41, 59)  # #1E293B
    C_TEXT_MUTED = RGBColor(100, 116, 139) # #64748B
    C_LIGHT_BLUE = RGBColor(237, 242, 247) # #EDF2F7

    def draw_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG_SLIDE
        bg.line.color.rgb = C_BG_SLIDE
        return bg

    def add_top_nav(slide, tag_text, slide_num_str):
        # Top banner line
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_TEAL
        top_bar.line.color.rgb = C_TEAL

        # Header bar box
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.25), Inches(8), Inches(0.4))
        p = tb.text_frame.paragraphs[0]
        p.text = "FarmaCare & Physio  •  Proyecto Intermodular 2º DAM"
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_TEAL

        # Slide indicator on right
        tb_num = slide.shapes.add_textbox(Inches(9.5), Inches(0.25), Inches(3), Inches(0.4))
        p_num = tb_num.text_frame.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = slide_num_str
        p_num.font.name = "Calibri"
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = C_TEXT_MUTED

    def add_slide_header(slide, title, subtitle):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = 0
        tf.margin_left = 0

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY
        p1.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.name = "Calibri"
        p2.font.size = Pt(13)
        p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # DIAPOSITIVA 1: EL PROBLEMA Y A QUIÉN AFECTA
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    draw_bg(slide1)
    add_top_nav(slide1, "DIAGNÓSTICO DEL PROBLEMA", "01 / 03  •  EL PROBLEMA")
    add_slide_header(slide1, "1. Problema y Necesidad Detectada", "¿Qué ocurre en la realidad y a quién afecta directamente?")

    # Tarjeta Izquierda: ¿Qué ocurre? (El Problema)
    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.5))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_CARD_BG
    card1.line.color.rgb = C_BORDER
    card1.line.width = Pt(1.5)

    tb_c1 = slide1.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.1))
    tf1 = tb_c1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "🚨 ¿QUÉ OCURRE?"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_CORAL
    p.space_after = Pt(12)

    items_c1 = [
        ("Falta de Adherencia Terapéutica", "Casi el 50% de los pacientes no toman su medicación según lo prescrito (OMS), provocando recaídas y complicaciones."),
        ("Olvidos y Confusión de Posología", "La toma de múltiples pastillas genera dosis duplicadas o tomas omitidas por desconocer las horas exactas."),
        ("Prospectos Incomprensibles", "Letra diminuta y terminología médica compleja que desconciertan al usuario no especializado."),
        ("Rehabilitación Abandonada", "Las pautas en papel de ejercicios musculares o traumatismos se pierden o se ejecutan sin la postura adecuada.")
    ]
    for tit, desc in items_c1:
        p_t = tf1.add_paragraph()
        p_t.text = f"• {tit}: "
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_t.space_after = Pt(1)

        p_d = tf1.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_TEXT_DARK
        p_d.space_after = Pt(8)

    # Tarjeta Derecha: ¿A quién afecta?
    card2 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.5))
    card2.fill.solid()
    card2.fill.fore_color.rgb = C_CARD_BG
    card2.line.color.rgb = C_BORDER
    card2.line.width = Pt(1.5)

    tb_c2 = slide1.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.1))
    tf2 = tb_c2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "👥 ¿A QUIÉN AFECTA?"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(12)

    items_c2 = [
        ("Personas Mayores y Pacientes con Alzheimer", "Especial vulnerabilidad ante la polimedicación y el deterioro cognitivo leve o despistes frecuentes."),
        ("Cuidadores y Familiares", "Estrés y sobrecarga mental permanente ante la incertidumbre de no saber si su familiar tomó la pastilla a tiempo."),
        ("Personas con Traumatismos o Dolor Muscular", "Pacientes en recuperación de esguinces, cirugías o dolores crónicos que necesitan fortalecer zonas específicas."),
        ("Sistema Sanitario y ODS 3", "El abandono del tratamiento satura las urgencias. Resolverlo promueve el ODS 3 (Salud y Bienestar).")
    ]
    for tit, desc in items_c2:
        p_t = tf2.add_paragraph()
        p_t.text = f"• {tit}: "
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_t.space_after = Pt(1)

        p_d = tf2.add_paragraph()
        p_d.text = f"   {desc}"
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_TEXT_DARK
        p_d.space_after = Pt(8)

    # Footer banner
    b_foot = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.55))
    b_foot.fill.solid()
    b_foot.fill.fore_color.rgb = C_NAVY
    b_foot.line.color.rgb = C_NAVY
    p_bf = b_foot.text_frame.paragraphs[0]
    p_bf.text = "💡 IMPACTO: Alineado con los Objetivos de Desarrollo Sostenible (ODS 3 Salud y Bienestar • ODS 10 Reducción de Desigualdades)"
    p_bf.font.name = "Calibri"
    p_bf.font.size = Pt(10.5)
    p_bf.font.bold = True
    p_bf.font.color.rgb = RGBColor(255, 255, 255)
    p_bf.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # DIAPOSITIVA 2: LA SOLUCIÓN Y FUNCIONALIDADES
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    draw_bg(slide2)
    add_top_nav(slide2, "PROPUESTA DIGITAL", "02 / 03  •  LA SOLUCIÓN")
    add_slide_header(slide2, "2. Solución Digital y Funcionalidades Clave", "FarmaCare & Physio: Asistente móvil integral para tratamientos y recuperación física")

    # Contenedor Imagen (Mockup de la App)
    img_path = os.path.join(os.path.dirname(__file__), "mockup_farmacare.jpg")
    if os.path.exists(img_path):
        # Insert image on left
        slide2.shapes.add_picture(img_path, Inches(0.8), Inches(1.8), width=Inches(5.6))

    # Tarjeta de Funcionalidades en la derecha
    card_sol = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.7), Inches(1.8), Inches(5.8), Inches(4.5))
    card_sol.fill.solid()
    card_sol.fill.fore_color.rgb = C_CARD_BG
    card_sol.line.color.rgb = C_BORDER
    card_sol.line.width = Pt(1.5)

    tb_sol = slide2.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.2), Inches(4.2))
    tf_sol = tb_sol.text_frame
    tf_sol.word_wrap = True

    p = tf_sol.paragraphs[0]
    p.text = "⚡ FUNCIONALIDADES PRINCIPALES"
    p.font.name = "Calibri"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    funcs_list = [
        ("⏰ Alarmas con Locución por Voz", "Avisos sonoros que explican qué fármaco tomar, la dosis y si debe acompañarse con comida o agua."),
        ("✅ Confirmación Fácil y Antiolvido", "Botón táctil gigante para registrar la toma, evitando dosis duplicadas por despistes."),
        ("🛡️ Alerta Automática a Cuidadores", "Si la toma no se confirma en 20 minutos, la app avisa al familiar por notificación o SMS."),
        ("🏋️ Módulo de Ejercicios Musculares", "Rutinas visuales guiadas para fortalecer músculos dañados por traumatismos o dolores posturales."),
        ("📖 Prospecto Claro y Resumido", "Información simplificada en lenguaje accesible sobre para qué sirve cada medicamento."),
        ("📊 Historial de Adherencia en PDF", "Gráficos de cumplimiento terapéutico y actividad para mostrar al médico en consulta.")
    ]
    for f_tit, f_desc in funcs_list:
        p_ft = tf_sol.add_paragraph()
        p_ft.text = f_tit
        p_ft.font.name = "Calibri"
        p_ft.font.size = Pt(11)
        p_ft.font.bold = True
        p_ft.font.color.rgb = C_TEAL
        p_ft.space_after = Pt(1)

        p_fd = tf_sol.add_paragraph()
        p_fd.text = f_desc
        p_fd.font.name = "Calibri"
        p_fd.font.size = Pt(9.5)
        p_fd.font.color.rgb = C_TEXT_DARK
        p_fd.space_after = Pt(6)

    # Footer banner slide 2
    b_foot2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.55))
    b_foot2.fill.solid()
    b_foot2.fill.fore_color.rgb = C_NAVY
    b_foot2.line.color.rgb = C_NAVY
    p_bf2 = b_foot2.text_frame.paragraphs[0]
    p_bf2.text = "📱 Solución Multiplataforma (Android / iOS) • Modo 'Fácil' Adaptado para la Tercera Edad"
    p_bf2.font.name = "Calibri"
    p_bf2.font.size = Pt(10.5)
    p_bf2.font.bold = True
    p_bf2.font.color.rgb = RGBColor(255, 255, 255)
    p_bf2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # DIAPOSITIVA 3: VALOR AÑADIDO Y MEJORA FUTURA
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    draw_bg(slide3)
    add_top_nav(slide3, "VALOR E INNOVACIÓN", "03 / 03  •  VALOR AÑADIDO")
    add_slide_header(slide3, "3. Valor Añadido y Visión de Futuro", "¿Por qué aporta un beneficio diferencial y cuáles son las mejoras previstas?")

    # Tarjeta Izquierda: ¿Por qué resulta útil? (Valor Añadido)
    card_va = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.5))
    card_va.fill.solid()
    card_va.fill.fore_color.rgb = C_CARD_BG
    card_va.line.color.rgb = C_BORDER
    card_va.line.width = Pt(1.5)

    tb_va = slide3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.1))
    tf_va = tb_va.text_frame
    tf_va.word_wrap = True

    p = tf_va.paragraphs[0]
    p.text = "🌟 VALOR AÑADIDO (¿POR QUÉ ES ÚTIL?)"
    p.font.name = "Calibri"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(12)

    val_items = [
        ("Solución Dual 2 en 1", "Unifica el control farmacológico y el fortalecimiento muscular en una única aplicación sin dispersión de datos."),
        ("Máxima Autonomía para Mayores", "Reduce la dependencia de terceros gracias a alarmas habladas, diseño contrastado y confirmación simple."),
        ("Tranquilidad para los Cuidadores", "Supervisión pasiva: solo reciben avisos si surge una omisión, eliminando el estrés de llamadas continuas."),
        ("Prevención y Recuperación Activa", "Evita que contracturas o lesiones traumatológicas se cronifiquen por falta de rehabilitación domiciliaria.")
    ]
    for v_tit, v_desc in val_items:
        p_t = tf_va.add_paragraph()
        p_t.text = f"✔ {v_tit}: "
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(11.5)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_t.space_after = Pt(1)

        p_d = tf_va.add_paragraph()
        p_d.text = f"   {v_desc}"
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_TEXT_DARK
        p_d.space_after = Pt(8)

    # Tarjeta Derecha: Mejoras Futuras
    card_mf = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.5))
    card_mf.fill.solid()
    card_mf.fill.fore_color.rgb = C_CARD_BG
    card_mf.line.color.rgb = C_BORDER
    card_mf.line.width = Pt(1.5)

    tb_mf = slide3.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.1))
    tf_mf = tb_mf.text_frame
    tf_mf.word_wrap = True

    p = tf_mf.paragraphs[0]
    p.text = "🚀 MEJORAS FUTURAS INCORPORABLES"
    p.font.name = "Calibri"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.space_after = Pt(12)

    fut_items = [
        ("Inteligencia Artificial Postural", "Uso de la cámara y Computer Vision para verificar en tiempo real si el paciente hace bien el ejercicio y corregirlo."),
        ("Escaneo OCR de Cajas Médicas", "Carga automática de posología fotografiando la caja del medicamento o el código de barras nacional."),
        ("Conexión con Wearables e IoT", "Vibración háptica de recordatorio en smartwatch, detección de caídas y pastilleros inteligentes conectados."),
        ("Integración con Receta Electrónica", "Sincronización con el sistema sanitario público para actualizar tratamientos automáticamente.")
    ]
    for f_tit, f_desc in fut_items:
        p_t = tf_mf.add_paragraph()
        p_t.text = f"✦ {f_tit}: "
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(11.5)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_t.space_after = Pt(1)

        p_d = tf_mf.add_paragraph()
        p_d.text = f"   {f_desc}"
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_TEXT_DARK
        p_d.space_after = Pt(8)

    # Footer banner slide 3
    b_foot3 = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.55))
    b_foot3.fill.solid()
    b_foot3.fill.fore_color.rgb = C_NAVY
    b_foot3.line.color.rgb = C_NAVY
    p_bf3 = b_foot3.text_frame.paragraphs[0]
    p_bf3.text = "🎯 CONCLUSIÓN: Tecnología accesible al servicio de la salud, autonomía y bienestar de las personas"
    p_bf3.font.name = "Calibri"
    p_bf3.font.size = Pt(10.5)
    p_bf3.font.bold = True
    p_bf3.font.color.rgb = RGBColor(255, 255, 255)
    p_bf3.alignment = PP_ALIGN.CENTER

    output_pptx = os.path.join(os.path.dirname(__file__), "Tarea0_FarmaCare_Presentacion.pptx")
    prs.save(output_pptx)
    print(f"Presentation saved successfully at: {output_pptx}")

if __name__ == "__main__":
    create_presentation()
