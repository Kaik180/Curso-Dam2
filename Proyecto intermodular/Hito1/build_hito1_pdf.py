import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

curr_dir = r"c:\Users\kevin\OneDrive\Documentos\GitHub\Curso-Dam2\Proyecto intermodular\Hito1"

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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#78909C"))

        header_text = "Proyecto Intermodular - 2º DAM  |  Hito 1: LeadCraft AI"
        self.drawRightString(A4[0] - 40, A4[1] - 30, header_text)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(40, A4[1] - 35, A4[0] - 40, A4[1] - 35)

        footer_left = "LeadCraft AI  •  Kevin Muñoz Córcoles"
        footer_right = f"Página {self._pageNumber} de {page_count}"
        self.line(40, 35, A4[0] - 40, 35)
        self.drawString(40, 24, footer_left)
        self.drawRightString(A4[0] - 40, 24, footer_right)
        self.restoreState()

def generate_hito1_pdf():
    pdf_path_leadcraft = os.path.join(curr_dir, "Hito1_LeadCraft_Kevin.pdf")
    pdf_path_viabilidad = os.path.join(curr_dir, "Hito1_Viabilidad_LeadCraft_Kevin.pdf")

    # Build story
    s_title = ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=26, leading=30, textColor=colors.HexColor("#0A192F"), alignment=1)
    s_sub = ParagraphStyle('CoverSub', fontName='Helvetica-Oblique', fontSize=11, leading=15, textColor=colors.HexColor("#0038FF"), alignment=1)
    s_badge = ParagraphStyle('CoverBadge', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=colors.HexColor("#00B496"), alignment=1)
    s_hito = ParagraphStyle('CoverHito', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor("#475569"), alignment=1)
    s_meta = ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#232F3E"), alignment=1)

    s_h1 = ParagraphStyle('Heading1', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor("#0A192F"), spaceBefore=4, spaceAfter=2)
    s_body = ParagraphStyle('BodyTextCustom', fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=colors.HexColor("#2C3E50"), alignment=4, spaceAfter=2.5)
    s_toc = ParagraphStyle('TOCItem', fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=colors.HexColor("#0A192F"), spaceAfter=1.5)
    s_cap = ParagraphStyle('Caption', fontName='Helvetica-Oblique', fontSize=7.5, leading=10, textColor=colors.HexColor("#64748B"), alignment=1, spaceAfter=2)

    story = []

    # ========================== PÁGINA 1: PORTADA ==========================
    story.append(Spacer(1, 15))
    story.append(Paragraph("PROYECTO INTERMODULAR • 2º DAM", s_badge))
    story.append(Spacer(1, 4))
    story.append(Paragraph("LeadCraft AI", s_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Servicio Integral de Gestión y Presencia Digital para el Pequeño Comercio Local impulsado por Inteligencia Artificial", s_sub))
    story.append(Spacer(1, 8))
    story.append(Paragraph("—" * 28, ParagraphStyle('Div', fontName='Helvetica', fontSize=11, textColor=colors.HexColor("#CBD5E1"), alignment=1)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>HITO 1: ANÁLISIS Y CONTEXTO</b><br/><font color='#64748B'>Documento de Viabilidad Inicial, Definición de Alcance y Modelo de Servicio</font>", s_hito))
    story.append(Spacer(1, 20))

    meta_html = (
        "<b>Alumno:</b> Kevin Muñoz Córcoles<br/>"
        "<b>Curso:</b> 2º Desarrollo de Aplicaciones Multiplataforma (DAM)<br/>"
        "<b>Módulo:</b> Proyecto Intermodular | Convocatoria 2026/2027<br/>"
        "<b>Fecha de entrega:</b> 23 de Octubre de 2026"
    )
    story.append(Paragraph(meta_html, s_meta))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Índice del Documento de Viabilidad Inicial", s_h1))
    tocs = [
        "01. Título y Descripción del Proyecto: El Servicio LeadCraft AI (Pág. 2)",
        "02. Problema o Necesidad: La Dificultad de Llevar un Negocio en Internet (Pág. 2)",
        "03. Usuarios y Público Objetivo (Pág. 2)",
        "04. Benchmarking Competitivo y Soluciones Similares (Pág. 2)",
        "05. Objetivos Iniciales del Proyecto (Modelo SMART) (Pág. 3)",
        "06. Alcance Mínimo Viable (MVP) y Ampliaciones Futuras (Pág. 3)",
        "07. Riesgos Iniciales y Medidas Preventivas (Pág. 3)",
        "08. Vinculación con los Objetivos de Desarrollo Sostenible (ODS) (Pág. 4)",
        "09. Organización Inicial del Trabajo y Metodología (Pág. 4)",
        "10. Caso de Uso Principal: Prospección, Venta e Implantación del Servicio (Pág. 4)",
        "11. Diagrama de Arquitectura del Sistema (Pág. 5)",
        "12. Mockups de Pantallas Clave de la Aplicación (Pág. 5)"
    ]
    for tl in tocs:
        story.append(Paragraph(f"• {tl}", s_toc))

    story.append(PageBreak())

    # ========================== PÁGINA 2: ANÁLISIS & BENCHMARKING ==========================
    story.append(Paragraph("01. Título y Descripción del Proyecto: El Servicio LeadCraft AI", s_h1))
    story.append(Paragraph(
        "LeadCraft AI es una solución de software como servicio (SaaS) diseñada para comercializar un servicio integral de digitalización y gestión online para pequeños comercios y profesionales locales (barberías, talleres, clínicas de fisioterapia, restaurantes o tiendas de barrio). El objetivo principal del proyecto no es únicamente crear páginas web estáticas, sino vender un servicio activo que ayuda al comerciante a llevar su negocio en Internet en el día a día: incluye la creación y alojamiento de su página web profesional mediante IA, un sistema integrado para gestionar sus citas y reservas online, catálogo de servicios actualizado, contacto directo por WhatsApp con sus clientes y un panel de control intuitivo desde el móvil o tablet para consultar sus reservas diarias y horarios sin depender de informáticos externos ni costes abusivos.",
        s_body
    ))

    story.append(Paragraph("02. Problema o Necesidad: La Dificultad de Llevar un Negocio en Internet", s_h1))
    story.append(Paragraph(
        "Hoy en día, la mayoría de los pequeños comerciantes y autónomos se encuentran desbordados para gestionar su presencia en Internet. Saben que necesitan estar digitalizados, pero no tienen tiempo, conocimientos técnicos ni presupuesto para contratar agencias de marketing o desarrolladores externos (que suelen cobrar entre 800€ y 2.500€ iniciales más cuotas de mantenimiento mensual desproporcionadas). Como consecuencia, muchos negocios solo tienen una ficha básica en Google Maps pero carecen de web propia, no ofrecen citas online y dependen de atender llamadas telefónicas mientras trabajan con un cliente en el local, perdiendo ventas frente a grandes franquicias. LeadCraft AI resuelve esta situación ofreciendo un servicio 'todo en uno' asequible y empaquetado que se encarga de poner en marcha y llevar su tienda o negocio en Internet de forma transparente.",
        s_body
    ))

    story.append(Paragraph("03. Usuarios y Público Objetivo", s_h1))
    story.append(Paragraph(
        "<b>• Cliente Principal (El Comerciante / Dueño del Negocio):</b> Propietarios de pymes locales que contratan el servicio de LeadCraft AI para despreocuparse de la complejidad técnica y tener su negocio operativo en Internet (web con citas, carta/catálogo y canal directo de WhatsApp).",
        s_body
    ))
    story.append(Paragraph(
        "<b>• Clientes Finales del Negocio:</b> Vecinos y usuarios de la zona que acceden a la web desde su móvil para reservar cita en la peluquería, encargar un pedido o consultar precios a cualquier hora.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• Operador Comercial / Gestor de Cuentas:</b> Diseñadores freelance, consultores o alumnos de DAM que utilizan la herramienta sobre Google Maps para identificar comercios con carencias digitales en su zona y ofrecerles el servicio con una demo interactiva ya configurada.",
        s_body
    ))

    story.append(Paragraph("04. Benchmarking Competitivo y Soluciones Similares", s_h1))
    story.append(Paragraph("Se han analizado tres alternativas actuales en el mercado para comparar cómo abordan la digitalización de pymes:", s_body))

    t_bench_data = [
        [Paragraph("<b>Plataforma</b>", ParagraphStyle('TBH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Modelo / Enfoque</b>", ParagraphStyle('TBH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Puntos Fuertes</b>", ParagraphStyle('TBH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Carencias frente al Servicio LeadCraft</b>", ParagraphStyle('TBH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white))],
        [Paragraph("<b>Wix Studio / Duda</b>", ParagraphStyle('TBD', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Generadores web SaaS con IA para crear sitios web corporativos.", ParagraphStyle('TBD', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Diseños modernos y plantillas responsive bien estructuradas.", ParagraphStyle('TBD', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("No incluye prospección en Maps ni detecta carencias; requiere que el comerciante dedique tiempo a construir y maquetar la web por su cuenta.", ParagraphStyle('TBD', fontName='Helvetica', fontSize=7.5, leading=9.5))],
        [Paragraph("<b>D7 Lead Finder</b>", ParagraphStyle('TBD', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Buscadores de leads que extraen datos de contacto desde Google Maps.", ParagraphStyle('TBD', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Rápida extracción masiva de correos y teléfonos de negocios.", ParagraphStyle('TBD', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Se limita a generar listados de texto en Excel; no audita carencias reales, no genera la solución web ni integra reservas.", ParagraphStyle('TBD', fontName='Helvetica', fontSize=7.5, leading=9.5))],
        [Paragraph("<b>Calendly / Treatwell</b>", ParagraphStyle('TBD', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Software especializado en reservas y gestión de citas online.", ParagraphStyle('TBD', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Calendarios eficaces con recordatorios automáticos por SMS/correo.", ParagraphStyle('TBD', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Son herramientas aisladas que no proporcionan la web del negocio ni canal directo por WhatsApp; comisiones abusivas en el caso de Treatwell.", ParagraphStyle('TBD', fontName='Helvetica', fontSize=7.5, leading=9.5))]
    ]
    t_bench_pdf = Table(t_bench_data, colWidths=[100, 115, 135, 165])
    t_bench_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A192F")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F1F5F9"), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_bench_pdf)
    story.append(PageBreak())

    # ========================== PÁGINA 3: SMART, MVP & RIESGOS ==========================
    story.append(Paragraph("05. Objetivos Iniciales del Proyecto (Modelo SMART)", s_h1))
    story.append(Paragraph("<b>• Específico (S):</b> Desarrollar una solución integral que permita activar un servicio digital completo para pequeños negocios locales (web profesional generada con IA mediante Google Gemini + widget de reservas online + panel de control simplificado para el comerciante).", s_body))
    story.append(Paragraph("<b>• Medible (M):</b> Conseguir que el tiempo de configuración y despliegue del servicio sea inferior a 60 segundos por comercio, y estructurar una oferta de servicio asequible para pymes con un coste inferior a 25€/mes frente a los costes tradicionales de agencia.", s_body))
    story.append(Paragraph("<b>• Alcanzable (A):</b> Desarrollar el sistema utilizando tecnologías multiplataforma dominadas en el ciclo (FastAPI en backend, Flutter/Web en frontend y bases de datos relacionales SQLite/PostgreSQL) con plantillas modulares prediseñadas por sector.", s_body))
    story.append(Paragraph("<b>• Relevante (R):</b> Cubre una necesidad real del mercado: transformar el tejido comercial de barrio dotándolo de autonomía digital y creando una oportunidad de autoempleo para titulados de DAM.", s_body))
    story.append(Paragraph("<b>• Temporal (T):</b> Cumplir la planificación académica en tres entregas: Hito 1 en octubre, Hito 2 (MVP funcional) en enero y Hito 3 (plataforma completa con panel de comerciante) en marzo/abril de 2027.", s_body))

    story.append(Paragraph("06. Alcance Mínimo Viable (MVP) y Ampliaciones Futuras", s_h1))
    story.append(Paragraph("<b>• Funcionalidades del MVP (Versión 1.0 del Servicio):</b>", s_body))
    story.append(Paragraph("1) Módulo de localización y auditoría express de comercios sobre Google Maps (detección de carencias web y reservas).<br/>"
                           "2) Motor de generación con IA de la web del negocio (redacción comercial de servicios, horarios y fotos de Maps).<br/>"
                           "3) Widget interactivo de citas y reservas online incrustado en la web con selección de franjas horarias.<br/>"
                           "4) Panel de gestión básico para el comerciante donde puede consultar las citas recibidas y cambiar horarios desde su móvil.<br/>"
                           "5) Integración de botón de contacto directo por WhatsApp Business.<br/>"
                           "6) Exportación de la web en paquete HTML5/Tailwind y generación de informe comercial de auditoría en PDF.", s_body))

    story.append(Paragraph("<b>• Ampliaciones Futuras (Versión 2.0):</b>", s_body))
    story.append(Paragraph("1) Bot inteligente de WhatsApp con IA que responde preguntas de los clientes y agenda citas de forma automática 24/7.<br/>"
                           "2) Pasarela de cobro integrada con Stripe para permitir a los clientes pagar señales o productos online.<br/>"
                           "3) Alojamiento cloud automatizado en Vercel/Netlify con asignación de dominios propios (.es / .com) con 1 clic.", s_body))

    story.append(Paragraph("07. Riesgos Iniciales y Medidas Preventivas", s_h1))
    story.append(Paragraph("<b>• Riesgo 1: Coste de las llamadas a Google Places API y modelos de IA.</b> Medida: Implementar almacenamiento en caché local (base de datos) para no repetir consultas sobre el mismo comercio y comprimir los prompts enviados a Gemini.", s_body))
    story.append(Paragraph("<b>• Riesgo 2: Reticencia del comerciante a la tecnología o falta de uso.</b> Medida: Diseñar el panel de gestión con una interfaz ultrasimplificada tipo 'Modo Fácil', similar a WhatsApp, sin menús complicados ni términos técnicos.", s_body))
    story.append(Paragraph("<b>• Riesgo 3: Gestión del tiempo durante el curso escolar.</b> Medida: Priorización estricta de tareas según el método MoSCoW, asegurando que el flujo de venta y el panel de citas funcionen antes de añadir florituras estéticas.", s_body))
    story.append(PageBreak())

    # ========================== PÁGINA 4: ODS, METODOLOGÍA & CASO DE USO ==========================
    story.append(Paragraph("08. Vinculación con los Objetivos de Desarrollo Sostenible (ODS)", s_h1))
    story.append(Paragraph("<b>• ODS 8: Trabajo Decente y Crecimiento Económico (Meta 8.3):</b> LeadCraft AI impulsa la competitividad y modernización de las microempresas y trabajadores autónomos de barrio, dándoles herramientas para incrementar sus ventas y competir con grandes cadenas multinacionales.", s_body))
    story.append(Paragraph("<b>• ODS 9: Industria, Innovación e Infraestructura (Meta 9.3):</b> Democratiza el acceso a la inteligencia artificial generativa y a infraestructuras web avanzadas para comercios tradicionales con presupuestos modestos.", s_body))
    story.append(Paragraph("<b>• ODS 11: Ciudades y Comunidades Sostenibles (Meta 11.a):</b> Fortalece el comercio de proximidad, garantizando que los servicios esenciales y tiendas de barrio sigan vivos y conectados con los vecinos en la era digital.", s_body))

    story.append(Paragraph("09. Organización Inicial del Trabajo y Metodología", s_h1))
    story.append(Paragraph("El proyecto se desarrollará siguiendo el marco ágil Scrum apoyado en un tablero Kanban de Trello para la gestión del Product Backlog. El desarrollo se organiza en tres Sprints principales: <b>Sprint 1</b> (Explorador sobre Maps, API de Places y motor de auditoría); <b>Sprint 2</b> (Generador web con IA de Gemini, catálogo de plantillas por sector y widget de citas online); <b>Sprint 3</b> (Panel de control del comerciante, exportación cloud/PDF, integración de WhatsApp y pruebas de usuario).", s_body))

    story.append(Paragraph("10. Caso de Uso Principal: Prospección, Venta e Implantación del Servicio", s_h1))
    story.append(Paragraph("A continuación se detalla el flujo de funcionamiento y comercialización del servicio:", s_body))
    story.append(Paragraph("<b>1. Detección en Maps:</b> El gestor abre la aplicación, selecciona su zona geográfica y filtra por negocios de servicios (ej. barberías o clínicas dentales).", s_body))
    story.append(Paragraph("<b>2. Diagnóstico de Carencias:</b> El sistema analiza el local 'Barbería Clásica' y detecta que no tiene web ni reservas online (Score Digital del 45%).", s_body))
    story.append(Paragraph("<b>3. Generación Inmediata de la Solución:</b> La IA analiza los datos de Maps (horarios, opiniones y fotos) y genera en 25 segundos una web completa con precios de cortes y un widget de reservas de citas.", s_body))
    story.append(Paragraph("<b>4. Presentación y Demostración:</b> El comercial contacta con el dueño mostrando la web ya funcionando en el móvil: 'Hemos preparado esta demo para tu negocio; incluye tus citas y tu WhatsApp por una cuota reducida al mes'.", s_body))
    story.append(Paragraph("<b>5. Activación del Servicio:</b> El comerciante contrata el servicio; recibe acceso a su panel de control de LeadCraft AI en su móvil para gestionar sus citas entrantes y su web queda publicada en Internet.", s_body))
    story.append(PageBreak())

    # ========================== PÁGINA 5: ARQUITECTURA & MOCKUPS ==========================
    story.append(Paragraph("11. Diagrama de Arquitectura del Sistema", s_h1))
    story.append(Paragraph("La arquitectura técnica de LeadCraft AI se estructura en cuatro capas modulares que separan el cliente, la lógica de negocio, las APIs externas y la persistencia de datos:", s_body))

    diag_p = os.path.join(curr_dir, "diagrama_arquitectura_leadcraft.png")
    if os.path.exists(diag_p):
        story.append(Image(diag_p, width=5.5*inch, height=3.0*inch))
        story.append(Spacer(1, 1))
        story.append(Paragraph("Figura 1: Arquitectura de Componentes de LeadCraft AI (Frontend, Backend Gateway, APIs Externas y Capa de Datos).", s_cap))

    story.append(Spacer(1, 2))
    story.append(Paragraph("12. Mockups de Pantallas Clave de la Aplicación", s_h1))
    
    m1_p = os.path.join(curr_dir, "mockup_leadcraft_desktop.png")
    m2_p = os.path.join(curr_dir, "mockup_leadcraft_mobile.png")

    if os.path.exists(m1_p) and os.path.exists(m2_p):
        # 3.25 inches wide for both
        t_img_data = [
            [Image(m1_p, width=3.35*inch, height=2.44*inch), Image(m2_p, width=3.35*inch, height=1.87*inch)],
            [Paragraph("<b>Pantalla 1:</b> Mapa y Auditoría Digital Express (Escritorio).", s_cap), 
             Paragraph("<b>Pantalla 2:</b> Versión móvil en 3 fases (Explorar, Generar y Exportar).", s_cap)]
        ]
        t_mock_pdf = Table(t_img_data, colWidths=[255, 255])
        t_mock_pdf.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('LEFTPADDING', (0,0), (-1,-1), 1),
            ('RIGHTPADDING', (0,0), (-1,-1), 1),
        ]))
        story.append(t_mock_pdf)

    # Build both files
    doc_leadcraft = SimpleDocTemplate(
        pdf_path_leadcraft,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=38,
        bottomMargin=38
    )
    doc_leadcraft.build(list(story), canvasmaker=NumberedCanvas)
    print("Hito 1 PDF Document generated successfully at:", pdf_path_leadcraft)

    doc_viabilidad = SimpleDocTemplate(
        pdf_path_viabilidad,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=38,
        bottomMargin=38
    )
    doc_viabilidad.build(list(story), canvasmaker=NumberedCanvas)
    print("Hito 1 PDF Document generated successfully at:", pdf_path_viabilidad)

if __name__ == "__main__":
    generate_hito1_pdf()
