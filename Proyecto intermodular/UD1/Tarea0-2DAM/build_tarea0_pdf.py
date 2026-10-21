import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

curr_dir = r"c:\Users\kevin\OneDrive\Documentos\GitHub\Curso-Dam2\Proyecto intermodular\UD1\Tarea0-2DAM"

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

        header_text = "Proyecto Intermodular - 2º DAM  |  Tarea 0: LeadCraft AI"
        self.drawRightString(A4[0] - 50, A4[1] - 38, header_text)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(50, A4[1] - 44, A4[0] - 50, A4[1] - 44)

        footer_left = "LeadCraft AI  •  Kevin Muñoz Córcoles"
        footer_right = f"Página {self._pageNumber} de {page_count}"
        self.line(50, 42, A4[0] - 50, 42)
        self.drawString(50, 30, footer_left)
        self.drawRightString(A4[0] - 50, 30, footer_right)
        self.restoreState()

def generate_document_pdf():
    pdf_path = os.path.join(curr_dir, "Tarea0_LeadCraft_Kevin.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    s_title = ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=28, leading=32, textColor=colors.HexColor("#0A192F"), alignment=1)
    s_sub = ParagraphStyle('CoverSub', fontName='Helvetica-Oblique', fontSize=12, leading=16, textColor=colors.HexColor("#0038FF"), alignment=1)
    s_badge = ParagraphStyle('CoverBadge', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor("#00B496"), alignment=1)
    s_meta = ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=11, leading=16, textColor=colors.HexColor("#232F3E"), alignment=1)

    s_h1 = ParagraphStyle('Heading1', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor("#0A192F"), spaceBefore=7, spaceAfter=3)
    s_body = ParagraphStyle('BodyTextCustom', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#2C3E50"), alignment=4, spaceAfter=4)
    s_toc = ParagraphStyle('TOCItem', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor("#0A192F"), spaceAfter=2)
    s_cap = ParagraphStyle('Caption', fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=colors.HexColor("#64748B"), alignment=1, spaceAfter=3)
    s_ref = ParagraphStyle('RefText', fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor("#2C3E50"), spaceAfter=2)

    story = []

    # PORTADA
    story.append(Spacer(1, 40))
    story.append(Paragraph("PROYECTO INTERMODULAR • 2º DAM", s_badge))
    story.append(Spacer(1, 4))
    story.append(Paragraph("LeadCraft AI", s_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Plataforma Inteligente de Prospección Geográfica, Auditoría Digital y Generación Asistida de Soluciones Web para Pequeños Negocios", s_sub))
    story.append(Spacer(1, 14))
    story.append(Paragraph("—" * 28, ParagraphStyle('Div', fontName='Helvetica', fontSize=11, textColor=colors.HexColor("#CBD5E1"), alignment=1)))
    story.append(Spacer(1, 14))
    story.append(Paragraph("<b>Tarea 0: Una Solución Digital para un Problema Real</b><br/><font color='#64748B'>Propuesta Inicial y Definición del Proyecto Intermodular</font>", s_meta))
    story.append(Spacer(1, 120))

    meta_html = (
        "<b>Nombre y apellidos:</b> Kevin Muñoz Córcoles<br/>"
        "<b>Curso:</b> 2º Desarrollo de Aplicaciones Multiplataforma (DAM)<br/>"
        "<b>Módulo:</b> Proyecto Intermodular | Convocatoria 2026/2027"
    )
    story.append(Paragraph(meta_html, s_meta))
    story.append(PageBreak())

    # PÁGINA 2
    story.append(Paragraph("Índice de Contenidos", s_h1))
    story.append(Spacer(1, 2))
    tocs = [
        ("1. Problema o Necesidad Detectada", "Pág. 2"),
        ("2. Propuesta de Solución Digital: LeadCraft AI", "Pág. 2"),
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
        "<b>• ¿Qué ocurre?</b> En nuestras ciudades y barrios existen miles de pequeños comercios (peluquerías, talleres mecánicos, clínicas de fisioterapia o pequeños restaurantes) que tienen una presencia digital prácticamente inexistente o muy descuidada. La mayoría aparecen registrados en Google Maps pero carecen de página web propia, no disponen de un sistema para reservar citas online y dependen de llamadas telefónicas mientras atienden a sus clientes. Esto les hace perder ventas a diario frente a grandes franquicias. Al mismo tiempo, los profesionales y pequeñas agencias que se dedican a crear páginas web invierten semanas buscando clientes 'puerta a puerta', auditando sus carencias a mano y presentando presupuestos en frío que rara vez se aceptan porque el comerciante no visualiza el resultado final.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• ¿A quién afecta?</b> Afecta principalmente a dos perfiles: por un lado, a los dueños de pequeños negocios y pymes locales, que no tienen tiempo, presupuesto ni conocimientos técnicos para contratar agencias de marketing tradicionales (cuyos costes suelen superar los 1.000€). Por otro lado, a jóvenes desarrolladores, diseñadores freelance y consultores comerciales que buscan clientes locales pero carecen de una herramienta rápida para identificar oportunidades de negocio en su zona y mostrar propuestas ya construidas.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• ¿Por qué debería mejorarse?</b> Mejorar esta situación es fundamental para revitalizar el comercio de barrio. Si un comercial o desarrollador puede detectar en segundos qué le falta a un negocio y presentarse con una web ya maquetada y lista para funcionar, la probabilidad de contratación se multiplica. Este proyecto impacta directamente en el <b>ODS 8 (Trabajo decente y crecimiento económico)</b>, al fomentar la competitividad de las microempresas locales, y en el <b>ODS 9 (Industria, innovación e infraestructura)</b>, al democratizar el acceso a la tecnología digital para el pequeño comercio.",
        s_body
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Propuesta de Solución Digital: LeadCraft AI", s_h1))
    story.append(Paragraph(
        "<b>• Explicación de la idea:</b> LeadCraft AI es una aplicación multiplataforma (escritorio y web) que combina la exploración de mapas de Google con inteligencia artificial generativa. Permite navegar por cualquier barrio o código postal, seleccionar comercios locales y analizar automáticamente qué carencias digitales tienen, generando al instante una landing page moderna con sistema de citas online y contacto por WhatsApp lista para enseñar al cliente.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• ¿Qué permitiría hacer?</b> La aplicación permite: 1) Buscar negocios en el mapa filtrando por categoría (ej. barberías en Madrid); 2) Ejecutar una 'Auditoría Digital Express' que comprueba si tienen web, SSL, reservas online o redes sociales; 3) Conectar con un modelo de IA (API de Gemini/OpenAI) para redactar el contenido y personalizar una plantilla web profesional con los datos de Google Maps (fotos, horarios, reseñas); 4) Probar la web generada en un previsualizador en vivo con widget de citas; 5) Exportar el sitio web en código limpio y generar un dossier PDF de propuesta comercial.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• ¿Quién utilizaría la solución?</b> El sistema está dirigido a freelancers, comerciales y agencias de desarrollo web que buscan clientes de proximidad, así como a asociaciones de comerciantes que quieran impulsar la transformación digital de sus negocios locales de forma asequible.",
        s_body
    ))
    story.append(PageBreak())

    # PÁGINA 3
    story.append(Paragraph("3. Funcionalidades del Sistema", s_h1))
    
    t_data = [
        [Paragraph("<b>Funcionalidad</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
         Paragraph("<b>Descripción</b>", ParagraphStyle('THD', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white))],
        [Paragraph("<b>Búsqueda Geográfica en Maps</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Permite explorar zonas concretas sobre Google Maps y localizar comercios locales clasificados por sector (barberías, clínicas, hostelería).", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Motor de Auditoría Express</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Escanea en tiempo real si el comercio tiene web activa, certificado HTTPS, enlace de reservas, puntuación de reseñas y teléfono.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Generador Web con IA</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Una API de IA redacta textos comerciales, selecciona servicios y ensambla una landing page moderna usando datos de Maps.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Widget Integrado de Citas</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Incuba un calendario de citas con franjas horarias y confirmación en la web generada, resolviendo la gestión de reservas.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Previsualizador en Vivo</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Permite ver el resultado en vista móvil y escritorio, retocar precios, horarios o colores antes de generar la propuesta final.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Dossier Comercial y Exportación</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Genera un informe descargable de auditoría en PDF y exporta el código HTML/Tailwind en un archivo ZIP listo para publicar.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))]
    ]
    t_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A192F")),
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
        "<b>• Evolución prevista:</b> Como ampliación futura se prevé integrar un bot conversacional de WhatsApp conectado a la API de IA que atienda dudas y gestione las reservas de los clientes de forma automática 24/7. Además, se incorporará la conexión directa con pasarelas de pago (Stripe) para permitir el cobro de fianzas o citas online y el despliegue automático del sitio web con un solo clic en servidores cloud como Vercel o Netlify con dominio personalizado.",
        s_body
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("5. Prototipo e Identidad Visual de la Propuesta", s_h1))
    mockup_path = os.path.join(curr_dir, "mockup_leadcraft.jpg")
    if os.path.exists(mockup_path):
        story.append(Image(mockup_path, width=4.0*inch, height=2.25*inch))
        story.append(Spacer(1, 2))
        story.append(Paragraph("Figura 1: Prototipo de LeadCraft AI mostrando el mapa de prospección y la auditoría digital de un negocio local.", s_cap))

    story.append(Spacer(1, 3))
    story.append(Paragraph("6. Fuentes y Referencias Consultadas", s_h1))
    story.append(Paragraph("• <b>Instituto Nacional de Estadística (INE):</b> <font color='#0B7285'><u>https://www.ine.es</u></font> — Encuesta sobre el uso de TIC y comercio electrónico en empresas españolas.", s_ref))
    story.append(Paragraph("• <b>Google Cloud Platform:</b> <font color='#0B7285'><u>https://developers.google.com/maps</u></font> — Documentación de Google Places API.", s_ref))
    story.append(Paragraph("• <b>Naciones Unidas:</b> <font color='#0B7285'><u>https://www.un.org/sustainabledevelopment/es/economic-growth/</u></font> — ODS 8: Trabajo Decente y Crecimiento Económico.", s_ref))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF Tarea 0 LeadCraft saved at:", pdf_path)

def generate_presentation_pdf():
    pptx_pdf_path = os.path.join(curr_dir, "Tarea0_LeadCraft_Presentacion.pdf")
    w, h = 13.333 * inch, 7.5 * inch
    c = canvas.Canvas(pptx_pdf_path, pagesize=(w, h))

    c_navy = colors.HexColor("#0A192F")
    c_cyan = colors.HexColor("#00B496")
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
        c.setFillColor(c_cyan)
        c.rect(0, h - 8, w, 8, fill=True, stroke=False)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.8 * inch, h - 35, "LeadCraft AI  •  Proyecto Intermodular 2º DAM")
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(c_muted)
        c.drawRightString(w - 0.8 * inch, h - 35, num_str)

        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(c_navy)
        c.drawString(0.8 * inch, h - 75, title_str)
        c.setFont("Helvetica", 13)
        c.setFillColor(c_muted)
        c.drawString(0.8 * inch, h - 98, sub_str)

    # SLIDE 1
    draw_slide_base("01 / 03  •  EL PROBLEMA", "DIAGNÓSTICO DEL PROBLEMA", "1. Diagnóstico del Problema y Colectivos Afectados", "¿Qué ocurre con la digitalización de los pequeños comercios locales?")

    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(0.8 * inch, 1.3 * inch, 5.6 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(c_coral)
    c.drawString(1.1 * inch, 5.4 * inch, "🚨 ¿QUÉ OCURRE?")

    items1 = [
        ("Desconexión Digital en el Barrio", "Miles de negocios locales solo tienen ficha en Google Maps pero carecen de web propia o citas online."),
        ("Barreras de Coste y Tiempo", "Las agencias tradicionales cobran entre 800€ y 2.500€, un coste inasumible para pequeños comercios."),
        ("Prospección Lenta e Ineficiente", "Los comerciales pierden semanas contactando en frío sin una propuesta visual que convenza al dueño.")
    ]
    y_pos = 4.8 * inch
    for tit, desc in items1:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(c_navy)
        c.drawString(1.1 * inch, y_pos, f"• {tit}:")
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
        c.drawString(1.3 * inch, y_pos, l1.strip())
        y_pos -= 16
        if l2:
            c.drawString(1.3 * inch, y_pos, l2.strip())
            y_pos -= 18
        else:
            y_pos -= 4

    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(6.8 * inch, 1.3 * inch, 5.7 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(c_blue)
    c.drawString(7.1 * inch, 5.4 * inch, "👥 ¿A QUIÉN AFECTA?")

    items2 = [
        ("Pymes y Comercios Locales", "Peluquerías, talleres, clínicas y bares que pierden clientes frente a franquicias por no tener reservas."),
        ("Freelancers y Jóvenes Desarrolladores", "Buscan captar clientes de proximidad pero carecen de herramientas para auditar y generar demos rápidas."),
        ("Economía Local y ODS 8", "El comercio tradicional pierde competitividad. Resolverlo impulsa el ODS 8 y el ODS 9 (innovación accesible).")
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

    c.setFillColor(c_navy)
    c.rect(0.8 * inch, 0.45 * inch, 11.7 * inch, 0.55 * inch, fill=True, stroke=False)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(c_white)
    c.drawCentredString(w / 2.0, 0.65 * inch, "💡 IMPACTO: Alineado con ODS 8 (Trabajo Decente y Crecimiento Económico) y ODS 9 (Innovación en Pymes)")
    c.showPage()

    # SLIDE 2
    draw_slide_base("02 / 03  •  LA SOLUCIÓN", "PROPUESTA DIGITAL", "2. LeadCraft AI: Propuesta Digital y Funcionalidades", "Plataforma de prospección sobre Google Maps con auditoría y generador web con IA")

    mockup_path = os.path.join(curr_dir, "mockup_leadcraft.jpg")
    if os.path.exists(mockup_path):
        c.drawImage(mockup_path, 0.8 * inch, 1.3 * inch, width=5.5 * inch, height=4.6 * inch, preserveAspectRatio=True)

    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(6.6 * inch, 1.3 * inch, 5.9 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(c_navy)
    c.drawString(6.9 * inch, 5.4 * inch, "⚡ FUNCIONALIDADES CLAVE")

    funcs = [
        ("🗺️ Explorador Geográfico en Google Maps", "Localiza comercios por zona y sector (ej. peluquerías en Chamberí)."),
        ("🔍 Auditoría Digital Express en 3s", "Detecta si el local tiene web, SSL, reservas, redes y analiza reseñas."),
        ("🤖 Generador de Landing Pages con IA", "Redacta contenido y monta la web usando datos de Maps (horarios, fotos)."),
        ("📅 Widget Integrado de Citas Online", "Incuba un calendario de citas con franjas horarias y botón de confirmación."),
        ("💬 Dossier Comercial y Enlace WhatsApp", "Genera informe PDF de auditoría y mensaje listo para enviar al dueño.")
    ]
    y_pos = 4.9 * inch
    for tit, desc in funcs:
        c.setFont("Helvetica-Bold", 11.5)
        c.setFillColor(c_cyan)
        c.drawString(6.9 * inch, y_pos, tit)
        y_pos -= 16
        c.setFont("Helvetica", 9.5)
        c.setFillColor(c_text)
        c.drawString(7.1 * inch, y_pos, desc)
        y_pos -= 22

    c.setFillColor(c_navy)
    c.rect(0.8 * inch, 0.45 * inch, 11.7 * inch, 0.55 * inch, fill=True, stroke=False)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(c_white)
    c.drawCentredString(w / 2.0, 0.65 * inch, "🚀 Solución B2B SaaS • Arquitectura Modular y Aceleración con IA Generativa")
    c.showPage()

    # SLIDE 3
    draw_slide_base("03 / 03  •  VALOR AÑADIDO", "VALOR E INNOVACIÓN", "3. Valor Diferencial y Mejoras Futuras", "¿Por qué resulta útil esta solución y hacia dónde evoluciona?")

    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(0.8 * inch, 1.3 * inch, 5.6 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(c_cyan)
    c.drawString(1.1 * inch, 5.4 * inch, "🌟 VALOR AÑADIDO (¿POR QUÉ ES ÚTIL?)")

    vals = [
        ("Demos Ya Construidas", "En lugar de promesas abstractas, el comercial llega con la web del negocio terminada para enseñar."),
        ("Ahorro de Semanas de Trabajo", "Pasa de invertir 15 días en programar una web a generarla en 30 segundos con IA."),
        ("Digitalización Real para la Pyme", "El dueño del negocio obtiene web con citas por una fracción del precio habitual."),
        ("Generación de Nuevos Negocios", "Crea oportunidades laborales para jóvenes titulados de DAM en servicios digitales.")
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

    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(6.8 * inch, 1.3 * inch, 5.7 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(c_blue)
    c.drawString(7.1 * inch, 5.4 * inch, "🚀 MEJORAS FUTURAS PREVISTAS")

    futs = [
        ("Bot de WhatsApp con IA", "Atención automatizada 24/7 para responder preguntas y confirmar reservas por chat."),
        ("Pagos Integrados con Stripe", "Cobro de fianzas o citas online directamente en la web generada."),
        ("Despliegue Cloud en 1 Clic", "Publicación automatizada del código en Vercel/Netlify con dominio personalizado.")
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

    c.setFillColor(c_navy)
    c.rect(0.8 * inch, 0.45 * inch, 11.7 * inch, 0.55 * inch, fill=True, stroke=False)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(c_white)
    c.drawCentredString(w / 2.0, 0.65 * inch, "🎯 LEADCRAFT AI  •  Proyecto Intermodular 2º DAM  •  Kevin Muñoz Córcoles")
    c.showPage()

    c.save()
    print("PDF Presentation LeadCraft saved at:", pptx_pdf_path)

if __name__ == "__main__":
    generate_document_pdf()
    generate_presentation_pdf()
