import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_full_report():
    doc = Document()
    
    # Page Setup: A4, 2.5 cm margins
    for section in doc.sections:
        section.top_margin = Inches(0.984)    # 2.5 cm
        section.bottom_margin = Inches(0.984) # 2.5 cm
        section.left_margin = Inches(0.984)   # 2.5 cm
        section.right_margin = Inches(0.984)  # 2.5 cm
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        
        # Header / Footer setup
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("EcoRural Construcciones · Plan de Transformación Digital (THD) | Kevin · 2º DAM")
        f_run.font.name = "Calibri"
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
    
    # Base Style Settings
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Calibri'
    font_normal.size = Pt(11)
    font_normal.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    style_normal.paragraph_format.space_after = Pt(6)
    
    # Colors Palette
    C_PRIMARY = RGBColor(0x1B, 0x43, 0x32)   # Verde Bosque Profundo
    C_SECONDARY = RGBColor(0x2D, 0x6A, 0x4F) # Verde Salvia Oscuro
    C_ACCENT = RGBColor(0x40, 0x91, 0x6C)    # Verde Medio
    C_MUTED = RGBColor(0x55, 0x55, 0x55)     # Gris Oscuro
    C_LIGHT = "F4F7F5"                       # Fondo filas alternas
    
    def set_cell_background(cell, fill_hex):
        tc_pr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tc_pr.append(shd)

    def set_cell_margins(cell, top=140, bottom=140, left=160, right=160):
        tc_pr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/>'
            f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/>'
            f'<w:right w:w="{right}" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tc_pr.append(tcMar)

    def set_table_borders(table, color="D0DBD3", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        tblBorders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(tblBorders)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = C_PRIMARY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = C_SECONDARY
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = C_ACCENT
        return p

    def add_p(text, bold_prefix="", italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.name = "Calibri"
            r_b.font.size = Pt(11)
            r_b.font.bold = True
            r_b.font.color.rgb = RGBColor(0x1B, 0x43, 0x32)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.italic = italic
        r.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        return p

    def add_bullet(title, desc):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        r_t = p.add_run(title + " ")
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(11)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(0x1B, 0x43, 0x32)
        
        r_d = p.add_run(desc)
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(11)
        r_d.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        return p

    def add_callout(text, title="NOTA DESTACADA"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F2F7F4")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        
        tc_pr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="1B4332"/>'
            f'<w:top w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tc_pr.append(tcBorders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run_t = p.add_run(f"📌 {title}: ")
        run_t.font.name = "Calibri"
        run_t.font.size = Pt(10.5)
        run_t.font.bold = True
        run_t.font.color.rgb = RGBColor(0x1B, 0x43, 0x32)
        
        run_b = p.add_run(text)
        run_b.font.name = "Calibri"
        run_b.font.size = Pt(10.5)
        run_b.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(4)

    def build_custom_table(headers, rows_data, col_widths):
        """Builds a formatted table matching the required structure."""
        tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="B8C9BF", sz="6")
        
        # Header Row
        hdr_cells = tbl.rows[0].cells
        for idx, title in enumerate(headers):
            cell = hdr_cells[idx]
            cell.width = Inches(col_widths[idx])
            set_cell_background(cell, "1B4332")
            set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(title.upper())
            r.font.name = "Calibri"
            r.font.size = Pt(10)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        # Data Rows
        for r_idx, row in enumerate(rows_data):
            row_cells = tbl.rows[r_idx + 1].cells
            bg_color = C_LIGHT if (r_idx % 2 == 1) else "FFFFFF"
            for c_idx, val in enumerate(row):
                cell = row_cells[c_idx]
                cell.width = Inches(col_widths[c_idx])
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=120, bottom=120, left=130, right=130)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = 1.2
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
                
                # Check for subheadings or bold parts
                lines = val.split("\n")
                for l_idx, line in enumerate(lines):
                    if l_idx > 0:
                        p = cell.add_paragraph()
                        p.paragraph_format.line_spacing = 1.2
                        p.paragraph_format.space_after = Pt(0)
                        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    
                    if line.startswith("• "):
                        r_bullet = p.add_run("• ")
                        r_bullet.font.name = "Calibri"
                        r_bullet.font.size = Pt(9.5)
                        r_bullet.font.bold = True
                        r_bullet.font.color.rgb = RGBColor(0x1B, 0x43, 0x32)
                        
                        rest = line[2:]
                        if ":" in rest:
                            b_part, r_part = rest.split(":", 1)
                            rb = p.add_run(b_part + ":")
                            rb.font.name = "Calibri"
                            rb.font.size = Pt(9.5)
                            rb.font.bold = True
                            rb.font.color.rgb = RGBColor(0x1B, 0x43, 0x32)
                            
                            rr = p.add_run(r_part)
                            rr.font.name = "Calibri"
                            rr.font.size = Pt(9.5)
                            rr.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
                        else:
                            rr = p.add_run(rest)
                            rr.font.name = "Calibri"
                            rr.font.size = Pt(9.5)
                            rr.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
                    elif ":" in line and not line.startswith("http"):
                        b_part, r_part = line.split(":", 1)
                        rb = p.add_run(b_part + ":")
                        rb.font.name = "Calibri"
                        rb.font.size = Pt(10)
                        rb.font.bold = True
                        rb.font.color.rgb = RGBColor(0x1B, 0x43, 0x32)
                        
                        rr = p.add_run(r_part)
                        rr.font.name = "Calibri"
                        rr.font.size = Pt(9.5)
                        rr.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
                    else:
                        r_txt = p.add_run(line)
                        r_txt.font.name = "Calibri"
                        r_txt.font.size = Pt(9.5 if c_idx > 0 else 10)
                        if c_idx == 0:
                            r_txt.font.bold = True
                            r_txt.font.color.rgb = RGBColor(0x1B, 0x43, 0x32)
                        else:
                            r_txt.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
                            
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(4)
        p_sp.paragraph_format.space_after = Pt(6)

    # =========================================================================
    # PORTADA
    # =========================================================================
    p_cover_top = doc.add_paragraph()
    p_cover_top.paragraph_format.space_before = Pt(40)
    p_cover_top.paragraph_format.space_after = Pt(8)
    p_cover_top.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cat = p_cover_top.add_run("DIGITALIZACIÓN APLICADA AL SISTEMA PRODUCTIVO · 2º DAM")
    r_cat.font.name = "Calibri"
    r_cat.font.size = Pt(12)
    r_cat.font.bold = True
    r_cat.font.color.rgb = C_ACCENT
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(14)
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.line_spacing = 1.2
    r_t1 = p_title.add_run("TRANSFORMACIÓN DIGITAL EN ENTORNOS RURALES\n")
    r_t1.font.name = "Calibri"
    r_t1.font.size = Pt(24)
    r_t1.font.bold = True
    r_t1.font.color.rgb = C_PRIMARY
    
    r_t2 = p_title.add_run("Plan Integral de Implementación de THD para EcoRural Construcciones")
    r_t2.font.name = "Calibri"
    r_t2.font.size = Pt(17)
    r_t2.font.bold = True
    r_t2.font.color.rgb = C_SECONDARY
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(45)
    p_sub.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.line_spacing = 1.3
    r_sub = p_sub.add_run(
        "Modernización de procesos internos, desarrollo de viviendas inteligentes sostenibles "
        "y transformación hacia 'Smart Villages' comarcales con impacto medioambiental positivo."
    )
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = C_MUTED
    
    # Metadata Box on Cover Page
    tbl_meta = doc.add_table(rows=1, cols=1)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_meta = tbl_meta.cell(0, 0)
    set_cell_background(c_meta, "F0F4F2")
    set_cell_margins(c_meta, top=200, bottom=200, left=240, right=240)
    set_table_borders(tbl_meta, color="1B4332", sz="8")
    
    pm = c_meta.paragraphs[0]
    pm.paragraph_format.line_spacing = 1.3
    pm.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    meta_items = [
        ("Alumno:", "Kevin"),
        ("Módulo Profesional:", "Digitalización Aplicada al Sistema Productivo"),
        ("Ciclo Formativo:", "2º Grado Superior en Desarrollo de Aplicaciones Multiplataforma (DAM)"),
        ("Rol en el Proyecto:", "Asesor Tecnológico para Carlos y Esther (Fundadores de EcoRural)"),
        ("Entorno y Caso:", "EcoRural Construcciones S.L. · Comarca Rural Interconectada"),
        ("Convocatoria / Curso:", "2025 - 2026"),
        ("Entrega:", "Informe Técnico y Presentación para Aules")
    ]
    for idx, (label, val) in enumerate(meta_items):
        if idx > 0:
            pm = c_meta.add_paragraph()
            pm.paragraph_format.line_spacing = 1.3
            pm.paragraph_format.space_after = Pt(2)
        rl = pm.add_run(f"{label:<24} ")
        rl.font.name = "Calibri"
        rl.font.size = Pt(10.5)
        rl.font.bold = True
        rl.font.color.rgb = C_PRIMARY
        
        rv = pm.add_run(val)
        rv.font.name = "Calibri"
        rv.font.size = Pt(10.5)
        rv.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        
    p_bot = doc.add_paragraph()
    p_bot.paragraph_format.space_before = Pt(60)
    p_bot.paragraph_format.space_after = Pt(0)
    p_bot.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_bot = p_bot.add_run("OCTUBRE 2026")
    r_bot.font.name = "Calibri"
    r_bot.font.size = Pt(10)
    r_bot.font.color.rgb = C_MUTED
    
    doc.add_page_break()

    # =========================================================================
    # TABLA DE CONTENIDO (ÍNDICE)
    # =========================================================================
    add_h1("Tabla de Contenido")
    add_p(
        "El presente informe recoge la investigación, análisis tecnológico y hoja de ruta estratégica para "
        "la implantación de Tecnologías Habilitadoras Digitales (THD) en la empresa EcoRural Construcciones. "
        "A continuación se detalla la estructura jerárquica del plan:",
        italic=True
    )
    
    toc_items = [
        ("1. Introducción y Contexto Estratégico", "3"),
        ("   1.1. Contexto de Negocio: EcoRural Construcciones y la Visión de Carlos y Esther", "3"),
        ("   1.2. El Reto Rural: Llegada de Nuevos Pobladores y Teletrabajo", "3"),
        ("   1.3. Estado del Parque Edificado y Normativas Sostenibles Municipales", "4"),
        ("   1.4. La Oficina y Vivienda Piloto como Showroom Tecnológico Demostrador", "4"),
        ("2. Tarea 1: Análisis de las THD Aplicables a EcoRural (Procesos Internos)", "5"),
        ("   2.1. Selección y Justificación Técnica de las THD en Gestión y Diseño", "5"),
        ("   2.2. Tabla de Implementación de THD en Procesos Internos y Beneficios Empresariales", "7"),
        ("3. Tarea 2: Análisis de las THD Aplicables en las Viviendas", "8"),
        ("   3.1. Arquitectura Inteligente y Métodos Constructivos Avanzados", "8"),
        ("   3.2. Tabla de Implementación de THD en Viviendas y Ventajas para el Usuario", "10"),
        ("4. Tarea 3: Análisis de las THD Aplicables a los Pueblos (Zonas Comunes)", "11"),
        ("   4.1. Filosofía 'Smart Village': Modernización sin Pérdida de Identidad Tradicional", "11"),
        ("   4.2. Tabla de Implementación de THD en Calles, Parques y Zonas Comunes", "13"),
        ("5. Tarea 4: Evaluación del Impacto Social y Medioambiental", "14"),
        ("   5.1. Contribución al Desarrollo Sostenible y Descarbonización Rural", "14"),
        ("   5.2. Impacto Social: Rejuvenecimiento Demográfico, Empleo y 'Silver Economy'", "15"),
        ("   5.3. Análisis de Riesgos Potenciales y Medidas de Mitigación", "16"),
        ("6. Plan de Implementación y Toma de Decisiones para Carlos y Esther", "17"),
        ("   6.1. Fases de Ejecución: Del Despacho Técnico al Despliegue Comarcal", "17"),
        ("   6.2. Cronograma y Presupuesto Estimado de Digitalización", "18"),
        ("7. Valoración Final y Conclusiones Estratégicas", "19"),
        ("8. Defensa del Proyecto: Presentación Ejecutiva y Enlace a Aules", "20")
    ]
    
    tbl_toc = doc.add_table(rows=len(toc_items), cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_toc, color="E0E6E2", sz="4")
    for idx, (t_sec, t_pg) in enumerate(toc_items):
        r_c = tbl_toc.rows[idx].cells
        r_c[0].width = Inches(5.8)
        r_c[1].width = Inches(0.7)
        set_cell_margins(r_c[0], top=40, bottom=40, left=60, right=60)
        set_cell_margins(r_c[1], top=40, bottom=40, left=60, right=60)
        
        p0 = r_c[0].paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(t_sec)
        r0.font.name = "Calibri"
        r0.font.size = Pt(10)
        if not t_sec.startswith("   "):
            r0.font.bold = True
            r0.font.color.rgb = C_PRIMARY
        else:
            r0.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
            
        p1 = r_c[1].paragraphs[0]
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(t_pg)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        r1.font.color.rgb = C_MUTED
        
    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 1: INTRODUCCIÓN Y CONTEXTO ESTRATÉGICO
    # =========================================================================
    add_h1("1. Introducción y Contexto Estratégico")
    
    add_h2("1.1. Contexto de Negocio: EcoRural Construcciones y la Visión de Carlos y Esther")
    add_p(
        "EcoRural Construcciones es una empresa fundada por Carlos y Esther, dos jóvenes arquitectos que, "
        "tras formarse y adquirir experiencia en el sector de la edificación y las nuevas tecnologías aplicadas, "
        "han decidido regresar a la comarca rural donde crecieron para transformar radicalmente el modelo productivo "
        "de la construcción en su entorno de origen."
    )
    add_p(
        "La empresa nace con una misión clara: demostrar que la edificación sostenible de alta eficiencia energética, "
        "el respeto escrupuloso por la arquitectura tradicional de piedra y madera, y la incorporación de vanguardia de "
        "las Tecnologías Habilitadoras Digitales (THD) no son conceptos antagónicos, sino sinérgicos. Carlos y Esther "
        "pretenden romper con el falso dilema que sitúa la alta tecnología exclusivamente en las grandes urbes, "
        "acercando la digitalización integral como palanca tractora para la modernización socioeconómica rural."
    )
    
    add_h2("1.2. El Reto Rural: Llegada de Nuevos Pobladores y Teletrabajo")
    add_p(
        "El ámbito de actuación de EcoRural abarca una comarca compuesta por varios municipios de pequeña dimensión "
        "separados entre sí por apenas 3 a 8 kilómetros. En los últimos años, este territorio está experimentando un "
        "fenómeno demográfico inédito: la llegada progresiva de familias jóvenes y profesionales altamente cualificados "
        "que, gracias a la consolidación del teletrabajo y la expansión de redes de conectividad troncal, buscan abandonar "
        "la densidad y el estrés de las metrópolis."
    )
    add_p(
        "Estos nuevos residentes aspiran a disfrutar del contacto directo con la naturaleza, la tranquilidad y el bienestar "
        "propio del campo, pero sin renunciar a ninguna de las prestaciones, confort térmico, conectividad digital y "
        "servicios inteligentes característicos de la vida del siglo XXI. Se genera así una demanda latente de viviendas "
        "modernas que combinen funcionalidad laboral remota, eficiencia y automatización."
    )
    
    add_h2("1.3. Estado del Parque Edificado y Normativas Sostenibles Municipales")
    add_p(
        "Frente a esta creciente demanda, la realidad inmobiliaria de la comarca presenta una notable limitación: la mayor "
        "parte del parque residencial está formado por construcciones de gran antigüedad, con graves deficiencias de aislamiento "
        "térmico y acústico, humedades por capilaridad, instalaciones obsoletas y una distribución espacial inadecuada para el trabajo "
        "digital, requiriendo en la mayoría de los casos intervenciones de rehabilitación integral o reedificación."
    )
    add_p(
        "Conscientes de esta situación, los consistorios de la zona han consensuado una serie de ordenanzas y medidas de fomento "
        "urbanístico para impulsar viviendas de alta eficiencia energética que preserven rigurosamente la estética, la volumetría y "
        "los materiales vernáculos (mampostería de piedra, cubiertas de teja o pizarra, carpinterías de madera). EcoRural "
        "encaja de manera óptima en esta estrategia municipal al plantear un modelo de construcción asequible, ecológico "
        "e hiperconectado."
    )
    
    add_h2("1.4. La Oficina y Vivienda Piloto como Showroom Tecnológico Demostrador")
    add_p(
        "Con el propósito de vencer la resistencia cultural al cambio y evidenciar de forma palpable las ventajas de su modelo, "
        "Carlos y Esther han tomado la decisión estratégica de erigir una construcción piloto. Este espacio cumplirá una "
        "doble función:"
    )
    add_bullet("Sede Corporativa y Oficina Técnica:", "Espacio de trabajo digitalizado donde se coordinan los proyectos mediante metodología BIM, computación en la nube, inspección aérea y atención telemática.")
    add_bullet("Vivienda Piloto y Showroom Interactivo:", "Espacio demostrador real donde futuros compradores, técnicos municipales y vecinos pueden experimentar en primera persona el confort térmico pasivo, la domótica asistencial, el autoconsumo energético inteligente y la integración arquitectónica.")
    
    add_callout(
        "La vivienda piloto actuará como el banco de pruebas físico (Living Lab) donde se validarán todas las THD antes "
        "de su comercialización a gran escala, minimizando riesgos y asegurando la máxima fiabilidad técnica.",
        "ROL DEL LIVING LAB PILOTO"
    )

    # =========================================================================
    # SECCIÓN 2: TAREA 1 - THD EN PROCESOS INTERNOS
    # =========================================================================
    add_h1("2. Tarea 1: Análisis de las THD Aplicables a EcoRural (Procesos Internos)")
    
    add_h2("2.1. Selección y Justificación Técnica de las THD en Gestión y Diseño")
    add_p(
        "Adoptando el rol de Carlos y Esther, se ha investigado cómo la tecnología digital puede transformar los procesos "
        "internos de EcoRural Construcciones desde sus cimientos. La digitalización interna no persigue un fin estético, "
        "sino la optimización drástica de los recursos, la reducción de costes operativos, la eliminación de errores de ejecución "
        "en obra y la fluidez en la toma de decisiones."
    )
    add_p(
        "Para lograr estos objetivos, se han seleccionado seis Tecnologías Habilitadoras Digitales clave, plenamente integradas "
        "en el ciclo productivo de la oficina técnica:"
    )
    
    add_bullet("Building Information Modeling (BIM 5D/6D) y Gemelos Digitales:", "Evolución del CAD 2D tradicional a un modelo virtual inteligente en 3D que integra datos geométricos, costes económicos (5D) y parámetros de sostenibilidad y ciclo de vida de materiales (6D). Permite detectar colisiones estructurales o de fontanería antes de comenzar la excavación.")
    add_bullet("Cloud Computing y Entorno Común de Datos (CDE):", "Infraestructura en la nube con repositorios centralizados y sincronización instantánea entre ordenadores de oficina y dispositivos móviles/tablets de jefes de obra y operarios en campo.")
    add_bullet("Drones Fotogramétricos con Cámaras Termográficas:", "UAVs comerciales adaptados para levantamiento topográfico de parcelas escarpadas, inspección de cubiertas en ruinas sin riesgo de caídas y ortofotografía periódica de evolución de obra.")
    add_bullet("Inteligencia Artificial Generativa y Diseño Bioclimático:", "Algoritmos que analizan datos climáticos históricos de la comarca (radiación solar, vientos dominantes, pluviometría) para calcular automáticamente la orientación idónea, aberturas y sombras de la vivienda.")
    add_bullet("Ciberseguridad Integral y Políticas Zero Trust:", "Protocolos criptográficos para salvaguardar planos confidenciales, copias de seguridad inmutables frente a ataques de secuestro de datos (ransomware) y túneles VPN cifrados para teletrabajadores y personal desplazado.")
    add_bullet("ERP / CRM en la Nube y Automatización de Procesos (RPA):", "Plataforma de gestión integral que automatiza el control presupuestario por partidas, albaranes digitales, compras a aserraderos y canteras locales y facturación electrónica obligatoria.")
    
    add_h2("2.2. Tabla de Implementación de THD en Procesos Internos y Beneficios Empresariales")
    add_p(
        "A continuación se presenta la tabla formal requerida por el enunciado de la Tarea 1, donde se sintetiza la vinculación "
        "directa entre cada THD seleccionada, su aplicación en el proceso interno de EcoRural y los beneficios cuantitativos y "
        "cualitativos que reporta a la empresa:"
    )
    
    # TABLE 1
    t1_headers = ["THD", "PROCESO INTERNO", "BENEFICIOS"]
    t1_rows = [
        [
            "Building Information Modeling (BIM 5D/6D)\n& Gemelo Digital",
            "• Diseño arquitectónico tridimensional paramétrico.\n"
            "• Detección automática de colisiones e interferencias.\n"
            "• Integración directa con mediciones y presupuestos (5D).\n"
            "• Simulación del ciclo de vida y desmantelamiento (6D).",
            "• Reducción de hasta un 30% en sobrecostes y mermas en obra.\n"
            "• Detección precoz de fallos de diseño antes de construir.\n"
            "• Presupuestos automáticos y precisos al milímetro.\n"
            "• Entrega de un Gemelo Digital al cliente para facilitar el mantenimiento preventivo futuro."
        ],
        [
            "Cloud Computing\n& Entorno Común de Datos (CDE)",
            "• Gestión documental centralizada y colaborativa.\n"
            "• Sincronización en tiempo real de planos y fichas técnicas.\n"
            "• Acceso remoto desde obra mediante tablets rugerizadas.\n"
            "• Comunicación directa entre Carlos, Esther y gremios.",
            "• Eliminación total del papel y riesgo de planos desactualizados.\n"
            "• Teletrabajo fluido para el equipo técnico sin fricciones.\n"
            "• Ahorro de desplazamientos innecesarios entre pueblos.\n"
            "• Trazabilidad total de revisiones, firmas y aprobaciones."
        ],
        [
            "Drones con Fotogrametría\n& Visión Artificial",
            "• Levantamiento topográfico 3D de fincas rústicas.\n"
            "• Inspección visual y termográfica de tejados a rehabilitar.\n"
            "• Auditoría periódica y fotográfica del avance de la obra.\n"
            "• Control de acopios de materiales y tierras.",
            "• Reducción del tiempo de topografía de 5 días a 2 horas.\n"
            "• Cero riesgos de caídas en altura para los arquitectos.\n"
            "• Detección prematura de fugas térmicas o fisuras en muros.\n"
            "• Generación de vídeos hiperrealistas para marketing comercial."
        ],
        [
            "Inteligencia Artificial (IA)\n& Simulación Bioclimática",
            "• Diseño generativo de distribuciones espaciales óptimas.\n"
            "• Cálculo predictivo de trayectorias solares y sombras.\n"
            "• Modelado de ventilación cruzada y comportamiento térmico.\n"
            "• Optimización de espesores de aislamiento natural.",
            "• Aceleración del anteproyecto de 2 semanas a 48 horas.\n"
            "• Garantía técnica de estándar Passivhaus (consumo casi nulo).\n"
            "• Ahorro térmico de por vida para el usuario final.\n"
            "• Ajuste al microclima exacto de cada municipio comarcal."
        ],
        [
            "Ciberseguridad Avanzada\n& Respaldos Regla 3-2-1",
            "• Conexión mediante VPN cifrada con autenticación MFA.\n"
            "• Encriptación de bases de datos de clientes y presupuestos.\n"
            "• Copias de seguridad automáticas en almacenamiento inmutable.\n"
            "• Cortafuegos de siguiente generación (NGFW) en la oficina.",
            "• Protección absoluta de la propiedad intelectual de los proyectos.\n"
            "• Blindaje contra ataques de ransomware y fugas de datos.\n"
            "• Cumplimiento estricto del RGPD europeo ante clientes y banca.\n"
            "• Garantía de continuidad operativa ante incidencias eléctricas."
        ],
        [
            "ERP / CRM Cloud\n& Automatización (RPA)",
            "• Control de compras y stock con proveedores locales.\n"
            "• Emisión automatizada de facturas electrónicas (VeriFactu).\n"
            "• Seguimiento de prospectos, clientes y estado de licencias.\n"
            "• Alertas de desviaciones de plazos y costes por hito.",
            "• Reducción del 75% en tareas administrativas manuales.\n"
            "• Visión global del margen de rentabilidad de cada proyecto.\n"
            "• Pagos puntuales y transparentes a pequeñas empresas locales.\n"
            "• Mejora radical en la fidelización y experiencia de usuario."
        ]
    ]
    build_custom_table(t1_headers, t1_rows, [1.8, 2.7, 2.7])
    
    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 3: TAREA 2 - THD EN LAS VIVIENDAS
    # =========================================================================
    add_h1("3. Tarea 2: Análisis de las THD Aplicables en las Viviendas")
    
    add_h2("3.1. Arquitectura Inteligente y Métodos Constructivos Avanzados")
    add_p(
        "En la segunda fase del plan de implantación, el foco tecnológico se traslada a la propia vivienda. El reto "
        "consiste en transformar el edificio en una entidad viva, eficiente y autónoma, que aproveche las ventajas de la "
        "era digital para proporcionar bienestar al usuario y reducir al mínimo su huella de carbono, manteniendo a la vez "
        "una armonía absoluta con la arquitectura tradicional del valle."
    )
    add_p(
        "Carlos y Esther apuestan por una 'tecnología no invasiva ni estridente': los sistemas avanzados quedan perfectamente "
        "integrados tras los revestimientos de madera y piedra, interactuando con los usuarios de forma natural e intuitiva "
        "mediante las siguientes tecnologías:"
    )
    
    add_bullet("Internet de las Cosas (IoT) y Domótica Estándar Matter/Zigbee:", "Sensorización ubicua de parámetros ambientales interiores (calidad de aire CO2, temperatura zonal, humedad relativa, COVs), control de persianas motorizadas para captación solar pasiva y electroválvulas inteligentes antifugas de corte automático.")
    add_bullet("Gestión Energética Inteligente (Smart Energy) con Inversores Híbridos e IA:", "Generación solar fotovoltaica en cubierta con teja solar integrada, almacenamiento en baterías de litio ferrofosfato (LiFePO4) y bomba de calor aerotérmica. Un algoritmo predictivo cruza la previsión meteorológica comarcal con el precio horario de la electricidad para optimizar la carga y descarga.")
    add_bullet("Fabricación Aditiva (Impresión 3D) en Elementos Singulares:", "Uso de impresoras 3D de gran formato para fabricar elementos de hormigón ecológico y madera técnica reciclada: celosías bioclimáticas a medida con patrones tradicionales, remates de cubierta y canalones ocultos.")
    add_bullet("Realidad Virtual (VR) y Realidad Aumentada (AR) para Clientes y Obra:", "Experiencia inmersiva en el showroom con gafas VR para que el comprador recorra y personalice su casa antes de fabricarla; y cascos con AR para los operarios que proyectan la posición exacta de las instalaciones ocultas (fontanería, cables) sobre los paramentos reales.")
    add_bullet("Blockchain para el 'Pasaporte Digital de la Edificación':", "Registro inmutable en cadena de bloques de los certificados de origen de la madera (FSC), áridos locales de cantera y huella de carbono, junto al historial digital de mantenimiento y garantías de la vivienda.")
    add_bullet("Biometría y Cerraduras Inteligentes Conectadas:", "Sistemas de apertura mediante huella dactilar biométrica o reconocimiento facial 3D, combinados con llaves digitales en smartphone para permitir accesos temporales y seguros a familiares o transportistas.")

    add_h2("3.2. Tabla de Implementación de THD en Viviendas y Ventajas para el Usuario")
    add_p(
        "Se presenta a continuación la tabla estructurada correspondiente a la Tarea 2, especificando la THD, su modo "
        "de aplicación constructivo o habitacional y los beneficios directos que genera para los habitantes y la constructora:"
    )
    
    # TABLE 2
    t2_headers = ["THD", "APLICACIÓN EN VIVIENDA", "BENEFICIOS"]
    t2_rows = [
        [
            "Internet de las Cosas (IoT)\n& Domótica Abierta (Matter)",
            "• Monitorización de calidad de aire (CO2, COVs) y humedad.\n"
            "• Ventilación mecánica controlada (VMC) con recuperación de calor.\n"
            "• Electroválvulas de corte de agua ante fugas detectadas.\n"
            "• Persianas automatizadas según insolación y temperatura.",
            "• Confort térmico y salubridad interior constante para teletrabajar.\n"
            "• Prevención de patologías en muros y maderas por humedad.\n"
            "• Ahorro energético del 25-35% en climatización activa.\n"
            "• Control unificado desde smartphone, voz o pulsadores convencionales."
        ],
        [
            "Sistemas Smart Energy\n& Algoritmos Predictivos IA",
            "• Pérgolas y tejas solares fotovoltaicas integradas estéticamente.\n"
            "• Baterías de almacenamiento LiFePO4 de 10-15 kWh.\n"
            "• Aerotermia de alta eficiencia para suelo radiante y ACS.\n"
            "• IA que decide cuándo verter o almacenar según previsión y tarifas.",
            "• Cobertura del 80-90% de la demanda energética de la vivienda.\n"
            "• Facturas eléctricas mensuales testimoniales o neutras.\n"
            "• Resiliencia total y continuidad eléctrica frente a cortes rurales.\n"
            "• Punto de carga inteligente para coche eléctrico con excedentes solares."
        ],
        [
            "Fabricación Aditiva (3D)\n& Prefabricación Sostenible",
            "• Impresión 3D de celosías cerámicas y aislantes a medida.\n"
            "• Fabricación de encuentros y anclajes estructurales personalizados.\n"
            "• Paneles modulares preensamblados en taller local.\n"
            "• Maquetas a escala 1:20 hiperdetalladas para el cliente.",
            "• Reducción de los residuos de construcción a pie de obra en un 80%.\n"
            "• Acortamiento de los plazos de ejecución de la vivienda en 4 meses.\n"
            "• Integración estética perfecta respetando el estilo tradicional comarcal.\n"
            "• Eliminación de puentes térmicos en detalles singulares complejos."
        ],
        [
            "Realidad Virtual (VR)\n& Realidad Aumentada (AR)",
            "• Showroom con gafas VR en la oficina técnica para paseo virtual.\n"
            "• Selección en tiempo real de acabados, suelos y maderas.\n"
            "• Gafas AR en obra que superponen planos MEP sobre las paredes.\n"
            "• Manual visual interactivo en AR para el mantenimiento del hogar.",
            "• Cero discrepancias o frustraciones: el cliente ve su casa antes de edificar.\n"
            "• Los instaladores no taladran tuberías ocultas ni cometen fallos.\n"
            "• Reducción radical de las modificaciones de obra improvisadas.\n"
            "• Facilidad extrema para que el usuario localice válvulas y cuadros."
        ],
        [
            "Blockchain y Pasaporte\nDigital de Materiales",
            "• Tokenización del Libro del Edificio con garantías y manuales.\n"
            "• Trazabilidad inmutable de maderas sostenibles de bosques locales.\n"
            "• Registro criptográfico de ensayos de hormigón y aislamientos.\n"
            "• Certificación de neutralidad de carbono validada por Smart Contract.",
            "• Acreditación fehaciente de sostenibilidad, evitando el ecoblanqueo.\n"
            "• Revalorización de la vivienda en el mercado inmobiliario de segunda mano.\n"
            "• Bonificación de tipos de interés en hipotecas verdes bancarias.\n"
            "• Historial inalterable de reformas e intervenciones realizadas."
        ],
        [
            "Biometría y Control de\nAccesos Criptográfico",
            "• Manillas y cerraduras con sensor biométrico de huella y rostro 3D.\n"
            "• Generación de códigos digitales temporales para paquetería o visitas.\n"
            "• Vídeoportero IP conectado a smartphone con audio bidireccional.\n"
            "• Automatización de accesos adaptados para personas mayores.",
            "• Comodidad total: adiós a la pérdida de llaves en el monte o campo.\n"
            "• Recepción de paquetes de compras online mientras se teletrabaja.\n"
            "• Accesibilidad universal para personas con movilidad o visión reducida.\n"
            "• Alta seguridad física ante intrusiones en viviendas aisladas."
        ]
    ]
    build_custom_table(t2_headers, t2_rows, [1.8, 2.7, 2.7])
    
    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 4: TAREA 3 - THD EN LOS PUEBLOS
    # =========================================================================
    add_h1("4. Tarea 3: Análisis de las THD Aplicables a los Pueblos (Zonas Comunes)")
    
    add_h2("4.1. Filosofía 'Smart Village': Modernización sin Pérdida de Identidad Tradicional")
    add_p(
        "Carlos y Esther tienen muy presente que la misión de EcoRural no termina en los muros perimetrales de sus parcelas. "
        "Su visión empresarial está indisolublemente ligada a la prosperidad colectiva de la comarca. Atraer a teletrabajadores "
        "y revitalizar la economía requiere que el entorno público municipal ofrezca una calidad de vida de vanguardia, "
        "manteniendo al mismo tiempo su patrimonio histórico, el silencio, el paisaje y las costumbres locales."
    )
    add_p(
        "El concepto de 'Smart Village' (Pueblo Inteligente) que propone EcoRural traslada las soluciones de las grandes ciudades "
        "al contexto rural con una escala proporcionada, económica y de bajo mantenimiento. A través de convenios de colaboración "
        "público-privada con los ayuntamientos de la comarca, se proponen seis actuaciones tecnológicas en zonas comunes:"
    )
    
    add_bullet("Alumbrado Público Inteligente (Smart Lighting con IoT y Telegestión):", "Farolas LED de bajo consumo con sensores de movimiento y luminosidad ambiental que regulan su intensidad lumínica según el flujo de personas o vehículos, minimizando el gasto y respetando la oscuridad natural del cielo rural.")
    add_bullet("Sensorización de Residuos Urbanos y Rutas Dinámicas de Recogida:", "Contenedores públicos dotados de sensores de llenado por ultrasonidos que avisan a la Mancomunidad solo cuando alcanzan el 80% de su capacidad, optimizando los trayectos de los camiones entre los distintos pueblos.")
    add_bullet("Riego Inteligente Telegestionado en Parques y Zonas Verdes:", "Sondas higrométricas enterradas en jardines públicos y plazas que cruzan datos de humedad del suelo con estaciones meteorológicas comarcales, evitando regar en días de lluvia o viento.")
    add_bullet("Infraestructura Comarcal Abierta de Conectividad (LoRaWAN + Puntos WiFi4EU + 5G):", "Red de baja frecuencia y largo alcance (LoRaWAN) financiada en conjunto para alimentar todos los sensores municipales, combinada con puntos Wi-Fi de alta velocidad en plazas mayores para el trabajo al aire libre.")
    add_bullet("Red de Sensores Ambientales y Alerta Temprana de Incendios e Inundaciones:", "Cámaras térmicas con IA instaladas en torres de telecomunicaciones y boyas hidrométricas en cauces de ríos que avisan en segundos a Protección Civil y vecinos ante conatos de fuego o crecidas repentinas.")
    add_bullet("Plataforma Comarcal 'Smart Village' con Dinamización Ciudadana y Realidad Aumentada:", "Aplicación móvil municipal que permite reportar averías (farola rota, bache) con una foto y GPS, reservar instalaciones deportivas comarcales y dinamizar el turismo rural mediante guías en Realidad Aumentada.")

    add_h2("4.2. Tabla de Implementación de THD en Calles, Parques y Zonas Comunes")
    add_p(
        "A continuación se presenta la tabla correspondiente a la Tarea 3, que detalla la tecnología, su aplicación concreta "
        "en espacios compartidos de la comarca y los beneficios generados para los vecinos y la administración pública:"
    )
    
    # TABLE 3
    t3_headers = ["THD", "ZONAS COMUNES", "BENEFICIOS"]
    t3_rows = [
        [
            "Alumbrado Público Inteligente\n(IoT + Telegestión)",
            "• Farolas LED con diseño rústico de forja en calles y plazas.\n"
            "• Sensores de presencia y luminosidad con modulación continua.\n"
            "• Modo reposo (20% de brillo) cuando no hay peatones ni coches.\n"
            "• Alerta automática de luminarias fundidas vía software.",
            "• Reducción de más del 65-70% en la factura eléctrica municipal.\n"
            "• Erradicación de la contaminación lumínica (Certificación Starlight).\n"
            "• Aumento de la sensación de seguridad ciudadana nocturna.\n"
            "• Mantenimiento predictivo sin necesidad de patrullas de revisión."
        ],
        [
            "Gestión Inteligente de\nResiduos Urbanos (IoT)",
            "• Sensores volumétricos de ultrasonidos en islas de contenedores.\n"
            "• Monitorización en tiempo real del porcentaje de llenado.\n"
            "• Algoritmo de optimización de rutas para el camión comarcal.\n"
            "• Sensores térmicos en contenedores para alerta temprana de fuegos.",
            "• Reducción del 45% en consumo de gasóleo y desgaste de camiones.\n"
            "• Eliminación total de contenedores desbordados y malos olores.\n"
            "• Optimización de la mano de obra del personal de la Mancomunidad.\n"
            "• Disminución de emisiones de gases contaminantes en los pueblos."
        ],
        [
            "Riego Inteligente\n(IoT + Predicción Meteorológica)",
            "• Sondas de humedad y temperatura en el suelo de jardines y parques.\n"
            "• Electroválvulas de control zonificado conectadas por radiofrecuencia.\n"
            "• Algoritmo que cancela el riego si se pronostica lluvia o helada.\n"
            "• Detección automática de roturas en tuberías municipales.",
            "• Ahorro de más del 50% de agua potable en el mantenimiento municipal.\n"
            "• Parques infantiles y zonas verdes públicas en estado óptimo de salud.\n"
            "• Protección de los acuíferos y embalses en periodos de sequía estival.\n"
            "• Supresión de charcos, fugas inadvertidas y desperdicio hídrico."
        ],
        [
            "Red Comarcal LoRaWAN\n& Puntos WiFi Públicos",
            "• Red de 3 antenas LoRaWAN comarcales para cobertura total rural.\n"
            "• Puntos de acceso Wi-Fi gratuitos de alta velocidad en plazas (WiFi4EU).\n"
            "• Conectividad abierta para sensores agrícolas y ganaderos locales.\n"
            "• Conexión de respaldo vía satélite para servicios de emergencia.",
            "• Red pública y gratuita para teletrabajar en plazas y parques públicos.\n"
            "• Infraestructura compartida a bajísimo coste para todos los ayuntamientos.\n"
            "• Dinamización tecnológica del sector primario local (agricultura 4.0).\n"
            "• Inclusión digital de jóvenes y visitantes en todo el espacio público."
        ],
        [
            "Monitorización Ambiental\n& Alerta Temprana de Riesgos",
            "• Cámaras termográficas con visión IA para vigilar masas forestales.\n"
            "• Sensores de caudal por ultrasonidos en puentes y vados de ríos.\n"
            "• Red de estaciones de calidad de aire (partículas, polen, ozono).\n"
            "• Sistema comarcal de envío de alertas automáticas SMS/App a vecinos.",
            "• Detección de incendios forestales en menos de 5 minutos desde su inicio.\n"
            "• Evacuación preventiva ante riadas e inundaciones antes de desbordes.\n"
            "• Tranquilidad y protección del patrimonio natural y las vidas humanas.\n"
            "• Datos abiertos medioambientales de interés para la salud pública."
        ],
        [
            "Plataforma Digital Comarcal\n& Turismo con Realidad Aumentada",
            "• App móvil ciudadana para reporte de baches y averías con foto/GPS.\n"
            "• Reserva telemática de pistas de pádel, frontón o centros cívicos.\n"
            "• Tablón de bandos municipales y empleo local en smartphone.\n"
            "• Señalización turística con códigos QR y modelos 3D en Realidad Aumentada.",
            "• Participación ciudadana activa y resolución rápida de incidencias.\n"
            "• Aumento del turismo cultural y gasto en comercios y restaurantes.\n"
            "• Eliminación de trámites presenciales burocráticos en consistorios.\n"
            "• Cohesión comunitaria entre los habitantes de los distintos municipios."
        ]
    ]
    build_custom_table(t3_headers, t3_rows, [1.8, 2.7, 2.7])
    
    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 5: TAREA 4 - IMPACTO SOCIAL Y MEDIOAMBIENTAL
    # =========================================================================
    add_h1("5. Tarea 4: Evaluación del Impacto Social y Medioambiental")
    
    add_h2("5.1. Contribución al Desarrollo Sostenible y Descarbonización Rural")
    add_p(
        "El respeto al medio ambiente constituye uno de los principios fundacionales innegociables de EcoRural Construcciones. "
        "La integración de las THD no debe concebirse como un mero añadido técnico, sino como el catalizador esencial para "
        "alcanzar la neutralidad climática y regenerar el entorno comarcal. La empresa fundamenta su estrategia en cuatro ejes:"
    )
    add_bullet("Eficiencia Energética y Descarbonización Activa:", "Las viviendas desarrolladas bajo estándar Passivhaus y dotadas de gestión energética con IA consumen hasta un 90% menos de energía que las construcciones tradicionales de la zona. Al generar su propia electricidad limpia mediante solar fotovoltaica y aerotermia, evitan la emisión de más de 4,2 toneladas de CO2 al año por hogar, actuando como sumideros de carbono descentralizados.")
    add_bullet("Economía Circular y Materiales de Proximidad (Kilómetro Cero):", "El modelado BIM permite calcular con exactitud los despieces de piedra local, madera certificada de bosques comarcales y tierra compactada. En las tareas de rehabilitación, el 80% de los cascotes pétreos y vigas sanas son reutilizados in situ tras su escaneado digital, reduciendo el transporte pesado por carreteras locales y la extracción en canteras.")
    add_bullet("Preservación de los Recursos Hídricos y del Suelo:", "La implementación de redes de saneamiento separativas con depuración biológica por fitodepuración (humedales artificiales) y la monitorización IoT del ciclo del agua devuelven el recurso tratado al subsuelo o al riego agrícola sin vertidos contaminantes a los ríos de la comarca.")
    add_bullet("Protección de la Biodiversidad y del Cielo Oscuro:", "El alumbrado público inteligente y la orientación bioclimática de las viviendas reducen drásticamente la radiación lumínica y acústica, favoreciendo el descanso de las aves nocturnas, polinizadores y fauna autóctona, y preservando el cielo como recurso científico y turístico.")

    add_h2("5.2. Impacto Social: Rejuvenecimiento Demográfico, Empleo y 'Silver Economy'")
    add_p(
        "En la dimensión social, el modelo de EcoRural representa una respuesta directa y estructurada frente al drama de la "
        "'España Vaciada', el despoblamiento y el envejecimiento crónico de los núcleos rurales:"
    )
    add_bullet("Fijación de Jóvenes y Atracción de Nómadas Digitales:", "La disponibilidad de viviendas asequibles, con diseño vanguardista, bajo coste de mantenimiento y conectividad tecnológica garantizada convierte a la comarca en un destino de primer orden para teletrabajadores, autónomos digitales y familias con hijos, reactivando las matrículas en las escuelas rurales y el comercio de proximidad.")
    add_bullet("Creación de Empleo Cualificado Local:", "EcoRural no desplaza a los gremios tradicionales, sino que los capacita. Se articulan programas de formación para que albañiles, electricistas y fontaneros comarcales aprendan a instalar sistemas domóticos Matter, cableado estructurado, aerotermia y sensores IoT, elevando el valor añadido del tejido laboral local.")
    add_bullet("Envejecimiento Activo y 'Silver Economy':", "Las THD en el hogar no son solo para jóvenes. Mediante una domótica asistencial no invasiva (sensores de presencia que guían al baño de noche con luz tenue para evitar caídas, detección de inactividad anómala, control por voz sencillo y telemedicina), las personas mayores pueden permanecer viviendo con total seguridad y dignidad en sus casas de siempre, sin verse forzadas a mudarse a residencias de la capital.")

    add_h2("5.3. Análisis de Riesgos Potenciales y Medidas de Mitigación")
    add_p(
        "Toda implantación tecnológica en entornos tradicionales conlleva riesgos potenciales que deben identificarse "
        "con rigor para diseñar planes de mitigación eficaces:"
    )
    
    # TABLE 4 (Risks & Mitigations)
    t4_headers = ["RIESGO POTENCIAL", "DESCRIPCIÓN DEL IMPACTO", "MEDIDA DE MITIGACIÓN (ECORURAL)"]
    t4_rows = [
        [
            "Riesgo 1: Ruptura Estética\ny Paisajística Vernácula",
            "Introducción de elementos tecnológicos visibles (paneles solares reflectantes, farolas futuristas) que dañen la identidad arquitectónica de piedra y madera.",
            "• Integración arquitectónica oculta: tejas solares mate de color pizarra o arcilla.\n"
            "• Canalizaciones invisibles y sensores embutidos en carpinterías tradicionales.\n"
            "• Farolas municipales de forja artesanal que alojan en su interior las placas LED e IoT."
        ],
        [
            "Riesgo 2: Brecha Digital\ny Exclusión de Mayores",
            "Sentimiento de frustración o impotencia entre los vecinos ancianos ante interfaces complejas en smartphone o cuadros de control ininteligibles.",
            "• Automatización 'invisible': el sistema actúa solo sin requerir interacción.\n"
            "• Mantenimiento de mandos físicos, pulsadores tradicionales e interfaces de voz.\n"
            "• Talleres comunitarios gratuitos de alfabetización digital impartidos por Carlos y Esther."
        ],
        [
            "Riesgo 3: Gentrificación Rural\ny Alza de Precios",
            "Llegada masiva de compradores con alto poder adquisitivo que encarezca el suelo y la vivienda, expulsando a la juventud local.",
            "• Modelo constructivo estandarizado de coste controlado mediante prefabricación.\n"
            "• Convenios con ayuntamientos para cesión de suelo público en derecho de superficie.\n"
            "• Fomento de cooperativas de vivienda y reservas para empadronados de la comarca."
        ],
        [
            "Riesgo 4: Obsolescencia y\nBasura Electrónica (e-waste)",
            "Dispositivos IoT cerrados o privativos que queden inservibles en pocos años tras el cierre del fabricante, generando residuos contaminantes.",
            "• Adopción estricta de protocolos abiertos e interoperables (Matter, Zigbee, MQTT).\n"
            "• Arquitectura modular con componentes fácilmente sustituibles y reparables.\n"
            "• Convenio con el Punto Limpio comarcal para reciclaje certificado de RAEEs."
        ]
    ]
    build_custom_table(t4_headers, t4_rows, [1.8, 2.5, 2.9])

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 6: PLAN DE IMPLEMENTACIÓN Y TOMA DE DECISIONES
    # =========================================================================
    add_h1("6. Plan de Implementación y Toma de Decisiones")
    
    add_h2("6.1. Fases de Ejecución: Del Despacho Técnico al Despliegue Comarcal")
    add_p(
        "Para transformar este análisis en una realidad operativa viable y financieramente controlada, Carlos y Esther "
        "deben acometer la implantación mediante una hoja de ruta estructurada en tres fases consecutivas:"
    )
    
    add_bullet("Fase 1: Digitalización del Núcleo Interno (Meses 1 a 4):", "Implantación del software BIM (Revit/Archicad), migración a nube segura colaborativa (CDE), adquisición del dron de fotogrametría y termografía con titulación de piloto oficial para Carlos, despliegue del ERP/CRM y blindaje de ciberseguridad. Inversión estimada: 18.500 €.")
    add_bullet("Fase 2: Construcción y Validación de la Oficina y Vivienda Piloto (Meses 5 a 10):", "Ejecución física del edificio piloto de 90 m² utilizando metodología BIM y fabricación modular. Instalación del ecosistema domótico Matter, aerotermia, baterías híbridas con IA, gafas VR para el showroom de ventas y registro de los materiales en Blockchain. Inversión estimada: 125.000 € (financiada mediante préstamo verde bancario y fondos Next Generation EU / Kit Digital).")
    add_bullet("Fase 3: Escalado Comercial y Despliegue Comarcal 'Smart Village' (Meses 11 a 18):", "Apertura de la vivienda piloto al público. Comercialización de las primeras promociones de viviendas particulares y firma de convenios piloto con dos ayuntamientos de la comarca para desplegar la red LoRaWAN comarcal y sensorizar el alumbrado y residuos. Inversión estimada municipal financiada con fondos de cohesión rural.")

    add_h2("6.2. Cronograma y Presupuesto Estimado de Digitalización")
    add_p(
        "En la siguiente tabla se resumen las partidas presupuestarias de digitalización tecnológica asociadas a la empresa "
        "y su retorno sobre la inversión (ROI) estimado:"
    )
    
    # TABLE BUDGET
    t_bud_headers = ["CONCEPTO TECNOLÓGICO", "INVERSIÓN ESTIMADA", "PLAZO RETORNO (ROI)", "IMPACTO ESTRATÉGICO"]
    t_bud_rows = [
        [
            "Licencias BIM + Formación Avanzada",
            "4.200 € / año",
            "6 meses (1ª obra)",
            "Ahorro de un 30% en desperdicios y erradicación de errores de obra."
        ],
        [
            "Dron Fotogramétrico + Cámara Térmica",
            "3.800 € (único)",
            "4 meses",
            "Ahorro de 1.200 € por topografía subcontratada y seguridad total."
        ],
        [
            "Infraestructura Cloud, ERP/CRM y Ciberseguridad",
            "2.500 € / año",
            "Inmediato",
            "Continuidad de negocio garantizada y automatización administrativa."
        ],
        [
            "Equipamiento Showroom VR y Software Interactivo",
            "3.500 € (único)",
            "2 meses",
            "Tasa de conversión de visitas a contratos de venta superior al 60%."
        ],
        [
            "Kit Living Lab Piloto (Sensores IoT, Matter, IA)",
            "4.500 € (en piloto)",
            "12 meses",
            "Banco de pruebas real para validación técnica y homologación."
        ]
    ]
    build_custom_table(t_bud_headers, t_bud_rows, [2.3, 1.4, 1.5, 2.0])

    # =========================================================================
    # SECCIÓN 7: VALORACIÓN FINAL Y CONCLUSIONES
    # =========================================================================
    add_h1("7. Valoración Final y Conclusiones Estratégicas")
    add_p(
        "Adoptando de manera concluyente la posición de Carlos y Esther, la elaboración de este plan de transformación "
        "digital permite extraer las siguientes valoraciones estratégicas:"
    )
    add_bullet("La Digitalización como Baluarte de la Sostenibilidad:", "Las Tecnologías Habilitadoras Digitales no son un suplemento de lujo; son la herramienta indispensable para que la construcción sostenible sea técnicamente medible, económicamente viable y ambientalmente neutra. Sin BIM no hay residuo cero; sin IA e IoT no hay eficiencia energética real.")
    add_bullet("Viabilidad Económica y Competitiva:", "La inversión tecnológica requerida es moderada y plenamente amortizable en las primeras dos obras gracias al ahorro de costes por mermas, la reducción de plazos de ejecución y la captación preferente de clientes que buscan viviendas preparadas para el teletrabajo.")
    add_bullet("Legado Comarcal y Compromiso Territorial:", "EcoRural demuestra que los pueblos pequeños pueden liderar la vanguardia tecnológica sin traicionar su memoria histórica. El modelo de 'Smart Village' humaniza la digitalización, convirtiéndola en una muralla infranqueable frente al abandono rural y devolviendo la vitalidad a la comarca.")

    # =========================================================================
    # SECCIÓN 8: DEFENSA DEL PROYECTO Y ENLACE A AULES
    # =========================================================================
    add_h1("8. Defensa del Proyecto: Presentación Ejecutiva y Enlace a Aules")
    add_p(
        "En cumplimiento de los requisitos del informe final, se ha desarrollado una presentación ejecutiva multimedia "
        "diseñada específicamente para defender y exponer las conclusiones de este plan ante el tribunal evaluador y la dirección."
    )
    add_p(
        "La presentación está estructurada en formato panorámico 16:9 con un lenguaje visual directo, esquemas conceptuales "
        "y tarjetas explicativas que resumen los puntos clave de cada una de las 4 tareas del proyecto."
    )
    
    add_callout(
        "• Archivo de Presentación: Presentacion_THD_EcoRural_Kevin.pptx\n"
        "• Enlace de Acceso / Carga en Plataforma: https://aules.edu.gva.es/dam2/digitalizacion/proyecto_thd_ecorural_kevin\n"
        "• Formato de Entrega: Documento técnico oficial en formato Word/PDF y diapositivas ejecutivas cargadas en la tarea de Aules.",
        "DATOS DE LA DEFENSA Y ENTREGA EN AULES"
    )
    
    # Save document
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "Plan_Digitalizacion_THD_EcoRural_Kevin.docx")
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")
    return output_path

if __name__ == "__main__":
    create_full_report()
