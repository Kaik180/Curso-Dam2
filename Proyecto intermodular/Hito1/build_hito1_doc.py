import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

curr_dir = r"c:\Users\kevin\OneDrive\Documentos\GitHub\Curso-Dam2\Proyecto intermodular\Hito1"

def build_word_hito1():
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.different_first_page_header_footer = True

        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("Proyecto Intermodular - 2º DAM  |  Hito 1: Viabilidad Inicial (LeadCraft AI)")
        r_hdr.font.name = "Calibri"
        r_hdr.font.size = Pt(8.5)
        r_hdr.font.color.rgb = RGBColor(120, 144, 156)

        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ftr_l = p_ftr.add_run("LeadCraft AI  •  Kevin Muñoz Córcoles\t\tPágina ")
        r_ftr_l.font.name = "Calibri"
        r_ftr_l.font.size = Pt(9)
        r_ftr_l.font.color.rgb = RGBColor(120, 144, 156)
        
        fld_run = p_ftr.add_run()
        fld_run.font.name = "Calibri"
        fld_run.font.size = Pt(9)
        fld_run.font.color.rgb = RGBColor(120, 144, 156)
        fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
        instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
        fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
        fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
        fld_run._r.append(fldChar1)
        fld_run._r.append(instrText)
        fld_run._r.append(fldChar2)
        fld_run._r.append(fldChar3)

    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Calibri'
    font_normal.size = Pt(11)
    font_normal.color.rgb = RGBColor(35, 47, 62)
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(3)

    bookmark_id = 0
    def add_bookmark(paragraph, name):
        nonlocal bookmark_id
        bookmark_id += 1
        b_start = parse_xml(f'<w:bookmarkStart {nsdecls("w")} w:id="{bookmark_id}" w:name="{name}"/>')
        b_end = parse_xml(f'<w:bookmarkEnd {nsdecls("w")} w:id="{bookmark_id}"/>')
        paragraph._p.insert(0, b_start)
        paragraph._p.append(b_end)

    def add_external_link(paragraph, url, text):
        part = paragraph.part
        r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
        hyperlink = parse_xml(f'<w:hyperlink {nsdecls("w")} {nsdecls("r")} r:id="{r_id}" w:history="1"/>')
        new_run = parse_xml(
            f'<w:r {nsdecls("w")}><w:rPr>'
            f'<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
            f'<w:color w:val="0B7285"/>'
            f'<w:u w:val="single"/>'
            f'</w:rPr><w:t>{text}</w:t></w:r>'
        )
        hyperlink.append(new_run)
        paragraph._p.append(hyperlink)

    def add_h1(text, anchor=None, space_before=6, space_after=2):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(13.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(10, 25, 47) # Deep Navy
        if anchor:
            add_bookmark(p, anchor)
        return p

    def add_h2(text, space_before=4, space_after=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 150, 136) # Teal
        return p

    def add_p(text, bold_prefix=None, space_after=3):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(space_after)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = 'Calibri'
            rb.font.size = Pt(11)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(10, 37, 64)
        rt = p.add_run(text)
        rt.font.name = 'Calibri'
        rt.font.size = Pt(11)
        rt.font.color.rgb = RGBColor(40, 50, 60)
        return p

    # ========================== PÁGINA 1: PORTADA & ÍNDICE ==========================
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(30)

    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_after = Pt(6)
    rb = p_badge.add_run("PROYECTO INTERMODULAR • 2º DAM")
    rb.font.name = "Calibri"
    rb.font.size = Pt(11)
    rb.font.bold = True
    rb.font.color.rgb = RGBColor(0, 180, 150)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.line_spacing = 1.1
    rt = p_title.add_run("LeadCraft AI")
    rt.font.name = "Calibri"
    rt.font.size = Pt(30)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(10, 25, 47)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(12)
    p_sub.paragraph_format.line_spacing = 1.2
    rs = p_sub.add_run("Plataforma Inteligente de Prospección Geográfica, Auditoría Digital y Generación Asistida de Soluciones Web para Pequeños Negocios Locales")
    rs.font.name = "Calibri"
    rs.font.size = Pt(12.5)
    rs.font.italic = True
    rs.font.color.rgb = RGBColor(0, 56, 255)

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_after = Pt(12)
    rd = p_div.add_run("—" * 32)
    rd.font.color.rgb = RGBColor(203, 213, 225)

    p_hito = doc.add_paragraph()
    p_hito.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hito.paragraph_format.space_after = Pt(35)
    p_hito.paragraph_format.line_spacing = 1.25
    rh = p_hito.add_run("HITO 1: ANÁLISIS Y CONTEXTO\nDocumento de Viabilidad Inicial, Definición de Alcance y Diseño Preliminar")
    rh.font.name = "Calibri"
    rh.font.size = Pt(11.5)
    rh.font.bold = True
    rh.font.color.rgb = RGBColor(71, 85, 105)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.line_spacing = 1.3
    p_meta.paragraph_format.space_after = Pt(40)
    
    p_meta.add_run("Alumno: ").font.bold = True
    p_meta.add_run("Kevin Muñoz Córcoles\n")
    p_meta.add_run("Curso: ").font.bold = True
    p_meta.add_run("2º Desarrollo de Aplicaciones Multiplataforma (DAM)\n")
    p_meta.add_run("Módulo: ").font.bold = True
    p_meta.add_run("Proyecto Intermodular | Convocatoria 2026/2027\n")
    p_meta.add_run("Fecha de entrega: ").font.bold = True
    p_meta.add_run("23 de Octubre de 2026")

    # Índice de contenidos
    add_h1("Índice del Documento de Viabilidad Inicial", space_before=10, space_after=4)
    toc_lines = [
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
    for tl in toc_lines:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.15
        p_t.paragraph_format.space_after = Pt(1.5)
        r_t = p_t.add_run("• " + tl)
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_page_break()

    # ========================== PÁGINA 2: ANÁLISIS & BENCHMARKING ==========================
    add_h1("01. Título y Descripción del Proyecto")
    add_p("LeadCraft AI es una solución de software B2B SaaS concebida para acelerar la digitalización del comercio local de proximidad. La plataforma integra una interfaz cartográfica interactiva sobre Google Maps que permite a profesionales digitales, agencias de marketing y comerciales explorar barrios o municipios, auditar de forma automática la presencia web de los negocios locales y generar al instante, mediante modelos de IA Generativa (LLM), una landing page profesional con sistema de reservas/citas online y contacto directo por WhatsApp adaptada a la identidad y datos públicos del comercio.")

    add_h1("02. Problema o Necesidad Detectada")
    add_p("A pesar del avance tecnológico, miles de microempresas de proximidad (barberías, talleres mecánicos, restaurantes, centros de estética y fisioterapia) presentan una grave brecha digital. Si bien figuran registrados en Google Maps, un alto porcentaje no dispone de página web propia, carece de certificados de seguridad HTTPS y no ofrece mecanismos para reservar citas online. Esto provoca pérdidas directas de clientes frente a grandes franquicias y una sobrecarga telefónica para los dueños mientras trabajan. Paralelamente, los profesionales y agencias web invierten incontables horas en prospección manual en frío, recopilando datos uno a uno y presentando presupuestos abstractos que los comerciantes suelen rechazar por desconfianza o desconocimiento del resultado final.")

    add_h1("03. Usuarios y Público Objetivo")
    add_p("• Operador Primario (Comercial / Agencia / Freelancer): Desarrolladores noveles de DAM, diseñadores web freelance y pequeñas agencias de marketing que necesitan una herramienta ágil para detectar oportunidades comerciales en su área geográfica, automatizar la generación de propuestas funcionales y elevar drásticamente su tasa de conversión de clientes.")
    add_p("• Beneficiario Final (Dueño del Negocio y Clientes Finales): Propietarios de pymes locales que obtienen una presencia web moderna con reservas online por una fracción del coste tradicional, y sus clientes, que pueden consultar servicios y agendar citas desde su móvil las 24 horas del día.")

    add_h1("04. Benchmarking Competitivo y Soluciones Similares")
    add_p("Se han analizado tres plataformas de referencia en los sectores de generación web, prospección de leads y gestión de citas:")

    # Tabla de benchmarking
    t_bench = doc.add_table(rows=1, cols=4)
    t_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_bench.autofit = False

    b_hdrs = ["Herramienta", "Enfoque / Función", "Puntos Fuertes", "Carencias / Oportunidad LeadCraft"]
    b_widths = [Inches(1.4), Inches(1.5), Inches(1.8), Inches(2.0)]
    
    for i, h in enumerate(t_bench.rows[0].cells):
        h.text = b_hdrs[i]
        h.width = b_widths[i]
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="0A192F"/>')
        h._tc.get_or_add_tcPr().append(shd)
        for p in h.paragraphs:
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.bold = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(255, 255, 255)

    bench_data = [
        ("Wix Studio / Duda (ADI)", "Generadores web basados en IA para crear sitios web corporativos.", "Diseños modernos y plantillas responsive bien estructuradas.", "No incluye motor de prospección geográfica ni detecta carencias de negocios en Google Maps; requiere introducir datos manualmente."),
        ("D7 Lead Finder / LeadEnforce", "Buscadores de leads que extraen datos de contacto desde Google Maps.", "Rápida extracción masiva de correos y teléfonos de negocios.", "Se limita a generar listados de texto (Excel/CSV); no audita necesidades web ni construye ninguna solución interactiva para enseñar al cliente."),
        ("Calendly / Treatwell", "Software especializado en reservas y gestión de citas online.", "Calendarios eficaces con recordatorios automáticos por SMS/correo.", "Son herramientas aisladas que no proporcionan la web del negocio y exigen cuotas mensuales recurrentes elevadas para pequeñas pymes.")
    ]

    for idx, (tool, enf, pf, car) in enumerate(bench_data):
        row = t_bench.add_row().cells
        for j in range(4):
            row[j].width = b_widths[j]
        row[0].text = tool
        row[1].text = enf
        row[2].text = pf
        row[3].text = car

        fill = "F1F5F9" if idx % 2 == 0 else "FFFFFF"
        for j, cell in enumerate(row):
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill}"/>')
            cell._tc.get_or_add_tcPr().append(shd)
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(1.5)
                p.paragraph_format.space_after = Pt(1.5)
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(8.5)
                    r.font.color.rgb = RGBColor(35, 47, 62)
                    if j == 0:
                        r.font.bold = True

    doc.add_page_break()

    # ========================== PÁGINA 3: OBJETIVOS SMART, ALCANCE & RIESGOS ==========================
    add_h1("05. Objetivos Iniciales del Proyecto (Modelo SMART)")
    add_p("• Específico (S): Desarrollar una aplicación funcional multiplataforma que integre Google Places API para localizar comercios locales, ejecute un algoritmo de auditoría digital express y genere una landing page adaptada con widget de citas mediante llamadas a la API de Google Gemini.")
    add_p("• Medible (M): Lograr que el tiempo de análisis y generación completa de la propuesta web sea inferior a 30 segundos por negocio, alcanzando un score de satisfacción técnica del 100% en la validación de código HTML5/Tailwind.")
    add_p("• Alcanzable (A): Utilizar una arquitectura modular en Python (FastAPI) y Flutter/React con plantillas prediseñadas por sector, acotando el alcance para evitar desarrollos inabarcables en el calendario académico.")
    add_p("• Relevante (R): Dotar a los alumnos de DAM de un proyecto con aplicación comercial directa en el mercado de servicios informáticos y alineado con los fondos de digitalización de pymes.")
    add_p("• Temporal (T): Completar el ciclo de desarrollo en tres hitos evaluables antes del término del curso escolar (Hito 1: Octubre; Hito 2: Enero; Hito 3 / Defensa final: Marzo/Abril).")

    add_h1("06. Alcance Mínimo Viable (MVP) y Ampliaciones Futuras")
    add_p("• Funcionalidades del MVP (Versión 1.0 Obligatoria):")
    add_p("  1) Navegación sobre mapa con filtrado por categoría (Hostelería, Salud/Estética, Servicios mecánicos).")
    add_p("  2) Panel de Auditoría Express con cálculo de 'Digital Health Score' (Web, SSL, Reservas, Reseñas).")
    add_p("  3) Generación asistida por IA del copy comercial y ensamblado de Landing Page responsive.")
    add_p("  4) Widget incrustado de selección de fecha y hora para reserva de citas.")
    add_p("  5) Previsualizador interactivo con vista móvil y escritorio.")
    add_p("  6) Exportador de código web en archivo ZIP y generación de informe de auditoría en PDF.")

    add_p("• Ampliaciones Futuras (Post-MVP / Versión 2.0):")
    add_p("  1) Agente conversacional de WhatsApp conectado a IA para confirmación automática de citas 24/7.")
    add_p("  2) Pasarela de pago con Stripe para cobro de reservas o señales bancarias.")
    add_p("  3) Despliegue cloud automatizado en Vercel o Netlify con asignación de subdominios o dominios .es.")

    add_h1("07. Riesgos Iniciales y Medidas Preventivas")
    add_p("• Riesgo 1: Coste y límites de cuota de Google Places API y LLM. Medida: Implementar una capa de almacenamiento en caché local (SQLite/PostgreSQL) para reutilizar datos de comercios ya consultados y diseñar prompts compactos que minimicen el consumo de tokens.")
    add_p("• Riesgo 2: Datos incompletos en Google Maps (falta de teléfono o fotos). Medida: El motor incorporará plantillas inteligentes con contenido por defecto ('fallbacks') para rellenar de forma coherente cualquier campo omitido.")
    add_p("• Riesgo 3: Gestión del tiempo y sobrecarga tecnológica. Medida: Adopción de metodología ágil Scrum con entregas bisemanales y priorización estricta bajo técnica MoSCoW (Must, Should, Could, Won't).")

    doc.add_page_break()

    # ========================== PÁGINA 4: ODS, METODOLOGÍA & CASO DE USO ==========================
    add_h1("08. Vinculación con los Objetivos de Desarrollo Sostenible (ODS)")
    add_p("• ODS 8: Trabajo Decente y Crecimiento Económico (Meta 8.3): LeadCraft AI impulsa de forma directa la digitalización y productividad de las microempresas y trabajadores autónomos, permitiéndoles competir en igualdad de condiciones con grandes cadenas comerciales.")
    add_p("• ODS 9: Industria, Innovación e Infraestructura (Meta 9.3): Facilita el acceso democrático y asequible a tecnologías de inteligencia artificial generativa a comercios que no pueden permitirse grandes presupuestos de software.")
    add_p("• ODS 11: Ciudades y Comunidades Sostenibles (Meta 11.a): Fortalece el tejido comercial de barrio y la economía de proximidad, garantizando la supervivencia de negocios tradicionales en entornos urbanos.")

    add_h1("09. Organización Inicial del Trabajo y Metodología")
    add_p("El proyecto se desarrollará siguiendo el marco de trabajo ágil Scrum apoyado en un tablero Kanban de Trello para la monitorización continua del Product Backlog. El plan de trabajo se estructura en tres Sprints principales: Sprint 1 (Exploración geográfica, conexión con Google Places y motor de auditoría express); Sprint 2 (Integración del motor de IA con Gemini, catálogo de plantillas y widget de reservas); Sprint 3 (Previsualizador en vivo, exportador ZIP, generación del dossier comercial PDF y pruebas de rendimiento).")

    add_h1("10. Caso de Uso Principal Paso a Paso")
    add_p("A continuación se describe el flujo de interacción central de LeadCraft AI de inicio a fin:")
    add_p("1. Selección Geográfica: El operador abre la aplicación, visualiza el mapa de su ciudad y selecciona la categoría 'Peluquerías y Barberías' en el distrito Centro.")
    add_p("2. Detección y Auditoría: El sistema despliega pines sobre los locales encontrados. El operador pulsa sobre 'Barbería Clásica'. El motor de auditoría comprueba que no tiene web activa ni enlace de reservas y asigna un Digital Health Score del 45%.")
    add_p("3. Generación Inteligente: El operador hace clic en 'Generar Solución con IA'. La API extrae el nombre, teléfono, horario y reseñas de Maps, y ensambla en 20 segundos una landing page moderna con los servicios y el widget de citas online.")
    add_p("4. Previsualización y Ajuste: En la pantalla partida, el operador visualiza cómo queda la web en móvil y escritorio, ajustando si lo desea el precio de los cortes o el color corporativo.")
    add_p("5. Exportación y Contacto: Con un clic se descarga el informe de auditoría en PDF y la aplicación genera un mensaje formateado con enlace demo listo para enviar al dueño del local vía WhatsApp Business.")

    doc.add_page_break()

    # ========================== PÁGINA 5: ARQUITECTURA & MOCKUPS ==========================
    add_h1("11. Diagrama de Arquitectura del Sistema")
    add_p("La arquitectura técnica de LeadCraft AI se estructura en cuatro capas desacopladas para garantizar escalabilidad, mantenibilidad y rapidez:")

    diag_path = os.path.join(curr_dir, "diagrama_arquitectura_leadcraft.png")
    if os.path.exists(diag_path):
        p_img_d = doc.add_paragraph()
        p_img_d.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img_d.paragraph_format.space_before = Pt(2)
        p_img_d.paragraph_format.space_after = Pt(2)
        r_d = p_img_d.add_run()
        r_d.add_picture(diag_path, width=Inches(5.8))
        
        p_cap_d = doc.add_paragraph()
        p_cap_d.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap_d.paragraph_format.space_after = Pt(6)
        rcd = p_cap_d.add_run("Figura 1: Arquitectura de Componentes de LeadCraft AI (Frontend, Backend Gateway, APIs Externas y Capa de Datos).")
        rcd.font.name = "Calibri"
        rcd.font.size = Pt(8.5)
        rcd.font.italic = True
        rcd.font.color.rgb = RGBColor(100, 116, 139)

    add_h1("12. Mockups de Pantallas Clave de la Aplicación", space_before=4, space_after=2)
    
    m1_path = os.path.join(curr_dir, "mockup_leadcraft_audit.jpg")
    m2_path = os.path.join(curr_dir, "mockup_leadcraft_generator.jpg")

    # Tabla para colocar los dos mockups lado a lado o apilados
    if os.path.exists(m1_path) and os.path.exists(m2_path):
        t_mock = doc.add_table(rows=1, cols=2)
        t_mock.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_mock.autofit = False

        c1, c2 = t_mock.rows[0].cells
        c1.width = Inches(3.3)
        c2.width = Inches(3.3)

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p1.add_run()
        r1.add_picture(m1_path, width=Inches(3.1))
        p1_cap = c1.add_paragraph()
        p1_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1_cap.add_run("Pantalla 1: Mapa y Auditoría Digital Express.").font.size = Pt(8)

        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r2 = p2.add_run()
        r2.add_picture(m2_path, width=Inches(3.1))
        p2_cap = c2.add_paragraph()
        p2_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2_cap.add_run("Pantalla 2: Generador Web con Widget de Citas.").font.size = Pt(8)

    out_docx = os.path.join(curr_dir, "Hito1_Viabilidad_LeadCraft_Kevin.docx")
    doc.save(out_docx)
    print("Hito 1 Word Document saved at:", out_docx)

if __name__ == "__main__":
    build_word_hito1()
