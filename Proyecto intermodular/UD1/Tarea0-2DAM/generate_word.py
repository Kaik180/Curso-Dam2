import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

def create_document():
    doc = docx.Document()

    # Configure margins (2.5 cm approx)
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)
        section.different_first_page_header_footer = True

        # Header for subsequent pages
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("Proyecto Intermodular - 2º DAM  |  Tarea 0: Memorix")
        r_hdr.font.name = "Calibri"
        r_hdr.font.size = Pt(8.5)
        r_hdr.font.color.rgb = RGBColor(100, 116, 139)

        # Footer for subsequent pages
        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ftr_l = p_ftr.add_run("Memorix  •  Propuesta Inicial\t\tPágina ")
        r_ftr_l.font.name = "Calibri"
        r_ftr_l.font.size = Pt(9)
        r_ftr_l.font.color.rgb = RGBColor(100, 116, 139)
        
        # Add dynamic page number field in footer
        fld_run = p_ftr.add_run()
        fld_run.font.name = "Calibri"
        fld_run.font.size = Pt(9)
        fld_run.font.color.rgb = RGBColor(100, 116, 139)
        fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
        instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
        fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
        fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
        fld_run._r.append(fldChar1)
        fld_run._r.append(instrText)
        fld_run._r.append(fldChar2)
        fld_run._r.append(fldChar3)

    # Style defaults
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Calibri'
    font_normal.size = Pt(12)
    font_normal.color.rgb = RGBColor(30, 41, 59)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(4)

    # Bookmarks
    bookmark_id = 0
    def add_bookmark(paragraph, name):
        nonlocal bookmark_id
        bookmark_id += 1
        b_start = parse_xml(f'<w:bookmarkStart {nsdecls("w")} w:id="{bookmark_id}" w:name="{name}"/>')
        b_end = parse_xml(f'<w:bookmarkEnd {nsdecls("w")} w:id="{bookmark_id}"/>')
        paragraph._p.insert(0, b_start)
        paragraph._p.append(b_end)

    # External hyperlinks
    def add_external_link(paragraph, url, text):
        part = paragraph.part
        r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
        hyperlink = parse_xml(f'<w:hyperlink {nsdecls("w")} {nsdecls("r")} r:id="{r_id}" w:history="1"/>')
        new_run = parse_xml(
            f'<w:r {nsdecls("w")}><w:rPr>'
            f'<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
            f'<w:color w:val="00A896"/>'
            f'<w:u w:val="single"/>'
            f'</w:rPr><w:t>{text}</w:t></w:r>'
        )
        hyperlink.append(new_run)
        paragraph._p.append(hyperlink)

    # TOC links
    def add_toc_item(paragraph, title, anchor_name, page_num_str):
        hyperlink = parse_xml(f'<w:hyperlink {nsdecls("w")} w:anchor="{anchor_name}" w:history="1"/>')
        run_title = parse_xml(
            f'<w:r {nsdecls("w")}><w:rPr>'
            f'<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
            f'<w:color w:val="050C26"/>'
            f'<w:u w:val="single"/>'
            f'</w:rPr><w:t>{title}</w:t></w:r>'
        )
        hyperlink.append(run_title)
        paragraph._p.append(hyperlink)

        r_dots = paragraph.add_run(f"  {'.' * 46}  ")
        r_dots.font.color.rgb = RGBColor(160, 174, 192)
        r_dots.font.name = "Calibri"
        r_dots.font.size = Pt(11)

        r_p = paragraph.add_run(page_num_str)
        r_p.font.name = "Calibri"
        r_p.font.size = Pt(11)
        r_p.font.bold = True
        r_p.font.color.rgb = RGBColor(5, 12, 38)

    # Section headings (Calibri 14pt Bold)
    def add_section_heading(title_text, anchor_name=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        
        run = p.add_run(title_text)
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(5, 12, 38)  # Deep Navy #050C26
        
        if anchor_name:
            add_bookmark(p, anchor_name)
        return p

    def add_body_p(text, bold_prefix=None, space_after=3):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(space_after)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.name = 'Calibri'
            r_b.font.size = Pt(12)
            r_b.font.bold = True
            r_b.font.color.rgb = RGBColor(0, 168, 150)  # Turquoise #00A896
        r_t = p.add_run(text)
        r_t.font.name = 'Calibri'
        r_t.font.size = Pt(12)
        r_t.font.color.rgb = RGBColor(30, 41, 59)
        return p

    # =========================================================================
    # 01 PORTADA CON LOGO Y TEMÁTICA MEMORIX
    # =========================================================================
    curr_dir = os.path.dirname(__file__)
    logo_light = os.path.join(curr_dir, "logo_memorix_light.png")

    p_cov_sp1 = doc.add_paragraph()
    p_cov_sp1.paragraph_format.space_before = Pt(20)

    # Logo oficial Memorix en portada
    if os.path.exists(logo_light):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(8)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_light, width=Inches(1.8))

    # Badge superior
    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_after = Pt(6)
    r_badge = p_badge.add_run("PROYECTO INTERMODULAR • 2º DAM")
    r_badge.font.name = "Calibri"
    r_badge.font.size = Pt(11)
    r_badge.font.bold = True
    r_badge.font.color.rgb = RGBColor(0, 168, 150)

    # Título principal
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.line_spacing = 1.1
    r_title = p_title.add_run("Memorix")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(32)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(5, 12, 38)

    # Subtítulo de la propuesta
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    p_sub.paragraph_format.line_spacing = 1.2
    r_sub = p_sub.add_run("Asistente Móvil Inteligente de Tratamientos Farmacológicos y Rehabilitación Muscular Asistida")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0, 56, 255)

    # Divisor horizontal
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_after = Pt(18)
    r_line = p_line.add_run("—" * 32)
    r_line.font.color.rgb = RGBColor(203, 213, 225)

    # Cuadro informativo central
    p_tag = doc.add_paragraph()
    p_tag.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tag.paragraph_format.space_after = Pt(60)
    p_tag.paragraph_format.line_spacing = 1.3
    r_tag = p_tag.add_run("Tarea 0: Una Solución Digital para un Problema Real\nPropuesta Inicial y Definición del Proyecto Intermodular")
    r_tag.font.name = "Calibri"
    r_tag.font.size = Pt(11)
    r_tag.font.color.rgb = RGBColor(100, 116, 139)

    # Datos del alumno y entrega
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.line_spacing = 1.3
    p_meta.paragraph_format.space_after = Pt(0)
    
    r_autor = p_meta.add_run("Alumno: ")
    r_autor.font.bold = True
    r_autor.font.size = Pt(12)
    r_autor_name = p_meta.add_run("Kevin [Apellidos]\n")
    r_autor_name.font.size = Pt(12)
    
    r_curso = p_meta.add_run("Curso: ")
    r_curso.font.bold = True
    r_curso.font.size = Pt(12)
    r_curso_val = p_meta.add_run("2º Desarrollo de Aplicaciones Multiplataforma (DAM)\n")
    r_curso_val.font.size = Pt(12)

    r_modulo = p_meta.add_run("Módulo: ")
    r_modulo.font.bold = True
    r_modulo.font.size = Pt(12)
    r_modulo_val = p_meta.add_run("Proyecto Intermodular | Convocatoria 2026/2027")
    r_modulo_val.font.size = Pt(12)

    # Salto de página para la página 2 (primera de contenido)
    doc.add_page_break()

    # =========================================================================
    # PÁGINA 2: ÍNDICE, PROBLEMA Y SOLUCIÓN DIGITAL (MEMORIX)
    # =========================================================================
    
    # Índice enlazable
    add_section_heading("Índice de Contenidos", "toc")
    
    toc_items = [
        ("1. Problema o Necesidad Detectada", "sec_problema", "Pág. 2"),
        ("2. Solución Digital: Memorix", "sec_solucion", "Pág. 2"),
        ("3. Funcionalidades de la Propuesta", "sec_funcionalidades", "Pág. 3"),
        ("4. Mejora Futura y Escalabilidad", "sec_mejora", "Pág. 3"),
        ("5. Identidad Visual y Prototipo", "sec_imagen", "Pág. 3"),
        ("6. Fuentes y Referencias Consultadas", "sec_fuentes", "Pág. 3"),
    ]
    for title, anchor, pag in toc_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.line_spacing = 1.2
        p_item.paragraph_format.space_after = Pt(2)
        add_toc_item(p_item, title, anchor, pag)

    # 1. PROBLEMA O NECESIDAD
    add_section_heading("1. Problema o Necesidad Detectada", "sec_problema")
    
    add_body_p(
        "El incumplimiento terapéutico constituye una de las mayores crisis silenciosas de la salud pública. En pacientes con tratamientos continuados, es habitual olvidar tomas, confundir posologías o abandonar medicamentos esenciales por incomprensión de las instrucciones. De forma paralela, las personas que sufren traumatismos o dolor muscular no realizan su rehabilitación física domiciliaria porque las pautas en papel se extravían o no garantizan una postura correcta.",
        bold_prefix="• ¿Qué ocurre? "
    )

    add_body_p(
        "Afecta principalmente a personas mayores con polimedicación y a pacientes con fases tempranas de Alzheimer o deterioro cognitivo leve. Asimismo, genera una severa sobrecarga mental en cuidadores y familiares, obligados a supervisar las tomas diarias sin herramientas automáticas. En el plano motriz, afecta a deportistas, trabajadores sedentarios y personas en recuperación de lesiones traumatológicas.",
        bold_prefix="• ¿A quién afecta? "
    )

    add_body_p(
        "El teléfono móvil permite sustituir la incertidumbre del papel por alarmas habladas, confirmaciones táctiles simples e interfaces de máximo contraste visual (Modo Memorix). La propuesta impacta de lleno en el ODS 3 (Salud y Bienestar) al prevenir ingresos hospitalarios por error farmacológico y acelerar la recuperación física, y en el ODS 10 (Reducción de las Desigualdades) al eliminar la brecha digital en personas mayores.",
        bold_prefix="• ¿Por qué puede mejorarse y ODS? "
    )

    # 2. SOLUCIÓN DIGITAL: MEMORIX
    add_section_heading("2. Solución Digital: Memorix", "sec_solucion")

    add_body_p(
        "Memorix es una aplicación móvil multiplataforma (Android e iOS) concebida como un copiloto de salud accesible que fusiona la disciplina del tratamiento farmacológico con la actividad física de rehabilitación motriz en un entorno gráfico de alta visibilidad.",
        bold_prefix="• Explicación de la idea: "
    )

    add_body_p(
        "Memorix programa alarmas prioritarias que leen en voz alta el nombre del medicamento, dosis y pauta de ingesta (ej. 'tomar con agua tras la comida'). Dispone de confirmación de un solo toque y alerta diferida automática al cuidador ante retrasos. En paralelo, integra un entrenador de fisioterapia con rutinas visuales, temporizador guiado y ejercicios específicos para tonificar músculos lesionados o aliviar dolores musculares.",
        bold_prefix="• ¿Qué permitiría hacer? "
    )

    add_body_p(
        "1) Pacientes senior o con problemas de memoria (interfaz 'Modo Fácil' de alto contraste); 2) Usuarios en rehabilitación muscular o con dolores de espalda/cuello; 3) Cuidadores y familiares que requieren tele-supervisión tranquila y eficaz.",
        bold_prefix="• ¿Quién utilizaría la aplicación? "
    )

    # Salto de página para la página 3 (segunda página de contenido)
    doc.add_page_break()

    # =========================================================================
    # PÁGINA 3: FUNCIONALIDADES, MEJORAS, IDENTIDAD VISUAL Y FUENTES
    # =========================================================================

    # 3. FUNCIONALIDADES
    add_section_heading("3. Funcionalidades de la Propuesta", "sec_funcionalidades")

    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Funcionalidad"
    hdr_cells[1].text = "Descripción"
    hdr_cells[0].width = Inches(2.2)
    hdr_cells[1].width = Inches(4.5)

    for cell in hdr_cells:
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="050C26"/>')
        cell._tc.get_or_add_tcPr().append(shading)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.bold = True
                r.font.size = Pt(11)
                r.font.color.rgb = RGBColor(255, 255, 255)

    funcs_data = [
        ("Registro y Perfil Dual", "Configuración de perfiles adaptados: modo autónomo, modo asistido (para mayores) y perfil de cuidador supervisor."),
        ("Alarmas con Locución por Voz", "Avisos sonoros que reproducen por síntesis de voz el nombre del fármaco, dosis e instrucciones comprensibles."),
        ("Confirmación y Antiolvido", "Botón táctil de gran formato para confirmar la ingesta; registra hora exacta para evitar dosis duplicadas."),
        ("Alerta SOS a Cuidadores", "Si tras 20 minutos no se confirma una toma prioritaria, Memorix avisa por notificación push o SMS al contacto asignado."),
        ("Módulo de Fisioterapia Activa", "Catálogo interactivo con rutinas visuales para dolor lumbar, hombro, rodilla o cuello con conteo de series y descanso."),
        ("Prospecto Accesible", "Resumen claro sin tecnicismos que indica la función del fármaco, advertencias y alimentos incompatibles."),
        ("Modo Contraste Accesible", "Temas cromáticos optimizados (azul profundo, cian, menta y blanco) diseñados para máxima legibilidad visual (WCAG).")
    ]

    for idx, (func, desc) in enumerate(funcs_data):
        row_cells = table.add_row().cells
        row_cells[0].width = Inches(2.2)
        row_cells[1].width = Inches(4.5)
        row_cells[0].text = func
        row_cells[1].text = desc

        fill_color = "F1F5F9" if idx % 2 == 0 else "FFFFFF"
        for i_col, cell in enumerate(row_cells):
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
            cell._tc.get_or_add_tcPr().append(shd)
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(10)
                    r.font.color.rgb = RGBColor(30, 41, 59)
                    if i_col == 0:
                        r.font.bold = True

    # Bordes de la tabla
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="050C26"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

    # 4. MEJORA FUTURA
    add_section_heading("4. Mejora Futura y Escalabilidad", "sec_mejora")
    add_body_p(
        "Como salto tecnológico se incorporará Visión por Computador (Computer Vision) mediante la cámara frontal para evaluar la ejecución de los ejercicios de rehabilitación y corregir la postura en directo. Además, se integrará con pulseras inteligentes (vibración háptica y detección de caídas), pastilleros IoT con apertura inteligente y sincronización con los sistemas de receta electrónica autonómicos.",
        bold_prefix="• Evolución del sistema: "
    )

    # 5. IDENTIDAD VISUAL Y PROTOTIPO
    add_section_heading("5. Identidad Visual y Prototipo de la Propuesta", "sec_imagen")
    
    img_mockup = os.path.join(curr_dir, "mockup_memorix.jpg")
    img_contraste = os.path.join(curr_dir, "contrastes.png")

    if os.path.exists(img_mockup):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.paragraph_format.space_before = Pt(3)
        p_img1.paragraph_format.space_after = Pt(2)
        r_img1 = p_img1.add_run()
        r_img1.add_picture(img_mockup, width=Inches(4.6))

        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap1.paragraph_format.space_after = Pt(4)
        r_cap1 = p_cap1.add_run("Figura 1: Prototipo funcional de Memorix (Alarma con audio-guía y sesión de ejercicios guiados).")
        r_cap1.font.name = "Calibri"
        r_cap1.font.size = Pt(9)
        r_cap1.font.italic = True
        r_cap1.font.color.rgb = RGBColor(100, 116, 139)

    # 6. FUENTES CONSULTADAS
    add_section_heading("6. Fuentes y Referencias Consultadas", "sec_fuentes")
    
    p_f1 = doc.add_paragraph()
    p_f1.paragraph_format.line_spacing = 1.15
    p_f1.paragraph_format.space_after = Pt(2)
    r1 = p_f1.add_run("• Organización Mundial de la Salud (OMS): ")
    r1.font.name = "Calibri"
    r1.font.size = Pt(11)
    r1.font.bold = True
    add_external_link(p_f1, "https://www.who.int/es/publications/i/item/9241545992", "Adherencia a los tratamientos a largo plazo: pruebas para la acción (Enlace web)")

    p_f2 = doc.add_paragraph()
    p_f2.paragraph_format.line_spacing = 1.15
    p_f2.paragraph_format.space_after = Pt(2)
    r2 = p_f2.add_run("• Sociedad Española de Geriatría y Gerontología (SEGG): ")
    r2.font.name = "Calibri"
    r2.font.size = Pt(11)
    r2.font.bold = True
    add_external_link(p_f2, "https://www.segg.es", "Guías de buena práctica clínica en polimedicación y personas mayores (Enlace web)")

    p_f3 = doc.add_paragraph()
    p_f3.paragraph_format.line_spacing = 1.15
    p_f3.paragraph_format.space_after = Pt(2)
    r3 = p_f3.add_run("• Naciones Unidas (ODS): ")
    r3.font.name = "Calibri"
    r3.font.size = Pt(11)
    r3.font.bold = True
    add_external_link(p_f3, "https://www.un.org/sustainabledevelopment/es/health/", "Objetivo 3: Salud y Bienestar y Objetivo 10: Reducción de las Desigualdades (Enlace web)")

    output_path = os.path.join(curr_dir, "Tarea0_Memorix_Kevin.docx")
    doc.save(output_path)
    print(f"Document saved successfully at: {output_path}")

if __name__ == "__main__":
    create_document()
