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
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#78909C"))

        header_text = "Proyecto Intermodular - 2º DAM  |  Hito 1: Viabilidad Inicial (LeadCraft AI)"
        self.drawRightString(A4[0] - 45, A4[1] - 32, header_text)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(45, A4[1] - 38, A4[0] - 45, A4[1] - 38)

        footer_left = "LeadCraft AI  •  Kevin Muñoz Córcoles"
        footer_right = f"Página {self._pageNumber} de {page_count}"
        self.line(45, 36, A4[0] - 45, 36)
        self.drawString(45, 25, footer_left)
        self.drawRightString(A4[0] - 45, 25, footer_right)
        self.restoreState()

def generate_hito1_pdf():
    pdf_path = os.path.join(curr_dir, "Hito1_Viabilidad_LeadCraft_Kevin.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    s_title = ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=26, leading=30, textColor=colors.HexColor("#0A192F"), alignment=1)
    s_sub = ParagraphStyle('CoverSub', fontName='Helvetica-Oblique', fontSize=11.5, leading=15, textColor=colors.HexColor("#0038FF"), alignment=1)
    s_badge = ParagraphStyle('CoverBadge', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor("#00B496"), alignment=1)
    s_hito = ParagraphStyle('CoverHito', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor("#475569"), alignment=1)
    s_meta = ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=10.5, leading=15, textColor=colors.HexColor("#232F3E"), alignment=1)

    s_h1 = ParagraphStyle('Heading1', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=colors.HexColor("#0A192F"), spaceBefore=6, spaceAfter=2)
    s_body = ParagraphStyle('BodyTextCustom', fontName='Helvetica', fontSize=9, leading=12.5, textColor=colors.HexColor("#2C3E50"), alignment=4, spaceAfter=3.5)
    s_toc = ParagraphStyle('TOCItem', fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=colors.HexColor("#0A192F"), spaceAfter=1.5)
    s_cap = ParagraphStyle('Caption', fontName='Helvetica-Oblique', fontSize=7.5, leading=10, textColor=colors.HexColor("#64748B"), alignment=1, spaceAfter=2)

    story = []

    # ========================== PÁGINA 1: PORTADA ==========================
    story.append(Spacer(1, 20))
    story.append(Paragraph("PROYECTO INTERMODULAR • 2º DAM", s_badge))
    story.append(Spacer(1, 4))
    story.append(Paragraph("LeadCraft AI", s_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Plataforma Inteligente de Prospección Geográfica, Auditoría Digital y Generación Asistida de Soluciones Web para Pequeños Negocios Locales", s_sub))
    story.append(Spacer(1, 10))
    story.append(Paragraph("—" * 28, ParagraphStyle('Div', fontName='Helvetica', fontSize=11, textColor=colors.HexColor("#CBD5E1"), alignment=1)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>HITO 1: ANÁLISIS Y CONTEXTO</b><br/><font color='#64748B'>Documento de Viabilidad Inicial, Definición de Alcance y Diseño Preliminar</font>", s_hito))
    story.append(Spacer(1, 25))

    meta_html = (
        "<b>Alumno:</b> Kevin Muñoz Córcoles<br/>"
        "<b>Curso:</b> 2º Desarrollo de Aplicaciones Multiplataforma (DAM)<br/>"
        "<b>Módulo:</b> Proyecto Intermodular | Convocatoria 2026/2027<br/>"
        "<b>Fecha de entrega:</b> 23 de Octubre de 2026"
    )
    story.append(Paragraph(meta_html, s_meta))
    story.append(Spacer(1, 30))

    story.append(Paragraph("Índice del Documento de Viabilidad Inicial", s_h1))
    tocs = [
        "01. Título y Descripción del Proyecto (Pág. 2)",
        "02. Problema o Necesidad Detectada (Pág. 2)",
        "03. Usuarios y Público Objetivo (Pág. 2)",
        "04. Benchmarking Competitivo y Soluciones Similares (Pág. 2)",
        "05. Objetivos Iniciales del Proyecto (Modelo SMART) (Pág. 3)",
        "06. Alcance Mínimo Viable (MVP) y Ampliaciones Futuras (Pág. 3)",
        "07. Riesgos Iniciales y Medidas Preventivas (Pág. 3)",
        "08. Vinculación con los Objetivos de Desarrollo Sostenible (ODS) (Pág. 4)",
        "09. Organización Inicial del Trabajo y Metodología (Pág. 4)",
        "10. Caso de Uso Principal Paso a Paso (Pág. 4)",
        "11. Diagrama de Arquitectura del Sistema (Pág. 5)",
        "12. Mockups de Pantallas Clave de la Aplicación (Pág. 5)"
    ]
    for tl in tocs:
        story.append(Paragraph(f"• {tl}", s_toc))

    story.append(PageBreak())

    # ========================== PÁGINA 2: ANÁLISIS & BENCHMARKING ==========================
    story.append(Paragraph("01. Título y Descripción del Proyecto", s_h1))
    story.append(Paragraph(
        "LeadCraft AI es una solución de software B2B SaaS concebida para acelerar la digitalización del comercio local de proximidad. La plataforma integra una interfaz cartográfica interactiva sobre Google Maps que permite a profesionales digitales, agencias de marketing y comerciales explorar barrios o municipios, auditar de forma automática la presencia web de los negocios locales y generar al instante, mediante modelos de IA Generativa (LLM), una landing page profesional con sistema de reservas/citas online y contacto directo por WhatsApp adaptada a la identidad y datos públicos del comercio.",
        s_body
    ))

    story.append(Paragraph("02. Problema o Necesidad Detectada", s_h1))
    story.append(Paragraph(
        "A pesar del avance tecnológico, miles de microempresas de proximidad (barberías, talleres mecánicos, restaurantes, centros de estética y fisioterapia) presentan una grave brecha digital. Si bien figuran registrados en Google Maps, un alto porcentaje no dispone de página web propia, carece de certificados de seguridad HTTPS y no ofrece mecanismos para reservar citas online. Esto provoca pérdidas directas de clientes frente a grandes franquicias y una sobrecarga telefónica para los dueños mientras trabajan. Paralelamente, los profesionales y agencias web invierten incontables horas en prospección manual en frío, recopilando datos uno a uno y presentando presupuestos abstractos que los comerciantes suelen rechazar por desconfianza o desconocimiento del resultado final.",
        s_body
    ))

    story.append(Paragraph("03. Usuarios y Público Objetivo", s_h1))
    story.append(Paragraph(
        "<b>• Operador Primario (Comercial / Agencia / Freelancer):</b> Desarrolladores noveles de DAM, diseñadores web freelance y pequeñas agencias de marketing que necesitan una herramienta ágil para detectar oportunidades comerciales en su área geográfica, automatizar la generación de propuestas funcionales y elevar drásticamente su tasa de conversión de clientes.",
        s_body
    ))
    story.append(Paragraph(
        "<b>• Beneficiario Final (Dueño del Negocio y Clientes Finales):</b> Propietarios de pymes locales que obtienen una presencia web moderna con reservas online por una fracción del coste tradicional, y sus clientes, que pueden consultar servicios y agendar citas desde su móvil las 24 horas del día.",
        s_body
    ))

    story.append(Paragraph("04. Benchmarking Competitivo y Soluciones Similares", s_h1))
    story.append(Paragraph(
        "Se han analizado tres plataformas de referencia en los sectores de generación web, prospección de leads y gestión de citas:",
        s_body
    ))

    # Tabla benchmarking
    b_data = [
        [Paragraph("<b>Herramienta</b>", ParagraphStyle('BTH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Enfoque / Función</b>", ParagraphStyle('BTH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Puntos Fuertes</b>", ParagraphStyle('BTH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
         Paragraph("<b>Carencias / Oportunidad LeadCraft</b>", ParagraphStyle('BTH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white))],
        [Paragraph("<b>Wix Studio / Duda (ADI)</b>", ParagraphStyle('BTD', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5)),
         Paragraph("Generadores web con IA para sitios corporativos.", ParagraphStyle('BTD2', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Diseños modernos y plantillas responsive bien estructuradas.", ParagraphStyle('BTD2', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("No incluye motor de prospección geográfica ni audita negocios en Google Maps; requiere introducir datos manualmente.", ParagraphStyle('BTD2', fontName='Helvetica', fontSize=7.5, leading=9.5))],
        [Paragraph("<b>D7 Lead Finder / LeadEnforce</b>", ParagraphStyle('BTD', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5)),
         Paragraph("Buscadores de leads que extraen datos desde Google Maps.", ParagraphStyle('BTD2', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Rápida extracción masiva de correos y teléfonos de comercios.", ParagraphStyle('BTD2', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Se limita a generar listados de texto (CSV/Excel); no detecta carencias web ni construye ninguna solución interactiva para enseñar.", ParagraphStyle('BTD2', fontName='Helvetica', fontSize=7.5, leading=9.5))],
        [Paragraph("<b>Calendly / Treatwell</b>", ParagraphStyle('BTD', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5)),
         Paragraph("Software especializado en reservas y citas online.", ParagraphStyle('BTD2', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Calendarios eficaces con recordatorios automáticos por SMS.", ParagraphStyle('BTD2', fontName='Helvetica', fontSize=7.5, leading=9.5)),
         Paragraph("Son herramientas aisladas que no proporcionan la web del negocio y exigen cuotas mensuales recurrentes elevadas para pequeñas pymes.", ParagraphStyle('BTD2', fontName='Helvetica', fontSize=7.5, leading=9.5))]
    ]
    t_b = Table(b_data, colWidths=[110, 115, 135, 145])
    t_b.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0A192F")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F1F5F9"), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t_b)
    story.append(PageBreak())

    # ========================== PÁGINA 3: SMART, MVP & RIESGOS ==========================
    story.append(Paragraph("05. Objetivos Iniciales del Proyecto (Modelo SMART)", s_h1))
    story.append(Paragraph("<b>• Específico (S):</b> Desarrollar una aplicación funcional multiplataforma que integre Google Places API para localizar comercios locales, ejecute un algoritmo de auditoría digital express y genere una landing page adaptada con widget de citas mediante llamadas a la API de Google Gemini.", s_body))
    story.append(Paragraph("<b>• Medible (M):</b> Lograr que el tiempo de análisis y generación completa de la propuesta web sea inferior a 30 segundos por negocio, alcanzando un score de satisfacción técnica del 100% en la validación de código HTML5/Tailwind.", s_body))
    story.append(Paragraph("<b>• Alcanzable (A):</b> Utilizar una arquitectura modular en Python (FastAPI) y Flutter/React con plantillas prediseñadas por sector, acotando el alcance para evitar desarrollos inabarcables en el calendario académico.", s_body))
    story.append(Paragraph("<b>• Relevante (R):</b> Dotar a los alumnos de DAM de un proyecto con aplicación comercial directa en el mercado de servicios informáticos y alineado con los fondos de digitalización de pymes.", s_body))
    story.append(Paragraph("<b>• Temporal (T):</b> Completar el ciclo de desarrollo en tres hitos evaluables antes del término del curso escolar (Hito 1: Octubre; Hito 2: Enero; Hito 3 / Defensa final: Marzo/Abril).", s_body))

    story.append(Paragraph("06. Alcance Mínimo Viable (MVP) y Ampliaciones Futuras", s_h1))
    story.append(Paragraph("<b>• Funcionalidades del MVP (Versión 1.0 Obligatoria):</b>", s_body))
    story.append(Paragraph("1) Navegación sobre mapa con filtrado por categoría (Hostelería, Salud/Estética, Servicios mecánicos).<br/>"
                           "2) Panel de Auditoría Express con cálculo de 'Digital Health Score' (Web, SSL, Reservas, Reseñas).<br/>"
                           "3) Generación asistida por IA del copy comercial y ensamblado de Landing Page responsive.<br/>"
                           "4) Widget incrustado de selección de fecha y hora para reserva de citas.<br/>"
                           "5) Previsualizador interactivo con vista móvil y escritorio.<br/>"
                           "6) Exportador de código web en archivo ZIP y generación de informe de auditoría en PDF.", s_body))

    story.append(Paragraph("<b>• Ampliaciones Futuras (Post-MVP / Versión 2.0):</b>", s_body))
    story.append(Paragraph("1) Agente conversacional de WhatsApp conectado a IA para confirmación automática de citas 24/7.<br/>"
                           "2) Pasarela de pago con Stripe para cobro de reservas o señales bancarias.<br/>"
                           "3) Despliegue cloud automatizado en Vercel o Netlify con asignación de subdominios o dominios personalizados.", s_body))

    story.append(Paragraph("07. Riesgos Iniciales y Medidas Preventivas", s_h1))
    story.append(Paragraph("<b>• Riesgo 1: Coste y límites de cuota de Google Places API y LLM.</b> Medida: Implementar una capa de almacenamiento en caché local (SQLite/PostgreSQL) para reutilizar datos de comercios ya consultados y diseñar prompts compactos que minimicen el consumo de tokens.", s_body))
    story.append(Paragraph("<b>• Riesgo 2: Datos incompletos en Google Maps (falta de teléfono o fotos).</b> Medida: El motor incorporará plantillas inteligentes con contenido por defecto ('fallbacks') para rellenar de forma coherente cualquier campo omitido.", s_body))
    story.append(Paragraph("<b>• Riesgo 3: Gestión del tiempo y sobrecarga tecnológica.</b> Medida: Adopción de metodología ágil Scrum con entregas bisemanales y priorización estricta bajo técnica MoSCoW (Must, Should, Could, Won't).", s_body))
    story.append(PageBreak())

    # ========================== PÁGINA 4: ODS, METODOLOGÍA & CASO DE USO ==========================
    story.append(Paragraph("08. Vinculación con los Objetivos de Desarrollo Sostenible (ODS)", s_h1))
    story.append(Paragraph("<b>• ODS 8: Trabajo Decente y Crecimiento Económico (Meta 8.3):</b> LeadCraft AI impulsa de forma directa la digitalización y productividad de las microempresas y trabajadores autónomos, permitiéndoles competir en igualdad de condiciones con grandes cadenas comerciales.", s_body))
    story.append(Paragraph("<b>• ODS 9: Industria, Innovación e Infraestructura (Meta 9.3):</b> Facilita el acceso democrático y asequible a tecnologías de inteligencia artificial generativa a comercios que no pueden permitirse grandes presupuestos de software.", s_body))
    story.append(Paragraph("<b>• ODS 11: Ciudades y Comunidades Sostenibles (Meta 11.a):</b> Fortalece el tejido comercial de barrio y la economía de proximidad, garantizando la supervivencia de negocios tradicionales en entornos urbanos.", s_body))

    story.append(Paragraph("09. Organización Inicial del Trabajo y Metodología", s_h1))
    story.append(Paragraph("El proyecto se desarrollará siguiendo el marco de trabajo ágil Scrum apoyado en un tablero Kanban de Trello para la monitorización continua del Product Backlog. El plan de trabajo se estructura en tres Sprints principales: <b>Sprint 1</b> (Exploración geográfica, conexión con Google Places y motor de auditoría express); <b>Sprint 2</b> (Integración del motor de IA con Gemini, catálogo de plantillas y widget de reservas); <b>Sprint 3</b> (Previsualizador en vivo, exportador ZIP, generación del dossier comercial PDF y pruebas de rendimiento).", s_body))

    story.append(Paragraph("10. Caso de Uso Principal Paso a Paso", s_h1))
    story.append(Paragraph("A continuación se describe el flujo de interacción central de LeadCraft AI de inicio a fin:", s_body))
    story.append(Paragraph("<b>1. Selección Geográfica:</b> El operador abre la aplicación, visualiza el mapa de su ciudad y selecciona la categoría 'Peluquerías y Barberías' en el distrito Centro.", s_body))
    story.append(Paragraph("<b>2. Detección y Auditoría:</b> El sistema despliega pines sobre los locales encontrados. El operador pulsa sobre 'Barbería Clásica'. El motor de auditoría comprueba que no tiene web activa ni enlace de reservas y asigna un Digital Health Score del 45%.", s_body))
    story.append(Paragraph("<b>3. Generación Inteligente:</b> El operador hace clic en 'Generar Solución con IA'. La API extrae el nombre, teléfono, horario y reseñas de Maps, y ensambla en 20 segundos una landing page moderna con los servicios y el widget de citas online.", s_body))
    story.append(Paragraph("<b>4. Previsualización y Ajuste:</b> En la pantalla partida, el operador visualiza cómo queda la web en móvil y escritorio, ajustando si lo desea el precio de los cortes o el color corporativo.", s_body))
    story.append(Paragraph("<b>5. Exportación y Contacto:</b> Con un clic se descarga el informe de auditoría en PDF y la aplicación genera un mensaje formateado con enlace demo listo para enviar al dueño del local vía WhatsApp Business.", s_body))
    story.append(PageBreak())

    # ========================== PÁGINA 5: ARQUITECTURA & MOCKUPS ==========================
    story.append(Paragraph("11. Diagrama de Arquitectura del Sistema", s_h1))
    story.append(Paragraph("La arquitectura técnica de LeadCraft AI se estructura en cuatro capas desacopladas para garantizar escalabilidad, mantenibilidad y rapidez:", s_body))

    diag_p = os.path.join(curr_dir, "diagrama_arquitectura_leadcraft.png")
    if os.path.exists(diag_p):
        story.append(Image(diag_p, width=6.5*inch, height=3.6*inch))
        story.append(Paragraph("Figura 1: Arquitectura de Componentes de LeadCraft AI (Frontend, Backend Gateway, APIs Externas y Capa de Datos).", s_cap))

    story.append(Spacer(1, 3))
    story.append(Paragraph("12. Mockups de Pantallas Clave de la Aplicación", s_h1))
    
    m1_p = os.path.join(curr_dir, "mockup_leadcraft_audit.jpg")
    m2_p = os.path.join(curr_dir, "mockup_leadcraft_generator.jpg")

    if os.path.exists(m1_p) and os.path.exists(m2_p):
        t_img_data = [
            [Image(m1_p, width=3.2*inch, height=1.8*inch), Image(m2_p, width=3.2*inch, height=1.8*inch)],
            [Paragraph("Pantalla 1: Mapa y Auditoría Express.", s_cap), Paragraph("Pantalla 2: Generador Web con Citas.", s_cap)]
        ]
        t_mock_pdf = Table(t_img_data, colWidths=[250, 250])
        t_mock_pdf.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        story.append(t_mock_pdf)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Hito 1 PDF Document generated successfully at:", pdf_path)

if __name__ == "__main__":
    generate_hito1_pdf()
