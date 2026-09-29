import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

curr_dir = os.path.dirname(__file__)

# =========================================================================
# 1. GENERAR DOCUMENTO PDF (3 PÁGINAS A4 EXACTAS)
# =========================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#78909C"))

        # Cabecera
        header_text = "Proyecto Intermodular - 2º DAM  |  Tarea 0: Memorix"
        self.drawRightString(A4[0] - 50, A4[1] - 38, header_text)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(50, A4[1] - 44, A4[0] - 50, A4[1] - 44)

        # Pie de página
        footer_left = "Memorix  •  Kevin Muñoz Córcoles"
        footer_right = f"Página {self._pageNumber} de {page_count}"
        self.line(50, 42, A4[0] - 50, 42)
        self.drawString(50, 30, footer_left)
        self.drawRightString(A4[0] - 50, 30, footer_right)
        self.restoreState()

def generate_document_pdf():
    pdf_path = os.path.join(curr_dir, "Tarea0_Memorix_Kevin.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    s_title = ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=28, leading=32, textColor=colors.HexColor("#050C26"), alignment=1)
    s_sub = ParagraphStyle('CoverSub', fontName='Helvetica-Oblique', fontSize=12.5, leading=16, textColor=colors.HexColor("#0038FF"), alignment=1)
    s_badge = ParagraphStyle('CoverBadge', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor("#009688"), alignment=1)
    s_meta = ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=11, leading=16, textColor=colors.HexColor("#232F3E"), alignment=1)

    s_h1 = ParagraphStyle('Heading1', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor("#050C26"), spaceBefore=7, spaceAfter=3)
    s_body = ParagraphStyle('BodyTextCustom', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#2C3E50"), alignment=4, spaceAfter=4)
    s_toc = ParagraphStyle('TOCItem', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor("#050C26"), spaceAfter=2)
    s_cap = ParagraphStyle('Caption', fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=colors.HexColor("#64748B"), alignment=1, spaceAfter=3)
    s_ref = ParagraphStyle('RefText', fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor("#2C3E50"), spaceAfter=2)

    story = []

    # ========================== PÁGINA 1: PORTADA ==========================
    story.append(Spacer(1, 15))
    logo_path = os.path.join(curr_dir, "logo_memorix_light.png")
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=1.5*inch, height=1.5*inch))
        story.append(Spacer(1, 8))

    story.append(Paragraph("PROYECTO INTERMODULAR • 2º DAM", s_badge))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Memorix", s_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Asistente Móvil de Tratamientos Farmacológicos y Rehabilitación Muscular Guiada", s_sub))
    story.append(Spacer(1, 12))
    story.append(Paragraph("—" * 28, ParagraphStyle('Div', fontName='Helvetica', fontSize=11, textColor=colors.HexColor("#CBD5E1"), alignment=1)))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Tarea 0: Una Solución Digital para un Problema Real</b><br/><font color='#64748B'>Propuesta Inicial y Definición del Proyecto Intermodular</font>", s_meta))
    story.append(Spacer(1, 60))

    meta_html = (
        "<b>Nombre y apellidos:</b> Kevin Muñoz Córcoles<br/>"
        "<b>Curso:</b> 2º Desarrollo de Aplicaciones Multiplataforma (DAM)<br/>"
        "<b>Módulo:</b> Proyecto Intermodular | Convocatoria 2026/2027"
    )
    story.append(Paragraph(meta_html, s_meta))
    story.append(PageBreak())

    # ========================== PÁGINA 2: CONTENIDO 1 ==========================
    story.append(Paragraph("Índice de Contenidos", s_h1))
    story.append(Spacer(1, 2))
    tocs = [
        ("1. Problema o Necesidad Detectada", "Pág. 2"),
        ("2. Propuesta de Solución Digital: Memorix", "Pág. 2"),
        ("3. Funcionalidades del Sistema", "Pág. 3"),
        ("4. Mejora Futura y Escalabilidad", "Pág. 3"),
        ("5. Prototipo e Identidad Visual", "Pág. 3"),
        ("6. Fuentes y Referencias Consultadas", "Pág. 3"),
    ]
    for tit, pag in tocs:
        dots = ". " * 38
        story.append(Paragraph(f"<b>{tit}</b> <font color='#94A3B8'>{dots}</font> <b>{pag}</b>", s_toc))

    story.append(Spacer(1, 6))
    story.append(Paragraph("1. Problema o Necesidad Detectada", s_h1))
    story.append(Paragraph(
        "<b>• ¿Qué ocurre?</b> El problema principal que he detectado surge de dos dificultades muy habituales en la vida diaria: los olvidos en la medicación y el abandono de la rehabilitación física en casa. En tratamientos de media o larga duración, muchas personas olvidan tomas o confunden las horas, lo que hace que los medicamentos no hagan el efecto deseado. Además, los prospectos médicos suelen tener una letra diminuta y explicaciones técnicas difíciles de entender para la mayoría de la gente. Al mismo tiempo, cuando una persona sufre una lesión muscular, un esguince o dolores de espalda por malas posturas o traumatismos, el médico o fisioterapeuta suele darle una hoja de papel con ejercicios para hacer en casa. En la práctica, esa hoja casi siempre termina perdiéndose o el paciente no recuerda bien cómo hacer el movimiento, por lo que acaba dejando de hacerlos y la recuperación se alarga.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• ¿A quién afecta?</b> Esta situación afecta de forma directa a personas mayores que toman varias pastillas al día y a pacientes en fases iniciales de Alzheimer o deterioro cognitivo leve, que todavía mantienen autonomía en casa pero necesitan ayuda para no equivocarse. También repercute intensamente en sus familiares y cuidadores, que sufren la preocupación constante de no saber si se han tomado las pastillas a tiempo. En la parte física, afecta a deportistas, trabajadores con sobrecargas o cualquier persona en recuperación de un traumatismo que necesita fortalecer músculos específicos.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• ¿Por qué debería mejorarse?</b> Conviene mejorar esta situación porque un error en la dosis o una toma omitida de medicamentos para la tensión o el corazón puede provocar un ingreso hospitalario evitable. En el plano físico, no realizar bien la rehabilitación puede cronificar una lesión. Hoy en día casi todo el mundo tiene un móvil a mano, por lo que podemos sustituir los papeles y los pastilleros de plástico por una herramienta accesible con avisos sonoros hablados y vídeos sencillos de ejercicios. Esta propuesta conecta directamente con el <b>ODS 3 (Salud y Bienestar)</b> y el <b>ODS 10 (Reducción de las Desigualdades)</b>.",
        s_body
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Propuesta de Solución Digital: Memorix", s_h1))
    story.append(Paragraph(
        "<b>• Explicación de la idea:</b> Memorix es una aplicación móvil multiplataforma (diseñada para Android e iOS) pensada específicamente para ser muy intuitiva y limpia. Integra en un mismo lugar la gestión de los tratamientos farmacológicos diarios y una guía de ejercicios activos de fortalecimiento muscular, todo ello bajo una interfaz adaptada con botones grandes y colores de alto contraste que facilitan su lectura a personas con dificultades visuales o mayores.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• ¿Qué permitiría hacer?</b> La aplicación permite registrar la medicación con alarmas que suenan de forma clara y que además reproducen por voz qué pastilla toca y cómo tomarla (por ejemplo: 'Toca tomar Enalapril, una pastilla con un vaso de agua después de comer'). Incluye un botón grande para confirmar la toma y avisa automáticamente al cuidador si pasan más de 20 minutos sin confirmarse. En la parte física, ofrece un catálogo de ejercicios guiados con temporizador y demostraciones visuales para zonas concretas como hombros, espalda, cuello o piernas tras un traumatismo o sobrecarga.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• ¿Quién utilizaría la solución?</b> La utilizarán principalmente: 1) Personas mayores o con despistes frecuentes que necesitan un recordatorio claro; 2) Cuidadores y familiares que supervisan a distancia el cumplimiento del tratamiento; 3) Personas de cualquier edad en recuperación física que necesitan tablas guiadas de ejercicios musculares para hacer en su domicilio.",
        s_body
    ))
    story.append(PageBreak())

    # ========================== PÁGINA 3: CONTENIDO 2 ==========================
    story.append(Paragraph("3. Funcionalidades del Sistema", s_h1))
    
    t_data = [
        [Paragraph("<b>Funcionalidad</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
         Paragraph("<b>Descripción</b>", ParagraphStyle('THD', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white))],
        [Paragraph("<b>Perfiles de Paciente y Cuidador</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Permite configurar un modo fácil para el paciente y vincularlo con el móvil del familiar para supervisión a distancia.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Alarmas con Locución por Voz</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Avisos sonoros que leen en voz alta el nombre del medicamento, la dosis y consejos claros de toma (ej. tomar con comida).", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Confirmación de Toma y Registro</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Botón táctil grande para confirmar la ingesta; guarda la hora exacta para evitar tomas dobles accidentales.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Aviso de Seguridad al Cuidador</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Envía una alerta automática al móvil del cuidador si pasan 20 minutos desde la alarma sin confirmación de la toma.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Ejercicios Musculares Guiados</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Rutinas visuales para dolores o traumatismos (cuello, espalda, hombro, pierna) con temporizador, series y descansos.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Modo Contraste Accesible</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Esquemas de color de alto contraste (azul marino, cian, menta y blanco) diseñados para máxima legibilidad visual.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))]
    ]
    t_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#050C26")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F1F5F9"), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ])
    tab = Table(t_data, colWidths=[150, 345], style=t_style)
    story.append(tab)

    story.append(Spacer(1, 4))
    story.append(Paragraph("4. Mejora Futura y Escalabilidad", s_h1))
    story.append(Paragraph(
        "<b>• Evolución prevista:</b> Como mejora futura para más adelante, la idea es incorporar visión artificial (Computer Vision) usando la cámara frontal del teléfono. De este modo, mientras el paciente realiza los ejercicios de rehabilitación delante del móvil, la aplicación podrá evaluar en tiempo real la postura del cuerpo y avisarle por voz si está curvando mal la espalda o forzando la articulación, evitando nuevas lesiones. Además, se contempla la vinculación con pulseras inteligentes (smartwatch) para avisar de las pastillas mediante vibración en la muñeca y detectar posibles caídas en personas mayores.",
        s_body
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("5. Prototipo e Identidad Visual de la Propuesta", s_h1))
    mockup_path = os.path.join(curr_dir, "mockup_memorix.jpg")
    if os.path.exists(mockup_path):
        story.append(Image(mockup_path, width=4.0*inch, height=2.25*inch))
        story.append(Spacer(1, 2))
        story.append(Paragraph("Figura 1: Prototipo de Memorix mostrando la alarma con audio-guía y la rutina de ejercicios con temporizador.", s_cap))

    story.append(Spacer(1, 3))
    story.append(Paragraph("6. Fuentes y Referencias Consultadas", s_h1))
    story.append(Paragraph("• <b>Organización Mundial de la Salud (OMS):</b> <font color='#0B7285'><u>https://www.who.int</u></font> — Informe sobre adherencia a los tratamientos a largo plazo.", s_ref))
    story.append(Paragraph("• <b>Sociedad Española de Geriatría y Gerontología (SEGG):</b> <font color='#0B7285'><u>https://www.segg.es</u></font> — Guía de buena práctica clínica en polimedicación en el anciano.", s_ref))
    story.append(Paragraph("• <b>Naciones Unidas:</b> <font color='#0B7285'><u>https://www.un.org/sustainabledevelopment/es/health/</u></font> — Objetivo de Desarrollo Sostenible 3: Salud y Bienestar.", s_ref))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF Document generated successfully at:", pdf_path)

# =========================================================================
# 2. GENERAR PRESENTACIÓN PDF (3 DIAPOSITIVAS PANORÁMICAS 16:9 EXACTAS)
# =========================================================================
def generate_presentation_pdf():
    pptx_pdf_path = os.path.join(curr_dir, "Tarea0_Memorix_Presentacion.pdf")
    w, h = 13.333 * inch, 7.5 * inch
    c = canvas.Canvas(pptx_pdf_path, pagesize=(w, h))

    # Paleta Memorix
    c_navy = colors.HexColor("#050C26")
    c_mint = colors.HexColor("#00B496")
    c_blue = colors.HexColor("#0038FF")
    c_coral = colors.HexColor("#E05624")
    c_bg = colors.HexColor("#F8FAFC")
    c_white = colors.white
    c_border = colors.HexColor("#CBD5E1")
    c_text = colors.HexColor("#232F3E")
    c_muted = colors.HexColor("#64748B")

    def draw_slide_base(num_str, tag_str, title_str, sub_str):
        c.setFillColor(c_bg)
        c.rect(0, 0, w, h, fill=True, stroke=False)

        # Top mint line
        c.setFillColor(c_mint)
        c.rect(0, h - 8, w, 8, fill=True, stroke=False)

        # Nav bar
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.8 * inch, h - 35, "Memorix  •  Proyecto Intermodular 2º DAM")
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(c_muted)
        c.drawRightString(w - 0.8 * inch, h - 35, num_str)

        # Titles
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(c_navy)
        c.drawString(0.8 * inch, h - 75, title_str)
        c.setFont("Helvetica", 13)
        c.setFillColor(c_muted)
        c.drawString(0.8 * inch, h - 98, sub_str)

    # ------------------ SLIDE 1: EL PROBLEMA ------------------
    draw_slide_base("01 / 03  •  EL PROBLEMA", "DIAGNÓSTICO DEL PROBLEMA", "1. Diagnóstico del Problema y Colectivos Afectados", "¿Qué ocurre en la vida cotidiana y a quién afecta directamente?")

    # Card 1 (Left)
    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(0.8 * inch, 1.3 * inch, 5.6 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(c_coral)
    c.drawString(1.1 * inch, 5.4 * inch, "🚨 ¿QUÉ OCURRE?")

    items1 = [
        ("Olvidos y Confusión en la Medicación", "Casi el 50% de pacientes crónicos no toma bien su tratamiento (OMS), provocando recaídas y visitas a urgencias."),
        ("Dificultad con Posologías y Prospectos", "La letra diminuta y las explicaciones técnicas confunden al paciente sobre cómo y cuándo tomar cada pastilla."),
        ("Abandono de la Rehabilitación en Casa", "Las hojas de papel con ejercicios para dolores musculares o traumatismos se extravían y no guían la postura correcta.")
    ]
    y_pos = 4.8 * inch
    for tit, desc in items1:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(c_navy)
        c.drawString(1.1 * inch, y_pos, f"• {tit}:")
        y_pos -= 18
        c.setFont("Helvetica", 10.5)
        c.setFillColor(c_text)
        # wrap text simply
        words = desc.split()
        l1, l2 = "", ""
        for wd in words:
            if len(l1) + len(wd) < 55:
                l1 += wd + " "
            else:
                l2 += wd + " "
        c.drawString(1.3 * inch, y_pos, l1.strip())
        y_pos -= 16
        if l2:
            c.drawString(1.3 * inch, y_pos, l2.strip())
            y_pos -= 18
        else:
            y_pos -= 4

    # Card 2 (Right)
    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(6.8 * inch, 1.3 * inch, 5.7 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(c_blue)
    c.drawString(7.1 * inch, 5.4 * inch, "👥 ¿A QUIÉN AFECTA?")

    items2 = [
        ("Personas Mayores y Pacientes con Olvidos", "Especialmente vulnerables por polimedicación o principios de Alzheimer y deterioro cognitivo leve."),
        ("Familiares y Cuidadores", "Viven con la preocupación y el estrés diario de tener que estar comprobando si se han tomado la medicación."),
        ("Personas con Lesiones Musculares o Dolor", "Pacientes en recuperación de traumatismos, contracturas o con dolores de espalda que necesitan guías de ejercicios.")
    ]
    y_pos = 4.8 * inch
    for tit, desc in items2:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(c_navy)
        c.drawString(7.1 * inch, y_pos, f"• {tit}:")
        y_pos -= 18
        c.setFont("Helvetica", 10.5)
        c.setFillColor(c_text)
        words = desc.split()
        l1, l2 = "", ""
        for wd in words:
            if len(l1) + len(wd) < 55:
                l1 += wd + " "
            else:
                l2 += wd + " "
        c.drawString(7.3 * inch, y_pos, l1.strip())
        y_pos -= 16
        if l2:
            c.drawString(7.3 * inch, y_pos, l2.strip())
            y_pos -= 18
        else:
            y_pos -= 4

    # Bottom Banner Slide 1
    c.setFillColor(c_navy)
    c.rect(0.8 * inch, 0.45 * inch, 11.7 * inch, 0.55 * inch, fill=True, stroke=False)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(c_white)
    c.drawCentredString(w / 2.0, 0.65 * inch, "💡 IMPACTO: Alineado con ODS 3 (Salud y Bienestar) y ODS 10 (Reducción de las Desigualdades)")
    c.showPage()

    # ------------------ SLIDE 2: LA SOLUCIÓN ------------------
    draw_slide_base("02 / 03  •  LA SOLUCIÓN", "PROPUESTA DIGITAL", "2. Memorix: Propuesta Digital y Funcionalidades", "Asistente móvil accesible para el control de medicamentos y ejercicios de recuperación")

    mockup_path = os.path.join(curr_dir, "mockup_memorix.jpg")
    if os.path.exists(mockup_path):
        c.drawImage(mockup_path, 0.8 * inch, 1.3 * inch, width=5.5 * inch, height=4.6 * inch, preserveAspectRatio=True)

    # Card Right
    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(6.6 * inch, 1.3 * inch, 5.9 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(c_navy)
    c.drawString(6.9 * inch, 5.4 * inch, "⚡ FUNCIONALIDADES CLAVE")

    funcs = [
        ("🔊 Alarmas con Locución por Voz", "Lee en voz alta el nombre de la pastilla, la dosis y cómo tomarla (ej. con comida)."),
        ("👆 Confirmación Fácil de Un Toque", "Botón táctil grande para registrar la toma y evitar tomar la pastilla dos veces."),
        ("🛡️ Aviso Automático al Cuidador", "Manda una alerta al móvil del familiar si pasan 20 minutos sin confirmarse la toma."),
        ("🏋️ Rutinas Musculares Guiadas", "Ejercicios para dolores o traumatismos con temporizador, series y descansos."),
        ("🎨 Interfaz de Alto Contraste", "Tipografía clara y colores contrastados pensados para personas mayores o con poca vista.")
    ]
    y_pos = 4.9 * inch
    for tit, desc in funcs:
        c.setFont("Helvetica-Bold", 11.5)
        c.setFillColor(c_mint)
        c.drawString(6.9 * inch, y_pos, tit)
        y_pos -= 16
        c.setFont("Helvetica", 9.5)
        c.setFillColor(c_text)
        c.drawString(7.1 * inch, y_pos, desc)
        y_pos -= 22

    # Bottom Banner Slide 2
    c.setFillColor(c_navy)
    c.rect(0.8 * inch, 0.45 * inch, 11.7 * inch, 0.55 * inch, fill=True, stroke=False)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(c_white)
    c.drawCentredString(w / 2.0, 0.65 * inch, "📱 Solución Multiplataforma (Android / iOS) • Modo Fácil Diseñado para la Tercera Edad")
    c.showPage()

    # ------------------ SLIDE 3: VALOR AÑADIDO ------------------
    draw_slide_base("03 / 03  •  VALOR AÑADIDO", "VALOR E INNOVACIÓN", "3. Valor Diferencial y Mejoras Futuras", "¿Por qué resulta útil esta solución y cómo puede evolucionar?")

    # Card 1 (Left)
    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(0.8 * inch, 1.3 * inch, 5.6 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(c_mint)
    c.drawString(1.1 * inch, 5.4 * inch, "🌟 VALOR AÑADIDO (¿POR QUÉ ES ÚTIL?)")

    vals = [
        ("Solución 2 en 1 (Medicamentos + Ejercicio)", "Une en una sola aplicación el control de los tratamientos y la recuperación física activa."),
        ("Mayor Autonomía para Personas Mayores", "Las explicaciones por voz y los botones grandes permiten manejarse sin depender siempre de otro."),
        ("Tranquilidad para los Familiares", "Supervisión sin agobios; solo reciben alerta en el móvil si su familiar olvida una toma."),
        ("Constancia en la Rehabilitación", "Las guías visuales con cronómetro ayudan a no abandonar los ejercicios musculares en casa.")
    ]
    y_pos = 4.8 * inch
    for tit, desc in vals:
        c.setFont("Helvetica-Bold", 11.5)
        c.setFillColor(c_navy)
        c.drawString(1.1 * inch, y_pos, f"✔ {tit}:")
        y_pos -= 16
        c.setFont("Helvetica", 10)
        c.setFillColor(c_text)
        c.drawString(1.3 * inch, y_pos, desc)
        y_pos -= 20

    # Card 2 (Right)
    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(6.8 * inch, 1.3 * inch, 5.7 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(c_blue)
    c.drawString(7.1 * inch, 5.4 * inch, "🚀 MEJORAS FUTURAS PREVISTAS")

    futs = [
        ("Visión Artificial con Cámara Móvil", "Detección de la postura del usuario en tiempo real durante los ejercicios para avisar por voz si la espalda está mal colocada."),
        ("Conexión con Pulseras Inteligentes (Smartwatch)", "Avisos de medicación por vibración en la muñeca y detección de caídas accidentales en ancianos."),
        ("Escaneo de Cajas de Medicamentos", "Reconocimiento automático de la pastilla con la cámara para añadir la alarma sin tener que escribir.")
    ]
    y_pos = 4.8 * inch
    for tit, desc in futs:
        c.setFont("Helvetica-Bold", 11.5)
        c.setFillColor(c_navy)
        c.drawString(7.1 * inch, y_pos, f"✦ {tit}:")
        y_pos -= 16
        c.setFont("Helvetica", 10)
        c.setFillColor(c_text)
        words = desc.split()
        l1, l2 = "", ""
        for wd in words:
            if len(l1) + len(wd) < 55:
                l1 += wd + " "
            else:
                l2 += wd + " "
        c.drawString(7.3 * inch, y_pos, l1.strip())
        y_pos -= 15
        if l2:
            c.drawString(7.3 * inch, y_pos, l2.strip())
            y_pos -= 18
        else:
            y_pos -= 5

    # Bottom Banner Slide 3
    c.setFillColor(c_navy)
    c.rect(0.8 * inch, 0.45 * inch, 11.7 * inch, 0.55 * inch, fill=True, stroke=False)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(c_white)
    c.drawCentredString(w / 2.0, 0.65 * inch, "🎯 MEMORIX  •  Proyecto Intermodular 2º DAM  •  Kevin Muñoz Córcoles")
    c.showPage()

    c.save()
    print("PDF Presentation generated successfully at:", pptx_pdf_path)

if __name__ == "__main__":
    generate_document_pdf()
    generate_presentation_pdf()
