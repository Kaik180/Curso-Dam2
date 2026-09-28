import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    curr_dir = os.path.dirname(__file__)

    # Memorix Color Palette from contrastes.png
    C_NAVY = RGBColor(5, 12, 38)         # #050C26 (Deep Midnight Navy)
    C_MINT = RGBColor(0, 210, 180)       # #00D2B4 (Vibrant Mint / Cyan)
    C_BLUE = RGBColor(0, 56, 255)        # #0038FF (Royal Tech Blue)
    C_CORAL = RGBColor(224, 86, 36)      # #E05624 (Alert Coral)
    C_BG_SLIDE = RGBColor(248, 250, 252) # #F8FAFC
    C_CARD_BG = RGBColor(255, 255, 255)  # #FFFFFF
    C_BORDER = RGBColor(226, 232, 240)   # #E2E8F0
    C_TEXT_DARK = RGBColor(30, 41, 59)   # #1E293B
    C_TEXT_MUTED = RGBColor(100, 116, 139) # #64748B

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
        top_bar.fill.fore_color.rgb = C_MINT
        top_bar.line.color.rgb = C_MINT

        # Logo / Text box on left
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.2), Inches(8), Inches(0.45))
        p = tb.text_frame.paragraphs[0]
        p.text = "Memorix  •  Proyecto Intermodular 2º DAM"
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_MINT

        # Slide indicator on right
        tb_num = slide.shapes.add_textbox(Inches(9.5), Inches(0.2), Inches(3), Inches(0.45))
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
    add_slide_header(slide1, "1. Problema y Necesidad Detectada", "¿Qué ocurre en la realidad diaria y a quién afecta?")

    # Tarjeta Izquierda: ¿Qué ocurre?
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
        ("50% de Abandono Terapéutico", "Casi la mitad de enfermos crónicos no toman su medicación correctamente (OMS), provocando recaídas y urgencias."),
        ("Olvidos y Confusión de Dosis", "Múltiples pastillas diarias provocan tomas duplicadas o dosis omitidas por no recordar las horas."),
        ("Prospectos Inaccesibles", "Texto minúsculo e instrucciones farmacológicas complejas que generan inseguridad."),
        ("Rehabilitación en Papel Ineficaz", "Las rutinas de ejercicios para traumatismos o dolor muscular se olvidan o se ejecutan sin técnica adecuada.")
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
    p.font.color.rgb = C_BLUE
    p.space_after = Pt(12)

    items_c2 = [
        ("Mayores y Pacientes de Alzheimer", "Vulnerabilidad extrema ante polimedicación y despistes por deterioro cognitivo."),
        ("Cuidadores y Familias", "Estrés constante y sobrecarga mental por no tener confirmación de que la medicación se ha tomado."),
        ("Personas con Traumatismos o Dolor Físico", "Pacientes en recuperación de lesiones o con dolores de espalda/cuello que necesitan fortalecer zonas específicas."),
        ("Sistema de Salud y ODS 3", "El mal uso de medicamentos colapsa consultas. Resolverlo impacta en el ODS 3 (Salud) y ODS 10 (Accesibilidad).")
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

    # Footer banner slide 1
    b_foot1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.55))
    b_foot1.fill.solid()
    b_foot1.fill.fore_color.rgb = C_NAVY
    b_foot1.line.color.rgb = C_NAVY
    p_bf1 = b_foot1.text_frame.paragraphs[0]
    p_bf1.text = "💡 IMPACTO: Alineado con los Objetivos de Desarrollo Sostenible (ODS 3 Salud y Bienestar • ODS 10 Reducción de Desigualdades)"
    p_bf1.font.name = "Calibri"
    p_bf1.font.size = Pt(10.5)
    p_bf1.font.bold = True
    p_bf1.font.color.rgb = RGBColor(255, 255, 255)
    p_bf1.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # DIAPOSITIVA 2: LA SOLUCIÓN MEMORIX Y FUNCIONALIDADES
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    draw_bg(slide2)
    add_top_nav(slide2, "PROPUESTA DIGITAL", "02 / 03  •  LA SOLUCIÓN")
    add_slide_header(slide2, "2. Memorix: Solución Digital Accesible", "Asistente móvil inteligente con alto contraste visual para medicación y rehabilitación")

    # Contenedor Imagen Izquierda (Mockup de Memorix)
    img_mockup = os.path.join(curr_dir, "mockup_memorix.jpg")
    if os.path.exists(img_mockup):
        slide2.shapes.add_picture(img_mockup, Inches(0.8), Inches(1.8), width=Inches(5.5))

    # Tarjeta de Funcionalidades en la derecha
    card_sol = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.6), Inches(1.8), Inches(5.9), Inches(4.5))
    card_sol.fill.solid()
    card_sol.fill.fore_color.rgb = C_CARD_BG
    card_sol.line.color.rgb = C_BORDER
    card_sol.line.width = Pt(1.5)

    tb_sol = slide2.shapes.add_textbox(Inches(6.9), Inches(1.95), Inches(5.3), Inches(4.2))
    tf_sol = tb_sol.text_frame
    tf_sol.word_wrap = True

    p = tf_sol.paragraphs[0]
    p.text = "⚡ FUNCIONALIDADES CLAVE DE MEMORIX"
    p.font.name = "Calibri"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    funcs_list = [
        ("🔊 Alarmas Inteligentes con Audio-Guía", "Reproduce por voz el nombre del fármaco, dosis e indicaciones (ej. 'tomar con agua tras la comida')."),
        ("✅ Confirmación Fácil de Un Toque", "Botón táctil de gran visibilidad para registrar la toma y evitar duplicidades por despistes."),
        ("🛡️ Alerta Automática SOS a Cuidadores", "Si tras 20 min no se confirma una toma crítica, envía aviso inmediato al familiar asignado."),
        ("🏋️ Rutinas de Fortalecimiento Muscular", "Ejercicios guiados paso a paso con temporizador para dolores de espalda, hombros, cuello o piernas."),
        ("🎨 Interfaz de Alto Contraste (Modo Senior)", "Gama cromática de máxima legibilidad (azul, cian, menta) adaptada a problemas visuales."),
        ("📊 Historial de Adherencia Exportable", "Estadísticas semanales y mensuales de cumplimiento listas para compartir con el médico.")
    ]
    for f_tit, f_desc in funcs_list:
        p_ft = tf_sol.add_paragraph()
        p_ft.text = f_tit
        p_ft.font.name = "Calibri"
        p_ft.font.size = Pt(11)
        p_ft.font.bold = True
        p_ft.font.color.rgb = C_MINT
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
    p_bf2.text = "📱 Memorix: Aplicación Multiplataforma (Android / iOS) • Enfoque Universal y Accesible"
    p_bf2.font.name = "Calibri"
    p_bf2.font.size = Pt(10.5)
    p_bf2.font.bold = True
    p_bf2.font.color.rgb = RGBColor(255, 255, 255)
    p_bf2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # DIAPOSITIVA 3: VALOR AÑADIDO, CONTRASTES Y MEJORA FUTURA
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    draw_bg(slide3)
    add_top_nav(slide3, "VALOR E INNOVACIÓN", "03 / 03  •  VALOR AÑADIDO")
    add_slide_header(slide3, "3. Valor Añadido y Visión de Futuro", "¿Por qué Memorix marca la diferencia y hacia dónde evoluciona?")

    # Tarjeta Izquierda: ¿Por qué resulta útil? (Valor Diferencial)
    card_va = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.5))
    card_va.fill.solid()
    card_va.fill.fore_color.rgb = C_CARD_BG
    card_va.line.color.rgb = C_BORDER
    card_va.line.width = Pt(1.5)

    tb_va = slide3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.1))
    tf_va = tb_va.text_frame
    tf_va.word_wrap = True

    p = tf_va.paragraphs[0]
    p.text = "🌟 VALOR AÑADIDO DIFERENCIAL"
    p.font.name = "Calibri"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_MINT
    p.space_after = Pt(12)

    val_items = [
        ("Doble Enfoque Integral (Fármacos + Fisioterapia)", "Unifica en un solo lugar la adherencia médica y la actividad física terapéutica."),
        ("Accesibilidad Total por Contrastes", "La identidad gráfica de Memorix utiliza contrastes cromáticos de grado médico para eliminar barreras cognitivas."),
        ("Autonomía Real para la Tercera Edad", "Instrucciones de audio claras y botones gigantes que devuelven la independencia al paciente."),
        ("Paz Mental para las Familias", "Supervisión remota pasiva: solo alerta a los familiares cuando realmente ocurre una omisión.")
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
    p.text = "🚀 MEJORAS FUTURAS DE MEMORIX"
    p.font.name = "Calibri"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p.space_after = Pt(12)

    fut_items = [
        ("IA de Visión Artificial (Computer Vision)", "Supervisión postural en tiempo real a través de la cámara del móvil durante los ejercicios de fisioterapia."),
        ("Escaneo OCR Inteligente de Cajas", "Reconocimiento automático de prospectos y posología con solo enfocar la caja del medicamento."),
        ("Conectividad IoT con Smartwatches", "Vibración en la muñeca para avisar de la toma y detección de caídas en personas mayores."),
        ("Interoperabilidad con Receta Electrónica", "Conexión directa con la historia clínica pública para actualizar dosis automáticamente.")
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
    p_bf3.text = "🎯 MEMORIX: Tecnología accesible al servicio de la salud, autonomía y bienestar de las personas"
    p_bf3.font.name = "Calibri"
    p_bf3.font.size = Pt(10.5)
    p_bf3.font.bold = True
    p_bf3.font.color.rgb = RGBColor(255, 255, 255)
    p_bf3.alignment = PP_ALIGN.CENTER

    output_pptx = os.path.join(curr_dir, "Tarea0_Memorix_Presentacion.pptx")
    prs.save(output_pptx)
    print(f"Presentation saved successfully at: {output_pptx}")

if __name__ == "__main__":
    create_presentation()
