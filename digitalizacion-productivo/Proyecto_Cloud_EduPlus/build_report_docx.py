import os
import sys
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_full_report():
    doc = Document()

    # Configuración de página: A4, márgenes de 2.5 cm (0.984 pulgadas)
    for section in doc.sections:
        section.top_margin = Inches(0.984)
        section.bottom_margin = Inches(0.984)
        section.left_margin = Inches(0.984)
        section.right_margin = Inches(0.984)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

        # Encabezado y Pie de página
        header = section.header
        h_p = header.paragraphs[0]
        h_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        h_run = h_p.add_run("PROPUESTA DE TRABAJO EN LA NUBE · EDUPLUS ACADEMY")
        h_run.font.name = "Calibri"
        h_run.font.size = Pt(8.5)
        h_run.font.color.rgb = RGBColor(0x66, 0x77, 0x88)

        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("EduPlus Academy · Plan de Implementación Cloud Computing | Kevin (Rol: Rebeca) · 2º DAM")
        f_run.font.name = "Calibri"
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(0x77, 0x77, 0x77)

    # Formato exigido por el enunciado: Calibri 11, justificado, interlineado 1.5
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Calibri'
    font_normal.size = Pt(11)
    font_normal.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    style_normal.paragraph_format.space_after = Pt(6)

    # Paleta de colores corporativa (Azul Académico / Cloud)
    C_PRIMARY = RGBColor(0x12, 0x35, 0x5B)     # Azul Marino Académico (#12355B)
    C_SECONDARY = RGBColor(0x1E, 0x56, 0x8A)   # Azul Medio Cloud (#1E568A)
    C_ACCENT = RGBColor(0x2B, 0x7A, 0xB8)      # Azul Cielo Intenso (#2B7AB8)
    C_PURPLE = RGBColor(0x6A, 0x1B, 0x78)      # Morado (para cabeceras de Tarea 2 como en el PDF original)
    C_MUTED = RGBColor(0x55, 0x55, 0x55)       # Gris Oscuro
    HEX_PRIMARY = "12355B"
    HEX_SECONDARY = "1E568A"
    HEX_PURPLE = "7B1FA2"                      # Morado fiel al PDF de la Tarea 2
    HEX_GREEN = "4E8C2B"                       # Verde fiel al PDF de la Tarea 3
    HEX_LIGHT_BLUE = "F2F6FA"
    HEX_LIGHT_PURPLE = "F9F2FA"
    HEX_LIGHT_GREEN = "F3F8EE"

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

    def set_table_borders(table, color="B8C8D8", sz="6", val="single", inside_v=True):
        tblPr = table._tbl.tblPr
        iv_val = val if inside_v else "none"
        l_val = val if inside_v else "none"
        r_val = val if inside_v else "none"
        tblBorders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="{iv_val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="{l_val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="{r_val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(tblBorders)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
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
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
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
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
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
            r_b.font.color.rgb = C_PRIMARY
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
        r_t.font.color.rgb = C_PRIMARY

        r_d = p.add_run(desc)
        r_d.font.name = "Calibri"
        r_d.font.size = Pt(11)
        r_d.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        return p

    def add_callout(text, title="NOTA CLAVE DEL PROYECTO", border_hex="12355B", bg_hex="F2F6FA"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

        tc_pr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
            f'<w:top w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tc_pr.append(tcBorders)

        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run_t = p.add_run(f"☁️ {title}: ")
        run_t.font.name = "Calibri"
        run_t.font.size = Pt(11)
        run_t.font.bold = True
        run_t.font.color.rgb = C_PRIMARY

        run_b = p.add_run(text)
        run_b.font.name = "Calibri"
        run_b.font.size = Pt(11)
        run_b.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(4)

    def fill_formatted_cell(cell, text, font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold_first_col=False):
        lines = text.split("\n")
        for l_idx, line in enumerate(lines):
            p = cell.paragraphs[0] if l_idx == 0 else cell.add_paragraph()
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.alignment = align

            if line.startswith("• "):
                r_bullet = p.add_run("• ")
                r_bullet.font.name = "Calibri"
                r_bullet.font.size = Pt(font_size)
                r_bullet.font.bold = True
                r_bullet.font.color.rgb = C_PRIMARY

                rest = line[2:]
                if ":" in rest:
                    b_part, r_part = rest.split(":", 1)
                    rb = p.add_run(b_part + ":")
                    rb.font.name = "Calibri"
                    rb.font.size = Pt(font_size)
                    rb.font.bold = True
                    rb.font.color.rgb = C_PRIMARY

                    rr = p.add_run(r_part)
                    rr.font.name = "Calibri"
                    rr.font.size = Pt(font_size)
                    rr.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
                else:
                    rr = p.add_run(rest)
                    rr.font.name = "Calibri"
                    rr.font.size = Pt(font_size)
                    rr.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
            elif ":" in line and not line.startswith("http"):
                b_part, r_part = line.split(":", 1)
                rb = p.add_run(b_part + ":")
                rb.font.name = "Calibri"
                rb.font.size = Pt(font_size)
                rb.font.bold = True
                rb.font.color.rgb = C_PRIMARY

                rr = p.add_run(r_part)
                rr.font.name = "Calibri"
                rr.font.size = Pt(font_size)
                rr.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
            else:
                r_txt = p.add_run(line)
                r_txt.font.name = "Calibri"
                r_txt.font.size = Pt(font_size)
                if bold_first_col:
                    r_txt.font.bold = True
                    r_txt.font.color.rgb = C_PRIMARY
                else:
                    r_txt.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    def build_custom_table(headers, rows_data, col_widths, header_hex=HEX_PRIMARY, alt_hex=HEX_LIGHT_BLUE, border_hex="B8C8D8"):
        tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color=border_hex, sz="6", inside_v=True)

        # Fila de cabecera
        hdr_cells = tbl.rows[0].cells
        for idx, title in enumerate(headers):
            cell = hdr_cells[idx]
            cell.width = Inches(col_widths[idx])
            set_cell_background(cell, header_hex)
            set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(title.upper())
            r.font.name = "Calibri"
            r.font.size = Pt(11)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # Filas de datos
        for r_idx, row in enumerate(rows_data):
            row_cells = tbl.rows[r_idx + 1].cells
            bg_color = alt_hex if (r_idx % 2 == 1) else "FFFFFF"
            for c_idx, val in enumerate(row):
                cell = row_cells[c_idx]
                cell.width = Inches(col_widths[c_idx])
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=100, bottom=100, left=130, right=130)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
                col_align = WD_ALIGN_PARAGRAPH.LEFT if (c_idx == 0 and col_widths[c_idx] <= 2.0) else WD_ALIGN_PARAGRAPH.JUSTIFY
                fill_formatted_cell(
                    cell,
                    val,
                    font_size=11,
                    align=col_align,
                    bold_first_col=(c_idx == 0)
                )

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(4)
        p_sp.paragraph_format.space_after = Pt(6)

    # =========================================================================
    # PORTADA (Requisito: Portada con tu nombre y el título del proyecto)
    # =========================================================================
    p_cover_top = doc.add_paragraph()
    p_cover_top.paragraph_format.space_before = Pt(36)
    p_cover_top.paragraph_format.space_after = Pt(8)
    p_cover_top.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cover_top.paragraph_format.line_spacing = 1.5
    r_cat = p_cover_top.add_run("DIGITALIZACIÓN APLICADA AL SISTEMA PRODUCTIVO · TEMA 4: CLOUD Y EDGE COMPUTING")
    r_cat.font.name = "Calibri"
    r_cat.font.size = Pt(11)
    r_cat.font.bold = True
    r_cat.font.color.rgb = C_ACCENT

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(12)
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.line_spacing = 1.5
    r_t1 = p_title.add_run("PROPUESTA DE TRABAJO EN LA NUBE PARA UNA PEQUEÑA EMPRESA\n")
    r_t1.font.name = "Calibri"
    r_t1.font.size = Pt(22)
    r_t1.font.bold = True
    r_t1.font.color.rgb = C_PRIMARY

    r_t2 = p_title.add_run("Plan Integral de Implementación de Cloud Computing para EduPlus Academy")
    r_t2.font.name = "Calibri"
    r_t2.font.size = Pt(15)
    r_t2.font.bold = True
    r_t2.font.color.rgb = C_SECONDARY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(6)
    p_sub.paragraph_format.space_after = Pt(36)
    p_sub.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.line_spacing = 1.5
    r_sub = p_sub.add_run(
        "Estudio de viabilidad técnica, económica, laboral y medioambiental para la transición del modelo "
        "tradicional en local hacia una arquitectura SaaS en la nube para docencia presencial y remota."
    )
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = C_MUTED

    # Cuadro de metadatos en Portada
    tbl_meta = doc.add_table(rows=1, cols=1)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_meta = tbl_meta.cell(0, 0)
    set_cell_background(c_meta, HEX_LIGHT_BLUE)
    set_cell_margins(c_meta, top=180, bottom=180, left=220, right=220)
    set_table_borders(tbl_meta, color=HEX_PRIMARY, sz="8")

    pm = c_meta.paragraphs[0]
    pm.paragraph_format.line_spacing = 1.5
    pm.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    meta_items = [
        ("Nombre del Alumno:", "Kevin"),
        ("Título del Proyecto:", "Propuesta de Trabajo en la Nube para EduPlus Academy"),
        ("Módulo Profesional:", "Digitalización Aplicada al Sistema Productivo (Tema 4: Cloud y Edge Computing)"),
        ("Ciclo Formativo:", "2º Grado Superior en Desarrollo de Aplicaciones Multiplataforma (2º DAM)"),
        ("Empresa Objeto de Estudio:", "EduPlus Academy — Centro de formación y clases particulares online/presenciales"),
        ("Rol Asumido en el Proyecto:", "Rebeca (Cofundadora y docente, impulsora de la modernización en la nube)"),
        ("Destinatario Interno:", "Samuel (Cofundador y docente, reticente ante tiempos y costes de digitalización)"),
        ("Formato Oficial Aplicado:", "Texto Calibri 11, alineación justificada, interlineado 1.5")
    ]
    for idx, (label, val) in enumerate(meta_items):
        if idx > 0:
            pm = c_meta.add_paragraph()
            pm.paragraph_format.line_spacing = 1.5
            pm.paragraph_format.space_after = Pt(2)
            pm.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        rl = pm.add_run(f"{label} ")
        rl.font.name = "Calibri"
        rl.font.size = Pt(11)
        rl.font.bold = True
        rl.font.color.rgb = C_PRIMARY

        rv = pm.add_run(val)
        rv.font.name = "Calibri"
        rv.font.size = Pt(11)
        rv.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    p_bot = doc.add_paragraph()
    p_bot.paragraph_format.space_before = Pt(42)
    p_bot.paragraph_format.space_after = Pt(0)
    p_bot.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bot.paragraph_format.line_spacing = 1.5
    r_bot = p_bot.add_run("CURSO ACADÉMICO 2025 - 2026 · COMUNIDAD VALENCIANA")
    r_bot.font.name = "Calibri"
    r_bot.font.size = Pt(11)
    r_bot.font.bold = True
    r_bot.font.color.rgb = C_MUTED

    doc.add_page_break()

    # =========================================================================
    # TABLA DE CONTENIDO (Requisito: Tabla de contenido)
    # =========================================================================
    add_h1("Tabla de Contenido")
    add_p(
        "El presente documento constituye el Informe Final de estudio e implementación de servicios de computación "
        "en la nube (cloud computing) para el centro educativo EduPlus Academy, redactado desde la perspectiva de su "
        "cofundadora Rebeca para dar respuesta técnica, pedagógica y financiera a las inquietudes de su socio Samuel. "
        "A continuación se detalla el índice estructurado de contenidos:",
        italic=True
    )

    toc_items = [
        ("1. Introducción y Diagnóstico de la Situación Actual en EduPlus Academy", "3"),
        ("   1.1. Presentación de EduPlus Academy: Historia, Equipo y Oferta Formativa", "3"),
        ("   1.2. Diagnóstico del Modelo Tradicional Local y Riesgos de Pérdida de Datos", "3"),
        ("   1.3. El Dilema Estratégico entre Rebeca y Samuel: Transformación vs. Resistencia", "4"),
        ("2. Tarea 1: ¿Qué tipo de servicio en la nube va a ser necesario?", "6"),
        ("   2.1. ¿Para qué funciones concretas se utilizará la nube en EduPlus Academy?", "6"),
        ("   2.2. Comparativa entre el Alojamiento Tradicional Local y el Modelo Cloud", "9"),
        ("   2.3. ¿Qué modelo de nube (IaaS, PaaS o SaaS) será más adecuado? Justificación", "10"),
        ("   2.4. Niveles de Nube (Pública, Privada, Híbrida) y Rol del Edge/Fog/Mist Computing", "13"),
        ("3. Tarea 2: Análisis de Ventajas e Inconvenientes (Convencer a Samuel)", "14"),
        ("   3.1. Enfoque del Argumentario: Empatía, Datos Reales y Mitigación de Temores", "14"),
        ("   3.2. Tabla Oficial de la Tarea 2: Cambios Económicos, Empleados y Medioambientales", "14"),
        ("   3.3. Desarrollo Razonado de Respuestas a las Objeciones de Samuel", "18"),
        ("4. Tarea 3: Estudio Comparativo de Proveedores de Servicios en la Nube", "19"),
        ("   4.1. Análisis de los Tres Proveedores Líderes: Microsoft Azure, Google Cloud e IBM Cloud", "19"),
        ("   4.2. Tabla Oficial de la Tarea 3: Resumen de Servicios Relevantes para EduPlus Academy", "20"),
        ("   4.3. Toma de Decisiones: Selección de la Arquitectura Ganadora y Redundancia", "22"),
        ("5. Plan de Implementación, Hoja de Ruta y Presupuesto Estimado", "23"),
        ("   5.1. Fases de Implantación Gradual sin Interrumpir las Clases (Plan de 4 Semanas)", "23"),
        ("   5.2. Presupuesto Económico y Retorno de la Inversión (ROI) para EduPlus Academy", "23"),
        ("6. Valoración Final y Conclusiones del Proyecto", "25"),
        ("7. Defensa del Proyecto: Presentación Ejecutiva y Enlace de Acceso", "25")
    ]

    tbl_toc = doc.add_table(rows=len(toc_items), cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_toc, color="D6E0EB", sz="4", inside_v=False)
    for idx, (t_sec, t_pg) in enumerate(toc_items):
        r_c = tbl_toc.rows[idx].cells
        r_c[0].width = Inches(5.8)
        r_c[1].width = Inches(0.7)
        set_cell_margins(r_c[0], top=28, bottom=28, left=60, right=60)
        set_cell_margins(r_c[1], top=28, bottom=28, left=60, right=60)

        p0 = r_c[0].paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(0)
        p0.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r0 = p0.add_run(t_sec)
        r0.font.name = "Calibri"
        r0.font.size = Pt(10.5)
        if not t_sec.startswith("   "):
            r0.font.bold = True
            r0.font.color.rgb = C_PRIMARY
        else:
            r0.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

        p1 = r_c[1].paragraphs[0]
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(t_pg)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10.5)
        r1.font.bold = not t_sec.startswith("   ")
        r1.font.color.rgb = C_PRIMARY if not t_sec.startswith("   ") else C_MUTED

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 1: INTRODUCCIÓN Y DIAGNÓSTICO DE SITUACIÓN ACTUAL
    # =========================================================================
    add_h1("1. Introducción y Diagnóstico de la Situación Actual en EduPlus Academy")

    add_h2("1.1. Presentación de EduPlus Academy: Historia, Equipo y Oferta Formativa")
    add_p(
        "EduPlus Academy es un centro de formación y clases particulares, tanto presenciales como online, fundado en el "
        "año 2018 por dos profesores vocacionales: Samuel y Rebeca. Desde su apertura, el centro se ha especializado en "
        "ofrecer apoyo escolar personalizado y cursos de refuerzo académico a estudiantes de Educación Primaria, Educación "
        "Secundaria Obligatoria (ESO) y Bachillerato, complementando su catálogo con talleres prácticos de técnicas de "
        "estudio, orientación académica y preparación intensiva de exámenes oficiales (Pruebas de Acceso a la Universidad - PAU, "
        "certificaciones de inglés de Cambridge y pruebas de acceso a ciclos formativos)."
    )
    add_p(
        "Gracias a la calidad pedagógica de sus clases en grupos reducidos y al trato cercano con las familias, la academia "
        "ha experimentado un crecimiento sostenido desde su fundación, contando en la actualidad con una plantilla consolidada "
        "de 6 docentes y una matrícula activa que supera los 120 alumnos. Sin embargo, este crecimiento en volumen de estudiantes "
        "y profesores no ha ido acompañado de una modernización paralela de su infraestructura tecnológica ni de sus procesos "
        "de gestión documental y académica."
    )

    add_h2("1.2. Diagnóstico del Modelo Tradicional Local: Problemas Operativos y Riesgos de Pérdida de Datos")
    add_p(
        "En la actualidad, EduPlus Academy opera íntegramente bajo un modelo de alojamiento tradicional y local. Toda la "
        "documentación académica y administrativa se gestiona en soporte papel o mediante archivos informáticos dispersos "
        "en los discos duros locales de distintos ordenadores personales. Los informes psicopedagógicos, fichas de seguimiento, "
        "bancos de ejercicios y exámenes se archivan en carpetas físicas de anillas, mientras que el envío de tareas, apuntes "
        "y comunicaciones se realiza de forma desestructurada a través de mensajes de WhatsApp o correos electrónicos sueltos."
    )
    add_p(
        "Como se estudia en el Tema 4 (Cloud Computing y Edge Computing), mantener este modelo tradicional de trabajo en local "
        "expone a una empresa de más de 120 alumnos y 6 trabajadores a graves vulnerabilidades operativas y legales:"
    )

    add_bullet(
        "Riesgo crítico de pérdida de datos por error humano:",
        "Es la causa más habitual de pérdida de información en las empresas. Al trabajar en ordenadores locales sin sincronización "
        "en la nube (exactamente igual que el caso práctico de Marcos, el administrativo citado en el Tema 4), cualquier borrado "
        "accidental, sobrescritura de un examen o cierre sin guardar provoca la pérdida irreversible de horas de trabajo docente."
    )
    add_bullet(
        "Vulnerabilidad ante fallos mecánicos y cortes de suministro eléctrico:",
        "Los discos duros locales son una de las piezas más sensibles de un ordenador. El deterioro físico de un equipo, la caída "
        "accidental de líquido sobre el portátil de un profesor o un simple corte de luz en la academia puede destruir las notas "
        "trimestrales de decenas de estudiantes si no existen copias de seguridad remotas."
    )
    add_bullet(
        "Exposición a virus, malware y ciberdelincuencia:",
        "El intercambio constante de documentos mediante memorias USB entre los 6 profesores o la descarga de adjuntos en "
        "equipos sin protección centralizada expone a la academia al secuestro de datos (ransomware) o infección por virus."
    )
    add_bullet(
        "Riesgo sancionador severo en materia de Protección de Datos (RGPD y AEPD):",
        "EduPlus Academy maneja datos personales altamente sensibles de más de 120 alumnos (la mayoría menores de edad), "
        "incluyendo calificaciones, adaptaciones curriculares, teléfonos familiares y datos bancarios de facturación. Como advierte "
        "el Tema 4 con el caso real de la sanción de 60.000 € impuesta por la Agencia Española de Protección de Datos (AEPD) "
        "en 2019 por el extravío de pendrives sin encriptar, o el caso de 2022 en Japón, enviar notas por WhatsApp personal o "
        "perder una carpeta física o un USB de la academia podría acarrear una multa inasumible que cerraría el negocio."
    )
    add_bullet(
        "Incapacidad para la docencia híbrida y el teletrabajo fluido:",
        "Durante la pandemia, la carencia de una plataforma unificada en la nube obligó a improvisar clases online caóticas, "
        "donde muchos alumnos no podían acceder a sus materiales de estudio ni entregar sus ejercicios a tiempo."
    )

    add_h2("1.3. El Dilema Estratégico entre Rebeca y Samuel: Transformación vs. Resistencia al Cambio")
    add_p(
        "Ante esta problemática, los dos socios fundadores mantienen visiones contrapuestas que este proyecto viene a resolver. "
        "Por un lado, Rebeca (papel que asumimos en este informe) comprende que el futuro de EduPlus Academy pasa necesariamente "
        "por migrar a la nube (cloud computing) para centralizar los recursos didácticos, profesionalizar la comunicación con las "
        "familias y permitir que tanto los 6 docentes como los 120 alumnos trabajen con fluidez de forma presencial o remota."
    )
    add_p(
        "Por otro lado, Samuel manifiesta un temor comprensible en muchas pequeñas empresas: recela de que la digitalización "
        "requiera demasiado tiempo de implantación, suponga un desembolso económico desorbitado y que la formación tecnológica "
        "del profesorado resulte demasiado compleja. El objetivo de este documento es demostrar a Samuel, con argumentos "
        "sólidos, datos reales del sector y una propuesta llave en mano, que alrededor del 80 % de las empresas valoran de forma "
        "altamente positiva la nube en los primeros seis meses tras su implantación y que la solución elegida eliminará la complejidad "
        "técnica desde el minuto uno."
    )

    add_callout(
        "En este proyecto asumimos el papel de Rebeca. Nuestro propósito no es imponer tecnología compleja a Samuel, sino "
        "demostrarle cómo el modelo adecuado de computación en la nube (como el que emplea Sonia con Google Docs o los "
        "docentes de la Comunidad Valenciana con Microsoft Teams) protege el trabajo del centro, ahorra costes y simplifica "
        "la vida diaria de nuestros 6 profesores.",
        "PROPÓSITO DE REBECA EN ESTE INFORME"
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 2: TAREA 1 - ¿QUÉ TIPO DE SERVICIO VA A SER NECESARIO?
    # =========================================================================
    add_h1("2. Tarea 1: ¿Qué tipo de servicio en la nube va a ser necesario?")

    add_h2("2.1. ¿Para qué funciones concretas se utilizará la nube en EduPlus Academy?")
    add_p(
        "Los sistemas basados en la nube (cloud computing) permiten almacenar datos, ejecutar aplicaciones y acceder a recursos "
        "informáticos de manera remota a través de Internet, sin depender de discos duros locales ni de carpetas físicas. Tras "
        "analizar en detalle el funcionamiento diario de EduPlus Academy, la nube se utilizará para digitalizar y transformar "
        "siete funciones concretas e indispensables para el centro:"
    )

    add_bullet(
        "1. Almacenamiento centralizado de materiales de clase (PDF, vídeos, presentaciones):",
        "Se creará un repositorio único en la nube organizado por etapas educativas (Primaria, ESO, Bachillerato), asignaturas "
        "y preparación de exámenes oficiales (PAU, Cambridge, pruebas de acceso) además de los talleres de técnicas de estudio. "
        "En lugar de tener los apuntes dispersos en los ordenadores personales de los 6 profesores o en fotocopias de papel, "
        "todos los PDFs, vídeos explicativos grabados, audios de listening de Cambridge y presentaciones interactivas estarán "
        "alojados en unidades compartidas en la nube, con permisos de acceso por grupo y disponibilidad 24/7 sin ocupar espacio "
        "en la memoria de los móviles u ordenadores de los alumnos."
    )
    add_bullet(
        "2. Gestión de horarios, reservas de tutorías y control de asistencia:",
        "Mediante calendarios compartidos en la nube y aplicaciones de reserva de citas online, la academia gestionará en "
        "tiempo real la ocupación de sus aulas físicas, los cuadrantes de los grupos reducidos y la disponibilidad horaria de "
        "los 6 docentes. Las familias y alumnos podrán reservar tutorías individuales o sesiones de orientación académica desde "
        "su móvil eligiendo los huecos libres, evitando el cruce de mensajes por WhatsApp y los solapamientos de aulas. Asimismo, "
        "los profesores pasarán lista desde una hoja o app en la nube en segundos."
    )
    add_bullet(
        "3. Comunicación institucional, ágil y segura con familias y estudiantes:",
        "Se erradicará el uso de cuentas personales de WhatsApp y correos desorganizados. La nube proporcionará canales "
        "oficiales de comunicación (correo corporativo @eduplusacademy.es, tablón de anuncios en el aula virtual y mensajería "
        "institucional como Microsoft Teams o Google Chat/Classroom) donde las familias recibirán avisos de faltas de asistencia, "
        "convocatorias de reuniones y seguimiento académico cumpliendo estrictamente la Ley de Protección de Datos."
    )
    add_bullet(
        "4. Registro de notas, entrega de tareas y generación de evaluaciones:",
        "A través de un cuaderno de calificaciones digital en la nube (Gradebook), los profesores publicarán tareas, recogerán "
        "las entregas de los alumnos con control automático de fecha y hora, corregirán ejercicios directamente sobre el documento "
        "online sin necesidad de imprimirlo y registrarán las notas de los simulacros de examen. Al finalizar cada trimestre, "
        "los boletines e informes de seguimiento trimestral se generarán de forma automatizada en PDF y se compartirán de manera "
        "privada con cada familia, sustituyendo las antiguas carpetas físicas."
    )
    add_bullet(
        "5. Acceso remoto universal para estudiantes y profesorado (multidispositivo):",
        "Como destaca el Tema 4, el alojamiento en la nube permite acceder a los archivos y programas desde cualquier dispositivo "
        "con conexión a Internet (ordenador de sobremesa del aula, portátil personal, tablet o teléfono móvil Android/iOS), incluso "
        "aunque el dispositivo no sea propio. Así, los 6 docentes podrán preparar sus clases desde casa (teletrabajo) y los más "
        "de 120 alumnos podrán repasar sus materiales desde cualquier lugar o seguir la clase desde casa si están enfermos."
    )
    add_bullet(
        "6. Copias de seguridad automáticas (Backup) de informes y documentos importantes:",
        "La nube protegerá el activo más valioso de EduPlus Academy: los expedientes académicos, informes psicopedagógicos, "
        "materiales didácticos propios y facturación. Gracias al guardado automático continuo (cada pocos segundos, como el caso "
        "de Sonia en el Tema 4) y a las políticas de backup automatizado y versionado de archivos en servidores remotos redundantes, "
        "será imposible perder información aunque se vaya la luz en la academia, se rompa el disco duro de un profesor o alguien "
        "borre un archivo por error humano."
    )
    add_bullet(
        "7. Plataforma unificada para clases online y trabajos colaborativos:",
        "Se dispondrá de un entorno virtual de aprendizaje (LMS) integrado con salas de videoconferencia de baja latencia, "
        "pizarra digital interactiva en la nube y edición simultánea de documentos. Esto permitirá impartir clases particulares "
        "online de alta calidad sin las improvisaciones sufridas en la pandemia, así como realizar dinámicas colaborativas en "
        "los talleres de técnicas de estudio donde varios alumnos trabajen a la vez sobre un mismo esquema o documento online."
    )

    add_p(
        "Para visualizar con total claridad el impacto de estas siete funciones, se presenta la siguiente tabla de "
        "correspondencia operativa entre las necesidades de EduPlus Academy y su materialización en la nube:"
    )

    t_func_headers = ["FUNCIÓN EN EDUPLUS ACADEMY", "SITUACIÓN ACTUAL (LOCAL / PAPEL)", "SOLUCIÓN EN LA NUBE (CLOUD COMPUTING)"]
    t_func_rows = [
        [
            "1. Almacenamiento de materiales\n(PDF, vídeos, presentaciones)",
            "Archivos dispersos en ordenadores distintos, pendrives USB y fotocopias en carpetas físicas.",
            "Repositorio central en la nube (Drive / OneDrive / SharePoint) organizado por niveles (Primaria, ESO, Bachillerato, PAU, Cambridge)."
        ],
        [
            "2. Gestión de horarios,\ntutorías y asistencia",
            "Cuadrantes en papel, reservas manuales por teléfono/WhatsApp y partes de firmas físicos.",
            "Calendarios cloud compartidos, portal web de reserva automática de tutorías (Bookings / Calendar) y registro digital de asistencia."
        ],
        [
            "3. Comunicación con familias\ny estudiantes",
            "Mensajes sueltos por WhatsApp personal y correos dispersos sin trazabilidad ni control RGPD.",
            "Canal oficial unificado en la nube (Teams / Classroom / Correo corporativo) con notificaciones automáticas y privacidad garantizada."
        ],
        [
            "4. Registro de notas,\ntareas y evaluaciones",
            "Exámenes en papel archivados en carpetas físicas; boletines trimestrales redactados a mano o en Word local.",
            "Cuaderno de evaluación en la nube, formularios autocorregibles (Forms) y generación automatizada de informes trimestrales digitales."
        ],
        [
            "5. Acceso remoto para\nalumnos y 6 docentes",
            "Imposible acceder a un archivo si no estás delante del ordenador exacto donde se guardó.",
            "Acceso ubicuo 24/7 desde cualquier PC, portátil, tablet o smartphone con conexión a Internet, facilitando el estudio y el teletrabajo."
        ],
        [
            "6. Copias de seguridad (Backup)\nde informes y documentos",
            "Sin copias de seguridad; riesgo total ante cortes de luz (caso Marcos), rotura de disco duro, pérdida de USB o virus.",
            "Autoguardado cada 5 segundos (caso Sonia), historial de versiones de 30-100 días y copias de seguridad cifradas en centros de datos remotos."
        ],
        [
            "7. Plataforma de clases online\ny trabajo colaborativo",
            "Improvisación durante la pandemia sin plataforma unificada; dificultad de acceso para los alumnos.",
            "Aula virtual LMS (Classroom / Teams) con videollamadas HD (Meet / Teams), pizarra colaborativa y edición simultánea de documentos."
        ]
    ]
    build_custom_table(t_func_headers, t_func_rows, [2.0, 2.2, 2.3])

    add_h2("2.2. Comparativa entre el Alojamiento Tradicional Local de la Academia y el Modelo Cloud")
    add_p(
        "Siguiendo el esquema analítico del apartado 2.2 del Tema 4 (Diferencias entre los dos modelos), en el modelo tradicional "
        "los ordenadores de EduPlus Academy solo almacenan datos localmente, mientras que en el modelo de computación en la nube "
        "los servidores remotos no solo entregan la información al cliente (ordenador o móvil del profesor/alumno), sino que "
        "ejecutan los programas y procesan los cambios directamente en Internet. Analizamos estas cuatro diferencias clave "
        "aplicadas al día a día de Samuel y Rebeca:"
    )

    t_diff_headers = ["CRITERIO", "ALOJAMIENTO TRADICIONAL, LOCAL (ACTUAL EN EDUPLUS)", "CLOUD COMPUTING, ALOJAMIENTO EN LA NUBE (PROPUESTO)"]
    t_diff_rows = [
        [
            "Respuesta",
            "Los equipos locales solo presentan los datos archivados en ese ordenador. Si un docente modifica un examen en casa, el cambio no aparece en la academia.",
            "Los servidores en la nube presentan los datos archivados y ejecutan las aplicaciones online para modificarlos, guardando e incorporando los cambios al instante para todo el equipo."
        ],
        [
            "Almacenamiento",
            "Requiere ordenadores con gran capacidad de disco duro o comprar discos externos/USB para guardar vídeos de clase y PDFs. Si se llenan, no se puede trabajar.",
            "No requiere gran capacidad local porque programas y vídeos están en Internet. Si los 120 alumnos generan más datos, se amplía el espacio en la nube de forma inmediata."
        ],
        [
            "Acceso",
            "Cada uno de los 6 profesores solo puede acceder a sus ejercicios e informes desde el ordenador físico concreto donde los guardó o buscando la carpeta de papel.",
            "Profesores, alumnos y familias pueden acceder a sus materiales, notas y horarios desde cualquier dispositivo con Internet (PC, móvil, tablet), aunque no sea suyo."
        ],
        [
            "Actualización",
            "Exige actualizar periódicamente el hardware (equipos físicos) y comprar o instalar nuevas versiones del software (sistema operativo y suites ofimáticas) ordenador por ordenador.",
            "El proveedor en la nube actualiza automáticamente el software del servidor incluyendo mejoras de seguridad y compatibilidad con Windows, Mac, Android e iOS sin intervención de Samuel."
        ]
    ]
    build_custom_table(t_diff_headers, t_diff_rows, [1.5, 2.5, 2.5])

    add_h2("2.3. ¿Qué modelo de nube (IaaS, PaaS o SaaS) será más adecuado? Justificación Técnica")
    add_p(
        "Como se explica en el apartado 5 del Tema 4 (Contenedores en la nube), los servicios de cloud computing se empaquetan "
        "y distribuyen en tres grandes modelos según el nivel de control y responsabilidad que asume la empresa frente al "
        "proveedor: IaaS (Infrastructure as a Service), PaaS (Platform as a Service) y SaaS (Software as a Service). Para determinar "
        "cuál es el más adecuado para EduPlus Academy, analizamos primero qué implica cada uno utilizando los conceptos y las "
        "analogías didácticas del temario (el símil del coche y la metáfora de las pizzas):"
    )

    add_bullet(
        "IaaS (Infraestructura como Servicio - Infrastructure as a Service):",
        "Consiste en alquilar bajo demanda los componentes físicos básicos de computación en la nube: servidores virtuales, "
        "capacidad de procesamiento (CPU/RAM), almacenamiento de bloques, redes y firewalls (ejemplos: Amazon EC2, Google Compute "
        "Engine o Azure Virtual Machines). En la analogía de la pizza (Actividad 9 del Tema 4), equivale a preparar la pizza en "
        "casa comprando los ingredientes, amasando y controlando el horno; el cliente tiene control total (como la empresa de "
        "banca privada BinagorWorld citada en los apuntes), pero necesita administradores de sistemas (SysAdmin) en plantilla para "
        "configurar sistemas operativos, redes y bases de datos."
    )
    add_bullet(
        "PaaS (Plataforma como Servicio - Platform as a Service):",
        "Ofrece un entorno listo en la nube (hardware, sistema operativo, bases de datos y herramientas de desarrollo) para que "
        "los programadores construyan, prueben y desplieguen sus propias aplicaciones sin preocuparse del mantenimiento físico "
        "del servidor (ejemplos: Google App Engine, Azure App Service o Salesforce). En el símil del coche del Tema 4, el usuario "
        "solo echa gasolina y conduce; y en la analogía de la pizza, equivale a pedir en un restaurante eligiendo tú los ingredientes "
        "y cómo se cocina. Es ideal para empresas que desarrollan software propio (como la distribuidora TorcalMet del Tema 4), "
        "pero requiere contar con desarrolladores informáticos."
    )
    add_bullet(
        "SaaS (Software como Servicio - Software as a Service):",
        "Proporciona aplicaciones completas y listas para ser utilizadas directamente por el usuario final a través de Internet "
        "(ejemplos: Google Workspace, Microsoft 365, webmail corporativo, plataformas educativas online). El proveedor en la nube "
        "gestiona absolutamente todo: desde el hardware, los contenedores, la red y el sistema operativo hasta las actualizaciones, "
        "la ciberseguridad y el mantenimiento del software. En la analogía de la pizza, equivale a pedir una pizza online de tu "
        "pizzería favorita lista para comer: la pizzería se encarga desde la preparación hasta la entrega en tu mesa (como eligió "
        "la empresa DragonTel del Tema 4 para centrarse al 100 % en su negocio sin contratar personal técnico)."
    )

    add_callout(
        "DECISIÓN Y JUSTIFICACIÓN PARA EDUPLUS ACADEMY: El modelo de nube más adecuado para EduPlus Academy es, sin ninguna "
        "duda, el modelo SaaS (Software as a Service).",
        "MODELO ELEGIDO: SaaS (SOFTWARE AS A SERVICE)"
    )

    add_p(
        "Las razones técnicas, organizativas y económicas por las que el modelo SaaS es el idóneo para EduPlus Academy son "
        "las siguientes:"
    )

    add_bullet(
        "1. Especialización docente y ausencia de departamento informático (SysAdmin o Desarrolladores):",
        "Como recoge el propio enunciado, la especialidad de Rebeca, Samuel y los otros 4 profesores es la enseñanza (Primaria, "
        "ESO, Bachillerato, PAU y Cambridge), no la administración de servidores Linux/Windows (que exigiría IaaS) ni la programación "
        "de software a medida (que exigiría PaaS). Con SaaS, los 6 docentes son usuarios finales que utilizan aplicaciones "
        "educativas listas para funcionar desde el primer minuto."
    )
    add_bullet(
        "2. Mantenimiento, seguridad y actualizaciones delegadas al 100 % en el proveedor:",
        "En el modelo SaaS, el proveedor (como Google o Microsoft) se encarga de mantener los servidores, aplicar parches "
        "contra virus y ciberataques, garantizar el cifrado RGPD y actualizar las aplicaciones automáticamente. Esto responde "
        "directamente al mayor temor de Samuel: nadie en la academia tendrá que perder tiempo solucionando fallos técnicos ni "
        "configurando equipos."
    )
    add_bullet(
        "3. Curva de aprendizaje mínima e interfaz amigable:",
        "Las herramientas SaaS educativas (como Google Classroom, Google Docs, Drive, Microsoft Teams o Word Online) poseen "
        "interfaces web y móviles sumamente intuitivas que tanto los 6 profesores como los 120 alumnos y sus familias ya conocen "
        "y manejan en su vida cotidiana."
    )
    add_bullet(
        "4. Coste económico imbatible y sin inversión inicial (CAPEX cero):",
        "Tal como destaca el apartado 5.1.3 del Tema 4, más de una tercera parte de las empresas eligen SaaS por resultar el "
        "sistema más cómodo y económico al no requerir contratar personal informático especializado ni comprar servidores físicos. "
        "Además, en el sector educativo, suites SaaS completas como Google Workspace for Education Fundamentals o Microsoft 365 "
        "Education A1 ofrecen planes gratuitos o de coste simbólico para centros de enseñanza."
    )
    add_bullet(
        "5. Cobertura integral de las 7 necesidades de la academia en una sola suite:",
        "Un único ecosistema SaaS resuelve simultáneamente el almacenamiento (Drive/OneDrive), la edición colaborativa con "
        "autoguardado (Docs/Word Online), las clases por videollamada (Meet/Teams), los horarios y tutorías (Calendar/Bookings), "
        "las tareas y notas (Classroom/Teams Tareas) y las copias de seguridad automáticas."
    )

    t_models_headers = ["MODELO CLOUD", "QUÉ GESTIONA EL PROVEEDOR", "PERFIL DESTINATARIO / SÍMIL", "¿ADECUADO PARA EDUPLUS ACADEMY?"]
    t_models_rows = [
        [
            "IaaS\n(Infraestructura como Servicio)",
            "Servidores físicos, almacenamiento en bruto, red y virtualización.",
            "Administradores de Sistemas (SysAdmin).\nSímil: Hacer la pizza desde cero en casa.\nCaso Tema 4: BinagorWorld.",
            "NO. Requeriría contratar informáticos para instalar sistemas operativos, configurar cortafuegos y mantener servidores."
        ],
        [
            "PaaS\n(Plataforma como Servicio)",
            "Infraestructura + Sistema Operativo + Bases de datos y entorno de ejecución.",
            "Desarrolladores de Software.\nSímil: Echar gasolina y conducir / Pizza a medida.\nCaso Tema 4: TorcalMet.",
            "NO (como uso principal). Los 6 profesores no son programadores para desarrollar desde cero su propia plataforma de clases."
        ],
        [
            "SaaS\n(Software como Servicio)",
            "Todo incluido: Infraestructura, SO, bases de datos, aplicaciones, seguridad y soporte.",
            "Usuario Final (Profesores, alumnos, familias).\nSímil: Pedir la pizza lista a domicilio.\nCaso Tema 4: DragonTel.",
            "SÍ ( ÓPTIMO ). Aplicaciones listas para usar (Classroom, Teams, Drive, Docs) sin mantenimiento técnico y con coste mínimo."
        ]
    ]
    build_custom_table(t_models_headers, t_models_rows, [1.5, 1.7, 1.7, 1.6])

    add_h2("2.4. Niveles de Nube (Pública, Privada, Híbrida) y Rol del Edge/Fog/Mist Computing en el Aula")
    add_p(
        "Complementando la elección del modelo SaaS con los conceptos del apartado 4 del Tema 4, analizamos también qué nivel "
        "de despliegue en la nube y qué tecnologías de proximidad (Edge, Fog y Mist) encajan en EduPlus Academy:"
    )

    add_bullet(
        "Nivel de despliegue (Nube Pública con enfoque Híbrido para datos críticos):",
        "De los tres niveles explicados en el apartado 4.2 del Tema 4 (nube pública, nube privada y nube híbrida), una nube privada "
        "propia (como IBM Cloud Private con centro de datos exclusivo) sería inviable por coste para una pequeña academia de 6 "
        "docentes. Por tanto, EduPlus Academy utilizará una Nube Pública de primer nivel (Google Cloud / Microsoft Azure) bajo "
        "demanda para el trabajo habitual (materiales, clases online, calendarios), pudiendo aplicar un esquema de Nube Híbrida "
        "para mantener las copias de seguridad de los expedientes confidenciales y datos fiscales con encriptación privada reforzada."
    )
    add_bullet(
        "Descentralización en las aulas físicas (Edge, Fog y Mist Computing):",
        "Como señala el apartado 4.1 del Tema 4, para reducir la latencia, ahorrar ancho de banda y evitar la sobrecarga cuando "
        "decenas de alumnos se conectan a la vez en las aulas presenciales de EduPlus Academy, las soluciones en la nube se "
        "apoyan en el procesamiento cercano al origen del dato: el Edge Computing (por ejemplo, pizarras digitales interactivas en "
        "el aula o cámaras/tablets que procesan el trazo y el vídeo localmente con respuesta inmediata y baja latencia antes de "
        "sincronizar con la nube), el Fog Computing (un router/nodo local con caché en la propia academia que distribuye los "
        "archivos pesados de vídeo entre las aulas sin saturar la fibra de Internet) y el Mist Computing (dispositivos ligeros "
        "de los alumnos o sensores de confort/CO2 en las aulas que toman decisiones básicas de forma autónoma)."
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 3: TAREA 2 - VENTAJAS E INCONVENIENTES (CONVENCER A SAMUEL)
    # =========================================================================
    add_h1("3. Tarea 2: Análisis de Ventajas e Inconvenientes (Argumentario para Convencer a Samuel)")

    add_h2("3.1. Enfoque del Argumentario: Empatía, Datos Reales y Mitigación de Temores")
    add_p(
        "En esta segunda tarea asumimos plenamente la voz de Rebeca dirigiéndose a su socio y cofundador Samuel. El objetivo "
        "no es ignorar las preocupaciones de Samuel, sino anticipar con honestidad todos los posibles inconvenientes que él "
        "podría plantear (costes recurrentes, tiempo de formación del profesorado, caídas de Internet o huella ecológica de los "
        "servidores) y responder a cada uno con argumentos sólidos fundamentados en el Tema 4."
    )

    add_h2("3.2. Tabla Oficial de la Tarea 2: Cambios Económicos, en los Empleados y Medioambientales")
    add_p(
        "A continuación se presenta la estructura exacta solicitada en el enunciado de la Tarea 2 (organizada en los tres "
        "bloques oficiales: Cambios Económicos, Cambios en los Empleados y Cambios Medioambientales, con sus respectivas "
        "columnas de Ventajas, Inconvenientes y Respuesta razonada a los inconvenientes):"
    )

    # Construcción de la Tabla Oficial de la Tarea 2 (fiel al diseño del PDF de requisitos)
    tbl_t2 = doc.add_table(rows=12, cols=2)
    tbl_t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_t2, color=HEX_PURPLE, sz="6", inside_v=True)

    def format_t2_section_banner(row_idx, title_text):
        row = tbl_t2.rows[row_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.merge(c1)
        set_cell_background(c0, HEX_PURPLE)
        set_cell_margins(c0, top=120, bottom=120, left=150, right=150)
        p = c0.paragraphs[0]
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(title_text.upper())
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    def format_t2_subheaders(row_idx):
        row = tbl_t2.rows[row_idx]
        for idx, text in enumerate(["Ventajas", "Inconvenientes"]):
            cell = row.cells[idx]
            cell.width = Inches(3.25)
            set_cell_background(cell, HEX_LIGHT_PURPLE)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(11)
            r.font.bold = True
            r.font.color.rgb = C_PURPLE

    def format_t2_content_pair(row_idx, ventajas_txt, inconvenientes_txt):
        row = tbl_t2.rows[row_idx]
        for idx, txt in enumerate([ventajas_txt, inconvenientes_txt]):
            cell = row.cells[idx]
            cell.width = Inches(3.25)
            set_cell_background(cell, "FFFFFF")
            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
            fill_formatted_cell(cell, txt, font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold_first_col=False)

    def format_t2_response_row(row_idx, response_txt):
        row = tbl_t2.rows[row_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.merge(c1)
        set_cell_background(c0, "FDFCFE")
        set_cell_margins(c0, top=130, bottom=130, left=150, right=150)
        fill_formatted_cell(c0, response_txt, font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold_first_col=False)

    # --- BLOQUE 1: CAMBIOS ECONÓMICOS ---
    format_t2_section_banner(0, "CAMBIOS ECONÓMICOS")
    format_t2_subheaders(1)
    format_t2_content_pair(
        2,
        "• Sin inversión inicial en hardware (CAPEX cero): No hace falta comprar servidores físicos, discos duros externos ni habilitar una sala refrigerada en la academia.\n"
        "• Rentabilidad desde el minuto uno: Se paga únicamente por lo que se utiliza (pago por uso) con precios muy competitivos gracias a la economía de escala del proveedor.\n"
        "• Escalabilidad inmediata (upgrade / downgrade): Si en época de PAU o exámenes de Cambridge entran 50 alumnos más, se amplía el servicio con un clic y se reduce en verano sin equipos obsoletos.\n"
        "• Ahorro drástico en papelería, fotocopias, tóner, carpetas físicas y factura eléctrica 24/7.\n"
        "• Seguridad y mantenimiento incluidos: El proveedor asume los costes de ciberseguridad y evita multas de la AEPD (hasta 60.000 € por pérdida de datos como en el caso de CC.OO.).",
        "• Coste de suscripción periódico (OPEX): En planes de pago avanzados existe una cuota mensual o anual recurrente por usuario o por ampliar almacenamiento extra.\n"
        "• Necesidad de una buena conexión a Internet: Puede requerir contratar una línea de fibra óptica simétrica más rápida y estable en el local de la academia.\n"
        "• Percepción de gasto continuo: Samuel puede pensar que pagar una cuota o depender de un proveedor externo a largo plazo saldrá más caro que seguir usando los ordenadores actuales sin pagar licencias cloud."
    )
    format_t2_response_row(
        3,
        "Respuesta a los inconvenientes (Argumentación de Rebeca para Samuel):\n"
        "• Licencias educativas gratuitas o de coste mínimo: Al ser EduPlus Academy un centro de enseñanza, tanto Google (Google Workspace for Education Fundamentals) como Microsoft (Microsoft 365 Education A1) ofrecen sus planes base a coste 0 € para docentes y alumnos. Incluso si contratamos funciones premium o más espacio, apenas supone entre 3 € y 5 € al mes por cada uno de nuestros 6 profesores (menos de 30 €/mes en total).\n"
        "• El ahorro supera por diez a la cuota: Solo en folios, carpetas archivadoras, tóner de impresora y discos duros que se rompen gastamos hoy más de 150 € al mes. Además, como explica el Tema 4, comprar un servidor local propio requeriría miles de euros de golpe, meses de aprovisionamiento y expertos para mantenerlo.\n"
        "• Blindaje económico frente a desastres y multas: Una sola pérdida de datos de nuestros 120 alumnos menores o una sanción de la AEPD nos costaría hasta 60.000 € y nuestra reputación; la nube nos incluye seguridad profesional sin inversión adicional."
    )

    # --- BLOQUE 2: CAMBIOS EN LOS EMPLEADOS ---
    format_t2_section_banner(4, "CAMBIOS EN LOS EMPLEADOS")
    format_t2_subheaders(5)
    format_t2_content_pair(
        6,
        "• Trabajo colaborativo en tiempo real: Los 6 profesores pueden elaborar y revisar juntos simulacros de PAU o Cambridge sobre el mismo documento simultáneamente (como en Microsoft Teams o Google Docs).\n"
        "• Fin de la pérdida de trabajo por despistes o cortes de luz: El autoguardado cada 5 segundos (caso de Sonia frente a Marcos en el Tema 4) impide perder horas de redacción de informes trimestrales.\n"
        "• Facilitación del teletrabajo y deslocalización: Los docentes pueden corregir tareas, preparar clases o dar tutorías online desde su casa con baja latencia y acceso instantáneo.\n"
        "• Orden y desconexión digital: Se acaba el caos de recibir tareas de 120 alumnos por WhatsApp personal a cualquier hora; todo queda ordenado en el aula virtual.\n"
        "• Ahorro de tiempo administrativo: Evaluaciones tipo test autocorregibles y boletines trimestrales generados en minutos.",
        "• Curva de aprendizaje y tiempo de adaptación: Temor de Samuel a que los 6 docentes tarden mucho tiempo en aprender a usar las nuevas herramientas.\n"
        "• Esfuerzo inicial de migración: Necesidad de pasar los materiales actuales en papel y las carpetas dispersas en varios ordenadores a la estructura en la nube.\n"
        "• Resistencia psicológica al cambio: Hábitos muy arraigados de trabajar en papel o guardar en el escritorio local.\n"
        "• Dependencia de la red e incidencias del proveedor: Miedo a que si se cae Internet o falla el proveedor en la nube (como el incidente de DNS de AWS del 20 de octubre de 2025 citado en el Tema 4), los profesores se queden paralizados sin poder dar clase."
    )
    format_t2_response_row(
        7,
        "Respuesta a los inconvenientes (Argumentación de Rebeca para Samuel):\n"
        "• Cero complejidad técnica gracias al modelo SaaS: No vamos a instalar programas complicados de informáticos; usaremos aplicaciones web (como Google Drive, Docs, Classroom o Teams) que los 6 profesores ya saben usar porque son idénticas al correo electrónico o al navegador que usan a diario. Según el Tema 4, el 80 % de las empresas tienen una visión muy positiva en los primeros 6 meses.\n"
        "• Migración progresiva y acompañada: No hay que escanear ni subir todo el primer día. Yo misma (Rebeca) organizaré las carpetas base en una tarde e impartiré dos sesiones prácticas de 45 minutos a nuestros compañeros. Subiremos los temas semana a semana conforme los vayamos dando en clase.\n"
        "• Modo sin conexión (Offline) y redundancia ante fallos: Si un día falla Internet en la academia o hay una incidencia puntual en el proveedor cloud, tanto Google Drive/Docs como OneDrive/Office cuentan con 'Modo sin conexión' que permite seguir abriendo y editando los archivos en el aula y los sincroniza automáticamente al volver la red, además de mantener copia de seguridad de los materiales clave."
    )

    # --- BLOQUE 3: CAMBIOS MEDIOAMBIENTALES ---
    format_t2_section_banner(8, "CAMBIOS MEDIOAMBIENTALES")
    format_t2_subheaders(9)
    format_t2_content_pair(
        10,
        "• Academia 'Papel Cero' (Zero Paper): Eliminación de miles de folios impresos cada trimestre en fichas de ejercicios, simulacros de examen de PAU/Cambridge, circulares a padres y los 120 informes trimestrales en carpetas de plástico o cartón.\n"
        "• Reducción del consumo eléctrico en el centro: Como indica el Tema 4, no es necesario disponer de servidores propios consumiendo electricidad y aire acondicionado las 24 horas del día, los 365 días del año en una oficina sobredimensionada.\n"
        "• Disminución de emisiones de CO2 por desplazamientos: Las tutorías con familias por videollamada y las clases online evitan cientos de viajes en coche a la academia.\n"
        "• Alargamiento de la vida útil de los ordenadores actuales: Al ejecutarse el procesamiento y almacenamiento en la nube, nuestros ordenadores actuales no se quedan cortos de memoria ni necesitan renovarse, evitando generar basura electrónica (e-waste).",
        "• Consumo energético e hídrico de los grandes centros de datos (Data Centers): Los servidores remotos en la nube consumen electricidad de forma continua y requieren sistemas de refrigeración a gran escala.\n"
        "• Incremento del tráfico de red y ancho de banda: Como señala el apartado 4 del Tema 4, enviar y recibir vídeos, PDFs y videollamadas continuamente a través de Internet consume recursos energéticos en las redes de telecomunicaciones.\n"
        "• Acumulación de 'basura digital' (datos oscuros): Guardar copias innecesarias o vídeos duplicados en la nube sin borrarlos ocupa almacenamiento en servidores físicos remotos."
    )
    format_t2_response_row(
        11,
        "Respuesta a los inconvenientes (Argumentación de Rebeca para Samuel):\n"
        "• Eficiencia energética muy superior por economía de escala: Los grandes proveedores que analizamos (Google Cloud, Microsoft Azure, IBM Cloud) operan centros de datos hiperoptimizados que se alimentan con energía 100 % renovable y compromisos de huella de carbono neutra o negativa, siendo infinitamente más limpios y eficientes que tener servidores locales encendidos en miles de pequeñas empresas.\n"
        "• Optimización del ancho de banda y higiene digital: Aplicaremos buenas prácticas en EduPlus Academy (comprimir vídeos educativos, compartir enlaces en lugar de enviar archivos adjuntos pesados cien veces por correo o WhatsApp, y limpiar archivos temporales cada fin de curso), reduciendo el tráfico de red.\n"
        "• Balance ambiental claramente positivo para la academia: Evitar la tala de árboles asociada a miles de fotocopias anuales, eliminar cartuchos de tóner químicos y no tener que tirar a la basura nuestros ordenadores actuales convierte a la nube en la opción más ecológica y sostenible para EduPlus Academy."
    )

    p_sp_t2 = doc.add_paragraph()
    p_sp_t2.paragraph_format.space_before = Pt(4)
    p_sp_t2.paragraph_format.space_after = Pt(6)

    add_h2("3.3. Desarrollo Razonado de Respuestas a las Objeciones de Samuel (Seguridad, Caídas y Curva)")
    add_p(
        "Más allá del cuadro sintético anterior, como Rebeca quiero dejar por escrito tres reflexiones directas para "
        "tranquilizar a Samuel respecto a sus miedos principales:"
    )
    add_bullet(
        "Sobre el miedo al tiempo que nos llevará formarnos:",
        "Samuel, recuerda el ejemplo de Sonia y Marcos que vemos en el Tema 4. Marcos creía que trabajar en su ordenador de "
        "toda la vida era más rápido, hasta que un corte de luz le hizo perder todo su trabajo. Sonia, usando documentos en la "
        "nube que se guardan solos cada 5 segundos, no tuvo que aprender informática avanzada: escribe exactamente igual que en "
        "Word, pero nunca pierde nada y puede compartirlo con un clic. En menos de una semana nuestros 6 profesores habrán "
        "recuperado con creces el tiempo invertido gracias a no tener que buscar papeles ni contestar WhatsApps individuales."
    )
    add_bullet(
        "Sobre el miedo a qué pasa si la nube falla:",
        "Es cierto que ningún sistema es infalible al 100 %, como demostró la interrupción temporal de Amazon Web Services (AWS) "
        "el 20 de octubre de 2025 por un fallo de DNS en la región US East One (citada en la página 10 del Tema 4). Sin embargo, "
        "la lección de ese caso práctico es la planificación y la redundancia: en EduPlus Academy activaremos la sincronización "
        "local de respaldo en el ordenador del aula y programaremos una copia de seguridad automática en un segundo proveedor, "
        "garantizando que las clases jamás se detengan."
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 4: TAREA 3 - ESTUDIO DE PROVEEDORES
    # =========================================================================
    add_h1("4. Tarea 3: Estudio Comparativo de Proveedores de Servicios en la Nube")

    add_h2("4.1. Análisis de los Tres Proveedores Líderes: Microsoft Azure, Google Cloud e IBM Cloud")
    add_p(
        "Para seleccionar la plataforma tecnológica de EduPlus Academy, se han analizado los tres grandes proveedores de "
        "servicios en la nube indicados en la Tarea 3: Microsoft Azure, Google Cloud e IBM Cloud. Aunque a menudo asociamos "
        "estos nombres únicamente a infraestructura para grandes corporaciones, todos ellos articulan un ecosistema completo "
        "que abarca desde soluciones SaaS listas para centros educativos hasta servicios PaaS, IaaS, contenedores, copia de "
        "seguridad e Inteligencia Artificial:"
    )

    add_bullet(
        "1. Microsoft Azure (y el ecosistema SaaS Microsoft 365 Education):",
        "Como destaca el Tema 4 (pág. 13), Microsoft Azure es el referente mundial en entornos de nube híbrida, permitiendo "
        "combinar servicios públicos con un control de seguridad privado empresarial. Para EduPlus Academy, su gran fortaleza "
        "reside en su integración nativa con Microsoft 365 Education (el mismo entorno de Microsoft Teams que, como menciona "
        "la página 6 del Tema 4, utilizamos los docentes en la Comunidad Valenciana para guardar documentos en la nube y "
        "trabajar de forma colaborativa), sumado a servicios de Azure como Azure Backup, Azure Blob Storage y Entra ID."
    )
    add_bullet(
        "2. Google Cloud (y el ecosistema SaaS Google Workspace for Education):",
        "Como se estudia en las páginas 7 y 15 del Tema 4, Google Cloud Platform (GCP) ofrece más de 100 productos en la nube "
        "(Compute Services, Storage Services, Networking, Big Data, Cloud AI, IoT, Security & Identity Management) y fue pionero "
        "en 2014 en el lanzamiento de Kubernetes (Google Kubernetes Engine - GKE) para la gestión de contenedores a escala. "
        "En el ámbito educativo, su capa SaaS (Google Workspace for Education con Classroom, Drive, Docs, Meet, Calendar y Forms) "
        "es líder absoluto en academias y colegios por su sencillez, rapidez y colaboración en tiempo real."
    )
    add_bullet(
        "3. IBM Cloud (Nube Privada/Híbrida, Seguridad Criptográfica e IA Watsonx):",
        "El Tema 4 (pág. 13) señala a IBM Cloud Private como el ejemplo canónico de nube privada e híbrida orientada a "
        "organizaciones que exigen el máximo rigor en control y privacidad de datos. Además de su liderazgo en contenedores "
        "empresariales mediante Red Hat OpenShift, IBM Cloud aporta a una academia como EduPlus tres servicios de gran valor: "
        "almacenamiento inmutable de copias de seguridad (IBM Cloud Object Storage) para blindar expedientes académicos frente "
        "a ransomware o pérdidas, servidores virtuales/PaaS para alojar la web corporativa, y los servicios de Inteligencia "
        "Artificial de IBM Watsonx (como Watson Assistant) para implantar un asistente virtual de atención a familias 24/7."
    )

    add_h2("4.2. Tabla Oficial de la Tarea 3: Resumen de Servicios Relevantes para EduPlus Academy")
    add_p(
        "A continuación se presenta la tabla oficial requerida por la Tarea 3, resumiendo de forma estructurada los servicios "
        "relevantes de cada proveedor aplicables a las necesidades reales de EduPlus Academy:"
    )

    t3_headers = ["EMPRESA", "SERVICIOS RELEVANTES PARA EDUPLUS ACADEMY"]
    t3_rows = [
        [
            "Microsoft Azure\n(& Microsoft 365 Education)",
            "• Plataforma de Clases Online y Colaboración (SaaS - Microsoft Teams para Educación): Creación de equipos por etapa (Primaria, ESO, Bachillerato, PAU y Cambridge), videollamadas grabables, pizarra digital Whiteboard, entrega de tareas y boletines de notas.\n"
            "• Almacenamiento y Ofimática en la Nube (SaaS - OneDrive, SharePoint y Office Online): 1 TB de almacenamiento por docente, carpetas departamentales en SharePoint y edición simultánea en Word, Excel, PowerPoint y OneNote Class Notebook con autoguardado continuo.\n"
            "• Gestión de Horarios, Tutorías y Evaluaciones (SaaS - Microsoft Bookings, Outlook Calendar y Forms): Portal web donde las familias reservan tutorías automáticamente según disponibilidad de los 6 profesores, calendarios de aulas y exámenes tipo test autocorregibles.\n"
            "• Copias de Seguridad y Almacenamiento Seguro (IaaS/PaaS - Azure Backup y Azure Blob Storage): Respaldo automatizado e inmutable de los expedientes e informes trimestrales de los 120 alumnos en centros de datos europeos (cumplimiento estricto RGPD/AEPD).\n"
            "• Identidad, Nube Híbrida y Servidores (Microsoft Entra ID, Azure Virtual Machines y Azure App Service): Control de acceso seguro con doble factor (MFA) para profesores y alojamiento escalable de la web de la academia."
        ],
        [
            "Google Cloud\n(& Google Workspace for Education)",
            "• Aula Virtual y Gestión Académica (SaaS - Google Classroom): Plataforma centralizada muy intuitiva para publicar apuntes (PDF, vídeos), mandar deberes, calificar simulacros de examen y mantener informados a alumnos y padres con resúmenes automáticos por email.\n"
            "• Almacenamiento y Edición Colaborativa (SaaS - Google Drive, Docs, Sheets y Slides): Unidades compartidas para los 6 docentes y creación colaborativa de materiales didácticos con guardado automático cada 5 segundos (ejemplo de Sonia en el Tema 4) y modo sin conexión.\n"
            "• Videoconferencias, Horarios y Test (SaaS - Google Meet, Google Calendar y Google Forms): Clases particulares online de baja latencia, agenda compartida de aulas/tutorías y cuestionarios interactivos para preparación de Cambridge y PAU.\n"
            "• Infraestructura, Backups y Contenedores (IaaS/PaaS - Google Cloud Storage, Compute Engine, App Engine y Kubernetes Engine - GKE): Almacenamiento georredundante para copias de seguridad históricas del centro y plataforma de contenedores para la web de la academia.\n"
            "• Analítica e Inteligencia Artificial Educativa (Cloud AI / Vertex AI / Gemini Education y BigQuery): Asistencia inteligente para que los docentes generen ejercicios adaptados por nivel y análisis de evolución de notas."
        ],
        [
            "IBM Cloud",
            "• Copias de Seguridad de Alta Seguridad y Archivo Legal (IaaS - IBM Cloud Object Storage): Almacenamiento en la nube con cifrado de grado bancario para conservar durante años los expedientes académicos, contratos y datos sensibles de menores evitando multas de la AEPD.\n"
            "• Asistente Virtual de Atención a Familias e IA Pedagógica (SaaS/PaaS - IBM watsonx Assistant & Discovery): Chatbot inteligente integrado en la web de EduPlus Academy que responde 24/7 a las dudas de padres sobre horarios, precios, grupos de PAU/Cambridge y reserva de citas.\n"
            "• Nube Privada e Híbrida para Datos Críticos (IBM Cloud Private & Red Hat OpenShift): Arquitectura de alta privacidad (destacada en el Tema 4) y gestión avanzada de aplicaciones en contenedores sin dependencia de un único proveedor.\n"
            "• Alojamiento de Aplicaciones y Portal Web (IaaS/PaaS - IBM Cloud Virtual Servers y Code Engine): Infraestructura escalable bajo demanda para alojar el portal web de la academia y bases de datos (IBM Cloud Databases) con protección contra ciberataques."
        ]
    ]
    build_custom_table(t3_headers, t3_rows, [1.8, 4.7], header_hex=HEX_GREEN, alt_hex=HEX_LIGHT_GREEN, border_hex="A5C690")

    add_h2("4.3. Toma de Decisiones: Selección de la Arquitectura Ganadora y Estrategia de Redundancia")
    add_p(
        "Tras evaluar los tres proveedores desde la perspectiva de Rebeca y teniendo muy presentes las inquietudes de Samuel "
        "(sencillez de uso para los 6 profesores, rapidez de puesta en marcha y coste mínimo), tomamos la siguiente decisión "
        "estratégica para EduPlus Academy:"
    )

    add_bullet(
        "Plataforma Principal de Trabajo Diario (Google Workspace for Education + Google Cloud):",
        "Se selecciona el ecosistema de Google (Google Classroom, Google Drive, Google Docs/Sheets/Slides, Google Meet, Google "
        "Calendar y Google Forms) como plataforma SaaS principal para los 6 docentes y los más de 120 alumnos. Su interfaz es "
        "la más sencilla e intuitiva del mercado (reduciendo a casi cero el tiempo de formación que preocupa a Samuel), permite "
        "solicitar la licencia educativa gratuita o de muy bajo coste, cuenta con modo sin conexión y resuelve las 7 funciones "
        "de la Tarea 1 en un entorno único."
    )
    add_bullet(
        "Alternativa o Complemento Ofimático (Microsoft 365 Education / Teams):",
        "Dado que varios docentes e institutos de la Comunidad Valenciana utilizan Microsoft Teams y formatos de Word/Excel, "
        "Google Drive permite editar archivos de Office de forma nativa, o bien se puede activar el plan gratuito Microsoft 365 "
        "Education A1 en paralelo para aquellos profesores de Bachillerato/PAU que prefieran usar OneNote o Teams."
    )
    add_bullet(
        "Redundancia Multi-Proveedor contra Caídas de la Nube (Backup Cruzado en Azure / IBM Cloud):",
        "Aplicando la enseñanza del caso práctico 'Cuando la nube falla' del Tema 4 (pág. 10, sobre la caída de AWS el 20 de "
        "octubre de 2025), donde se explica que las empresas previsoras contratan copias de seguridad en un segundo proveedor "
        "para no paralizarse ni perder datos, EduPlus Academy realizará una copia de seguridad automática semanal cifrada de "
        "su unidad de Google Drive hacia un contenedor de almacenamiento económico en Microsoft Azure Blob Storage (o IBM Cloud "
        "Object Storage) con un coste inferior a 3 € al mes. Así, Samuel tendrá garantía absoluta del 100 % de disponibilidad."
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 5: PLAN DE IMPLEMENTACIÓN, HOJA DE RUTA Y PRESUPUESTO
    # =========================================================================
    add_h1("5. Plan de Implementación, Hoja de Ruta y Presupuesto Estimado")

    add_h2("5.1. Fases de Implantación Gradual sin Interrumpir las Clases (Plan de 4 Semanas)")
    add_p(
        "Para demostrar a Samuel que la transición a la nube no detendrá el ritmo de la academia ni agobiará al profesorado, "
        "Rebeca propone un plan de implementación gradual dividido en 4 semanas:"
    )

    add_bullet(
        "Semana 1 — Alta del Dominio, Cuentas y Estructura de Carpetas en la Nube:",
        "Registro del dominio educativo de la academia y alta en Google Workspace for Education (y respaldo en Azure). Creación "
        "de las cuentas corporativas para los 6 docentes y configuración de las Unidades Compartidas en Drive estructuradas "
        "por etapas: Primaria, ESO, Bachillerato, PAU, Cambridge, Técnicas de Estudio e Informes Trimestrales. Configuración de "
        "permisos y seguridad RGPD (verificación en dos pasos)."
    )
    add_bullet(
        "Semana 2 — Píldora Formativa Docente (90 min) y Digitalización de Horarios/Tutorías:",
        "Rebeca imparte dos talleres prácticos de 45 minutos en horario de reunión de equipo para enseñar a los 5 compañeros a "
        "subir archivos a Drive, editar informes colaborativos en Google Docs y gestionar el calendario compartido de aulas y "
        "reservas de tutorías. Se migran únicamente los materiales del trimestre en curso (sin necesidad de escanear archivos "
        "antiguos de años pasados de golpe)."
    )
    add_bullet(
        "Semana 3 — Apertura de Aulas Virtuales (Google Classroom / Meet) y Plantillas de Evaluación:",
        "Creación de las clases virtuales para cada grupo reducido y taller. Configuración de las plantillas digitales de los "
        "boletines trimestrales de notas y hojas de asistencia en Google Sheets. Prueba piloto con los grupos de Bachillerato "
        "y preparación de PAU/Cambridge."
    )
    add_bullet(
        "Semana 4 — Lanzamiento a Familias, Alumnos y Activación de Backups Automáticos:",
        "Envío de una circular de bienvenida a las familias de los 120 alumnos con sus claves de acceso al aula virtual y al "
        "sistema de reserva de tutorías, sustituyendo oficialmente el envío de tareas por WhatsApp. Activación de la copia de "
        "seguridad automática semanal cruzada en la nube."
    )

    add_h2("5.2. Presupuesto Económico y Retorno de la Inversión (ROI) para EduPlus Academy")
    add_p(
        "Uno de los argumentos más potentes del Tema 4 (apartado 3.1: ¿Cuánto cuesta implantar el cloud computing?) es que la "
        "nube elimina el aprovisionamiento de meses y los gastos inútiles en servidores físicos, permitiendo pagar solo por "
        "los recursos utilizados. A continuación se detalla el presupuesto real para EduPlus Academy:"
    )

    t_bud_headers = ["PARTIDA / SERVICIO CLOUD", "MODALIDAD ELEGIDA", "COSTE ESTIMADO", "AHORRO Y BENEFICIO DIRECTO"]
    t_bud_rows = [
        [
            "Suite Educativa Principal (SaaS)\nGoogle Workspace for Education",
            "Edición Education Fundamentals (o Standard para 6 docentes + 120 alumnos)",
            "0 € / mes (Plan Educativo Base)\no 18 € / mes (Plan Ampliado)",
            "Incluye Classroom, Drive, Docs, Meet, Calendar y Forms sin comprar licencias locales de Office ni servidores."
        ],
        [
            "Dominio Web y Correo Corporativo\n(@eduplusacademy.es)",
            "Registro anual de dominio y configuración DNS segura",
            "12 € / año\n(1 € / mes)",
            "Imagen profesional ante las familias y separación total del correo/WhatsApp personal de los profesores."
        ],
        [
            "Copia de Seguridad Redundante\n(Azure Blob Storage / IBM Cloud)",
            "Almacenamiento frío (Cool/Archive) para 200 GB de expedientes e informes",
            "3 € / mes\n(36 € / año)",
            "Blindaje total ante caídas de un proveedor (caso AWS Tema 4), cortes de luz o ransomware, cumpliendo con la AEPD."
        ],
        [
            "Formación y Puesta en Marcha\n(Liderada internamente por Rebeca)",
            "2 talleres internos de 45 min + guía rápida en PDF en la nube",
            "0 €\n(Gestión interna)",
            "Adopción rápida en 4 semanas sin contratar consultoras externas caras."
        ],
        [
            "BALANCE TOTAL Y RETORNO (ROI)",
            "Coste total mensual en la nube:\n4 € a 22 € / mes",
            "Ahorro en papel, tinta y tiempo:\n> 180 € / mes ahorrados",
            "Rentable desde el minuto uno (ahorro neto superior a 1.800 € al año y eliminación del riesgo de multas de 60.000 €)."
        ]
    ]
    build_custom_table(t_bud_headers, t_bud_rows, [1.8, 1.6, 1.4, 1.7])

    # =========================================================================
    # SECCIÓN 6: VALORACIÓN FINAL Y CONCLUSIONES DEL PROYECTO
    # =========================================================================
    add_h1("6. Valoración Final y Conclusiones del Proyecto")

    add_p(
        "Tras completar el análisis técnico, económico, laboral, medioambiental y de proveedores para EduPlus Academy, "
        "y asumiendo el papel de Rebeca como cofundadora del centro junto a Samuel, se extraen las siguientes conclusiones "
        "y valoración final del proyecto:"
    )

    add_bullet(
        "1. El modelo tradicional local ya no es viable ni seguro para una academia de 120 alumnos:",
        "Seguir manejando los informes trimestrales en carpetas físicas, los exámenes dispersos en ordenadores locales y las "
        "tareas por WhatsApp no solo lastra la productividad de los 6 docentes, sino que expone a EduPlus Academy a una pérdida "
        "catastrófica de datos por error humano, fallo mecánico o corte eléctrico (como ejemplifica el caso de Marcos en el "
        "Tema 4) y a severas sanciones económicas de la AEPD por desprotección de datos personales de menores."
    )
    add_bullet(
        "2. El modelo SaaS en nube pública/híbrida es la respuesta exacta a las preocupaciones de Samuel:",
        "Al optar por soluciones Software as a Service (Google Workspace for Education complementado con respaldo en Microsoft "
        "Azure / IBM Cloud), Samuel y los profesores no tienen que administrar servidores ni aprender informática compleja. "
        "Todo el mantenimiento, las actualizaciones y la ciberseguridad corren a cargo del proveedor, permitiendo al equipo "
        "centrarse al 100 % en su vocación: enseñar y acompañar a sus alumnos de Primaria, ESO, Bachillerato, PAU y Cambridge."
    )
    add_bullet(
        "3. Rentabilidad económica inmediata, flexibilidad laboral y sostenibilidad ambiental:",
        "La implantación de la nube en EduPlus Academy no requiere inversión inicial en hardware (CAPEX cero), alarga la vida "
        "útil de los ordenadores actuales del centro al delegar el procesamiento en servidores remotos, reduce drásticamente "
        "el gasto en papel y fotocopias, y dota a la academia de una plataforma unificada de clases online y trabajo colaborativo "
        "que garantiza la continuidad del negocio ante cualquier contingencia futura."
    )
    add_bullet(
        "4. Valoración personal desde el rol de Rebeca:",
        "Como socia de Samuel desde 2018, este plan demuestra que modernizar EduPlus Academy mediante cloud computing no es un "
        "salto al vacío ni una carga de trabajo adicional, sino la mejor inversión de futuro para proteger lo que hemos construido "
        "juntos, mejorar la conciliación de nuestros 6 profesores y ofrecer a nuestros más de 120 estudiantes y a sus familias "
        "una experiencia educativa de excelencia, moderna y segura."
    )

    # =========================================================================
    # SECCIÓN 7: DEFENSA DEL PROYECTO Y ENLACE A LA PRESENTACIÓN
    # =========================================================================
    add_h1("7. Defensa del Proyecto: Presentación Ejecutiva y Enlace de Acceso")

    add_p(
        "En cumplimiento del último requisito del Informe Final, se ha elaborado una presentación ejecutiva en formato "
        "panorámico (16:9) diseñada para defender esta propuesta ante Samuel y el claustro de profesores de EduPlus Academy. "
        "La presentación sintetiza de forma visual el diagnóstico inicial, las 7 funciones de la nube y la elección del modelo "
        "SaaS (Tarea 1), la tabla comparativa de ventajas, inconvenientes y respuestas razonadas en los ámbitos económico, "
        "laboral y medioambiental (Tarea 2), el estudio de proveedores Microsoft Azure, Google Cloud e IBM Cloud (Tarea 3) "
        "y la hoja de ruta de implantación."
    )

    # Cuadro con el enlace a la presentación (requisito explícito: "Añade enlace a la presentación al final del informe")
    tbl_link = doc.add_table(rows=1, cols=1)
    tbl_link.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_lnk = tbl_link.cell(0, 0)
    set_cell_background(c_lnk, HEX_LIGHT_BLUE)
    set_cell_margins(c_lnk, top=160, bottom=160, left=200, right=200)
    set_table_borders(tbl_link, color=HEX_PRIMARY, sz="8")

    pl1 = c_lnk.paragraphs[0]
    pl1.paragraph_format.line_spacing = 1.5
    pl1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    rl_title = pl1.add_run("📊 ENLACE A LA PRESENTACIÓN DE DEFENSA DEL PROYECTO (EDUPLUS ACADEMY)\n")
    rl_title.font.name = "Calibri"
    rl_title.font.size = Pt(11)
    rl_title.font.bold = True
    rl_title.font.color.rgb = C_PRIMARY

    link_items = [
        ("Archivo de la Presentación:", "Presentacion_Cloud_EduPlus_Kevin.pptx"),
        ("Enlace en Repositorio GitHub:", "https://github.com/kevin/Curso-Dam2/blob/main/digitalizacion-productivo/Proyecto_Cloud_EduPlus/Presentacion_Cloud_EduPlus_Kevin.pptx"),
        ("Enlace de Entrega en Aules / Cloud:", "https://aules.edu.gva.es/fp/mod/assign/view.php?name=Presentacion_Cloud_EduPlus_Kevin.pptx"),
        ("Autor y Rol de Defensa:", "Kevin (asumiendo el papel de Rebeca, cofundadora de EduPlus Academy) · 2º DAM")
    ]
    for label, val in link_items:
        pl = c_lnk.add_paragraph()
        pl.paragraph_format.line_spacing = 1.5
        pl.paragraph_format.space_after = Pt(2)
        pl.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_b = pl.add_run(f"• {label} ")
        r_b.font.name = "Calibri"
        r_b.font.size = Pt(11)
        r_b.font.bold = True
        r_b.font.color.rgb = C_PRIMARY

        r_v = pl.add_run(val)
        r_v.font.name = "Calibri"
        r_v.font.size = Pt(11)
        if val.startswith("http"):
            r_v.font.underline = True
            r_v.font.color.rgb = C_ACCENT
        else:
            r_v.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # Guardado del documento en la carpeta del proyecto y copia en digitalizacion-productivo
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "Propuesta_Cloud_EduPlus_Kevin.docx")
    doc.save(output_path)
    print(f"Documento Word creado con éxito en: {output_path}")

    parent_dir = os.path.dirname(output_dir)
    parent_copy = os.path.join(parent_dir, "Propuesta_Cloud_EduPlus_Kevin.docx")
    shutil.copyfile(output_path, parent_copy)
    print(f"Copia guardada en: {parent_copy}")

    return output_path

if __name__ == "__main__":
    create_full_report()
