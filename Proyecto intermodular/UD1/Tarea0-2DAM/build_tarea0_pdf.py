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

    s_h1 = ParagraphStyle('Heading1', fontName='Helvetica-Bold', fontSize=12.5, leading=15, textColor=colors.HexColor("#0A192F"), spaceBefore=5, spaceAfter=2)
    s_body = ParagraphStyle('BodyTextCustom', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor("#2C3E50"), alignment=4, spaceAfter=3)
    s_toc = ParagraphStyle('TOCItem', fontName='Helvetica', fontSize=9, leading=11.5, textColor=colors.HexColor("#0A192F"), spaceAfter=1)
    s_cap = ParagraphStyle('Caption', fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=colors.HexColor("#64748B"), alignment=1, spaceAfter=2)
    s_ref = ParagraphStyle('RefText', fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=colors.HexColor("#2C3E50"), spaceAfter=2)

    story = []

    # ========================== PÁGINA 1: PORTADA ==========================
    story.append(Spacer(1, 40))
    story.append(Paragraph("PROYECTO INTERMODULAR • 2º DAM", s_badge))
    story.append(Spacer(1, 4))
    story.append(Paragraph("LeadCraft AI", s_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Servicio Integral de Gestión y Presencia Online para Ayudar al Pequeño Comercio Local a Llevar su Negocio en Internet", s_sub))
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

    # ========================== PÁGINA 2: CONTENIDO 1 ==========================
    story.append(Paragraph("Índice de Contenidos", s_h1))
    story.append(Spacer(1, 2))
    tocs = [
        ("1. Problema o Necesidad Detectada", "Pág. 2"),
        ("2. Propuesta de Solución Digital: El Servicio LeadCraft AI", "Pág. 2"),
        ("3. Funcionalidades del Sistema", "Pág. 3"),
        ("4. Mejora Futura y Escalabilidad", "Pág. 3"),
        ("5. Prototipo e Identidad Visual", "Pág. 3"),
        ("6. Fuentes y Referencias Consultadas", "Pág. 3"),
    ]
    for tit, pag in tocs:
        dots = ". " * 38
        story.append(Paragraph(f"<b>{tit}</b> <font color='#94A3B8'>{dots}</font> <b>{pag}</b>", s_toc))

    story.append(Spacer(1, 4))
    story.append(Paragraph("1. Problema o Necesidad Detectada", s_h1))
    story.append(Paragraph(
        "<b>• ¿Qué ocurre?</b> En nuestros barrios existen miles de pequeños comercios (peluquerías, talleres, clínicas y tiendas de proximidad) que se ven desbordados para gestionar su presencia en Internet. La mayoría aparecen en Google Maps pero carecen de web propia, no disponen de citas online y dependen de atender llamadas mientras despachan en el mostrador, perdiendo ventas frente a grandes cadenas. Contratar agencias tradicionales resulta inviable (suelen cobrar más de 1.000€ iniciales y altas cuotas de mantenimiento), y los dueños carecen de tiempo y formación técnica para gestionarlo por su cuenta. Paralelamente, los profesionales y jóvenes desarrolladores que ofrecen servicios digitales invierten semanas contactando 'a puerta fría' sin una propuesta visual construida que convenza al dueño.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• ¿A quién afecta?</b> Afecta principalmente a los comerciantes y autónomos locales, que no pueden atender el mostrador físico y gestionar a la vez citas y mensajes en la red; a los vecinos y clientes locales, que no pueden reservar ni consultar precios fuera de horario; y a jóvenes titulados de DAM, que necesitan una herramienta ágil para empaquetar y vender este servicio de gestión digital a los negocios de su entorno.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• ¿Por qué debería mejorarse?</b> Resolver esta brecha es indispensable para la viabilidad del comercio tradicional. Venderles un servicio llave en mano y asequible que gestione su web y reservas online les permite competir en igualdad de condiciones con el comercio electrónico. Este proyecto impacta directamente en el ODS 8 (Trabajo decente y crecimiento económico), al fomentar la productividad de microempresas, y en el ODS 9 (Industria, innovación e infraestructura), al democratizar el acceso a la tecnología y la IA para negocios de proximidad.",
        s_body
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Propuesta de Solución Digital: El Servicio LeadCraft AI", s_h1))
    story.append(Paragraph(
        "<b>• Explicación de la idea:</b> LeadCraft AI es una plataforma de software diseñada para comercializar un servicio integral de digitalización y gestión online para comercios locales. El núcleo del proyecto consiste en vender un servicio activo de la aplicación que ayuda al comerciante a llevar su tienda en Internet: incluye el despliegue de su web profesional generada mediante IA, un gestor interactivo de citas y reservas en tiempo real, catálogo de servicios actualizado, canal directo de pedidos por WhatsApp y un panel intuitivo desde el móvil para consultar reservas del día sin complicaciones técnicas ni costes desproporcionados.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• ¿Qué permitiría hacer?</b> La solución permite: 1) Explorar negocios en Google Maps por sector y zona geográfica; 2) Auditar en 3 segundos sus carencias digitales (falta de web, citas online o redes); 3) Generar con una API de IA una web completa y personalizada con la información de Maps (fotos, horarios, servicios); 4) Activar un módulo interactivo de reservas y contacto por WhatsApp 24/7; 5) Facilitar al dueño un panel de control para gestionar citas diarias y precios; y 6) Empaquetar y vender esta solución bajo una suscripción mensual asequible de mantenimiento.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• ¿Quién utilizaría la solución?</b> El servicio está dirigido a los comerciantes y autónomos locales (los clientes del servicio, que obtienen una solución lista para gestionar su negocio online sin esfuerzo técnico), sus clientes finales (que reservan citas y compran desde el móvil), y el operador o consultor comercial (estudiante de DAM o desarrollador) que prospecta la zona y administra la implantación del servicio.",
        s_body
    ))

    story.append(PageBreak())

    # ========================== PÁGINA 3: CONTENIDO 2 ==========================
    story.append(Paragraph("3. Funcionalidades del Sistema", s_h1))
    story.append(Spacer(1, 2))

    t_data = [
        [Paragraph("<b>Funcionalidad</b>", ParagraphStyle('TH1', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
         Paragraph("<b>Descripción del Servicio</b>", ParagraphStyle('TH2', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white))],
        [Paragraph("<b>Búsqueda Geográfica y Auditoría</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Localiza comercios sobre Google Maps y analiza en tiempo real sus carencias digitales (ausencia de web, citas online o datos desactualizados).", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Generador Web con IA para Negocios</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("A partir de la ficha de Maps, una API de IA redacta textos comerciales, estructura los servicios y maqueta una web moderna y responsive.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Gestor Integrado de Citas y Reservas</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Incorpora un calendario interactivo con franjas horarias y confirmación inmediata para que los clientes reserven online 24/7.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Canal Directo de Contacto por WhatsApp</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Enlace automatizado que envía las consultas de clientes y solicitudes de servicio directamente al móvil del comerciante.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Panel de Control para el Comerciante</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Interfaz sencilla para consultar las reservas diarias, confirmar citas y actualizar precios u horarios desde cualquier dispositivo.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))],
        [Paragraph("<b>Dossier Comercial y Despliegue Cloud</b>", ParagraphStyle('TD1', fontName='Helvetica', fontSize=8.5, leading=11)),
         Paragraph("Genera informes descargables en PDF para la venta del servicio y permite exportar y publicar la web en servidores en la nube.", ParagraphStyle('TD2', fontName='Helvetica', fontSize=8.5, leading=11))]
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
        "<b>• Evolución prevista:</b> Como ampliación futura se prevé integrar un asistente virtual de WhatsApp impulsado por IA para atender preguntas frecuentes de los clientes y gestionar citas de forma automática las 24 horas del día. Además, se incorporará la pasarela de pagos con Stripe para permitir el cobro de señales de reserva o pedidos online y la sincronización bidireccional automática con la agenda de Google Calendar del negocio.",
        s_body
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("5. Prototipo e Identidad Visual de la Propuesta", s_h1))
    mockup_path = os.path.join(curr_dir, "mockup_leadcraft.jpg")
    if os.path.exists(mockup_path):
        story.append(Image(mockup_path, width=4.0*inch, height=2.25*inch))
        story.append(Spacer(1, 2))
        story.append(Paragraph("Figura 1: Prototipo de LeadCraft AI mostrando el buscador geográfico de comercios locales y el panel de auditoría para la venta del servicio digital.", s_cap))

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
    draw_slide_base("01 / 03  •  EL PROBLEMA", "DIAGNÓSTICO DEL PROBLEMA", "1. Diagnóstico del Problema y Colectivos Afectados", "¿Por qué los comercios locales tienen dificultades para llevar su negocio en Internet?")

    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(0.8 * inch, 1.3 * inch, 5.6 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(c_coral)
    c.drawString(1.1 * inch, 5.4 * inch, "🚨 ¿QUÉ OCURRE?")

    items1 = [
        ("Sobrecarga en la Tienda Física", "Los comerciantes atienden a clientes en local y carecen de tiempo para llevar citas, web y catálogo online."),
        ("Costes Inasumibles de Agencias", "Las agencias tradicionales cobran más de 1.000€ más cuotas altas, algo inviable para un negocio de barrio."),
        ("Pérdida Continua de Clientes", "Sin reservas online ni presencia digital cuidada, pierden ventas a diario frente a grandes franquicias.")
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
        ("Dueños de Tiendas y Comercios Locales", "Peluquerías, talleres, clínicas y bares que necesitan digitalizarse sin complicaciones técnicas."),
        ("Clientes y Vecinos del Barrio", "Buscan pedir cita, consultar precios y contactar desde el móvil 24/7 sin llamadas en horario comercial."),
        ("Titulados de DAM y Freelancers", "Oportunidad de ofrecer y vender un servicio recurrente de gestión digital 'llave en mano' en su entorno.")
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
    draw_slide_base("02 / 03  •  LA SOLUCIÓN", "PROPUESTA DIGITAL", "2. LeadCraft AI: Venta del Servicio Digital para Tiendas", "Servicio 'todo en uno' para poner en marcha y llevar el negocio del comerciante en Internet")

    mockup_path = os.path.join(curr_dir, "mockup_leadcraft.jpg")
    if os.path.exists(mockup_path):
        c.drawImage(mockup_path, 0.8 * inch, 1.3 * inch, width=5.5 * inch, height=4.6 * inch, preserveAspectRatio=True)

    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(6.6 * inch, 1.3 * inch, 5.9 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(c_navy)
    c.drawString(6.9 * inch, 5.4 * inch, "⚡ FUNCIONALIDADES CLAVE DEL SERVICIO")

    funcs = [
        ("🗺️ Prospección y Auditoría en Google Maps", "Localiza comercios y detecta carencias digitales (sin web, sin reservas)."),
        ("🤖 Web Asistida por IA para el Negocio", "Genera la web con horarios, catálogo y fotos extraídas de la ficha."),
        ("📅 Sistema Integrado de Citas Online 24/7", "Calendario interactivo con franjas horarias y confirmación inmediata."),
        ("💬 Canal de Contacto y Pedidos por WhatsApp", "Enlace directo para enviar consultas y reservas al móvil del comercio."),
        ("📱 Panel de Control Sencillo para el Dueño", "Gestión fácil de citas del día y cambios de horarios sin saber programar.")
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
    c.drawCentredString(w / 2.0, 0.65 * inch, "🚀 Modelo B2B Micro-SaaS • Servicio Integral de Digitalización y Acompañamiento a Comercios")
    c.showPage()

    # SLIDE 3
    draw_slide_base("03 / 03  •  VALOR AÑADIDO", "VALOR E INNOVACIÓN", "3. Valor Añadido del Servicio y Mejoras Futuras", "¿Por qué resulta útil vender este servicio y cuál es su proyección futura?")

    c.setFillColor(c_white)
    c.setStrokeColor(c_border)
    c.setLineWidth(1.5)
    c.roundRect(0.8 * inch, 1.3 * inch, 5.6 * inch, 4.6 * inch, 8, fill=True, stroke=True)

    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(c_cyan)
    c.drawString(1.1 * inch, 5.4 * inch, "🌟 VALOR DEL SERVICIO (¿POR QUÉ ES ÚTIL?)")

    vals = [
        ("Servicio 'Llave en Mano'", "El comerciante no compra un software suelto, sino un servicio activo que le lleva su tienda en Internet."),
        ("Demostración Visual Instantánea", "El comercial se presenta con la tienda ya maquetada sobre datos de Google Maps, multiplicando el cierre de ventas."),
        ("Cuota Asequible por Suscripción", "Sustituye los presupuestos desorbitados de agencias por un servicio mensual accesible y mantenido."),
        ("Independencia para el Comerciante", "Panel intuitivo para consultar reservas sin depender de soporte técnico externo.")
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
        ("Bot de WhatsApp con IA 24/7", "Atención automatizada para dudas frecuentes, confirmación de citas y recordatorios por chat."),
        ("Pagos Integrados con Stripe", "Cobro de señales o venta directa de productos y servicios desde la propia web."),
        ("Sincronización con Google Calendar", "Conexión bidireccional automática con la agenda personal y de empleados del comercio.")
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
