import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os

def create_document():
    doc = docx.Document()

    # Configure margins (2.5 cm all sides)
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)
        section.different_first_page_header_footer = True

        # Header for subsequent pages
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("Proyecto Intermodular - 2º DAM  |  Tarea 0: Solución Digital")
        r_hdr.font.name = "Calibri"
        r_hdr.font.size = Pt(8.5)
        r_hdr.font.color.rgb = RGBColor(120, 144, 156)

        # Footer for subsequent pages
        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ftr_l = p_ftr.add_run("FarmaCare & Physio  •  Propuesta Inicial\t\tPágina ")
        r_ftr_l.font.name = "Calibri"
        r_ftr_l.font.size = Pt(9)
        r_ftr_l.font.color.rgb = RGBColor(120, 144, 156)
        
        # Add dynamic page number field in footer
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

    # Style defaults
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Calibri'
    font_normal.size = Pt(12)
    font_normal.color.rgb = RGBColor(44, 62, 80)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(4)

    # Helper for adding bookmarks
    bookmark_id = 0
    def add_bookmark(paragraph, name):
        nonlocal bookmark_id
        bookmark_id += 1
        b_start = parse_xml(f'<w:bookmarkStart {nsdecls("w")} w:id="{bookmark_id}" w:name="{name}"/>')
        b_end = parse_xml(f'<w:bookmarkEnd {nsdecls("w")} w:id="{bookmark_id}"/>')
        paragraph._p.insert(0, b_start)
        paragraph._p.append(b_end)

    # Helper for adding external hyperlinks
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

    # Helper for adding internal TOC links
    def add_toc_item(paragraph, title, anchor_name, page_num_str):
        hyperlink = parse_xml(f'<w:hyperlink {nsdecls("w")} w:anchor="{anchor_name}" w:history="1"/>')
        run_title = parse_xml(
            f'<w:r {nsdecls("w")}><w:rPr>'
            f'<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
            f'<w:color w:val="005F73"/>'
            f'<w:u w:val="single"/>'
            f'</w:rPr><w:t>{title}</w:t></w:r>'
        )
        hyperlink.append(run_title)
        paragraph._p.append(hyperlink)

        r_dots = paragraph.add_run(f"  {'.' * 45}  ")
        r_dots.font.color.rgb = RGBColor(160, 174, 192)
        r_dots.font.name = "Calibri"
        r_dots.font.size = Pt(11)

        r_p = paragraph.add_run(page_num_str)
        r_p.font.name = "Calibri"
        r_p.font.size = Pt(11)
        r_p.font.bold = True
        r_p.font.color.rgb = RGBColor(44, 62, 80)

    # Helper for titles (Calibri 14pt Bold as required)
    def add_section_heading(title_text, anchor_name=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        
        run = p.add_run(title_text)
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(10, 37, 64)
        
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
            r_b.font.color.rgb = RGBColor(26, 82, 118)
        r_t = p.add_run(text)
        r_t.font.name = 'Calibri'
        r_t.font.size = Pt(12)
        r_t.font.color.rgb = RGBColor(44, 62, 80)
        return p

    # =========================================================================
    # 01 PORTADA
    # =========================================================================
    p_cov_sp1 = doc.add_paragraph()
    p_cov_sp1.paragraph_format.space_before = Pt(40)

    # Badge superior
    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_after = Pt(12)
    r_badge = p_badge.add_run("PROYECTO INTERMODULAR • 2º DAM")
    r_badge.font.name = "Calibri"
    r_badge.font.size = Pt(11)
    r_badge.font.bold = True
    r_badge.font.color.rgb = RGBColor(0, 150, 136)

    # Título principal
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(6)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run("FarmaCare & Physio")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(28)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(10, 37, 64)

    # Subtítulo de la propuesta
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(18)
    p_sub.paragraph_format.line_spacing = 1.2
    r_sub = p_sub.add_run("Asistente Móvil Inteligente para la Gestión de Tratamientos Farmacológicos y Rehabilitación Muscular Asistida")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(41, 128, 185)

    # Divisor horizontal elegante
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_after = Pt(24)
    r_line = p_line.add_run("—" * 32)
    r_line.font.color.rgb = RGBColor(189, 195, 199)

    # Cuadro informativo central
    p_tag = doc.add_paragraph()
    p_tag.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tag.paragraph_format.space_after = Pt(100)
    p_tag.paragraph_format.line_spacing = 1.3
    r_tag = p_tag.add_run("Tarea 0: Una Solución Digital para un Problema Real\nPropuesta Inicial y Definición del Proyecto de Fin de Ciclo")
    r_tag.font.name = "Calibri"
    r_tag.font.size = Pt(11)
    r_tag.font.color.rgb = RGBColor(86, 101, 115)

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

    # Salto de página para comenzar la página 2 (primera página de contenido)
    doc.add_page_break()

    # =========================================================================
    # PÁGINA 2: ÍNDICE, PROBLEMA Y SOLUCIÓN DIGITAL
    # =========================================================================
    
    # Índice enlazable
    add_section_heading("Índice de Contenidos", "toc")
    p_toc_box = doc.add_paragraph()
    p_toc_box.paragraph_format.line_spacing = 1.3
    p_toc_box.paragraph_format.space_after = Pt(2)
    
    toc_items = [
        ("1. Problema o Necesidad Detectada", "sec_problema", "Pág. 2"),
        ("2. Solución Digital Propuesta", "sec_solucion", "Pág. 2"),
        ("3. Funcionalidades de la Propuesta", "sec_funcionalidades", "Pág. 3"),
        ("4. Mejora Futura y Escalabilidad", "sec_mejora", "Pág. 3"),
        ("5. Imagen Ilustrativa de la Propuesta", "sec_imagen", "Pág. 3"),
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
        "El incumplimiento terapéutico es uno de los mayores desafíos sanitarios a nivel global. En tratamientos de media y larga duración, los pacientes frecuentemente olvidan tomas, confunden posologías o abandonan la medicación por desconocimiento de las pautas exactas o de los efectos adversos. A este factor se suma la falta de adherencia en procesos de rehabilitación muscular: tras un traumatismo o contractura, las personas no realizan sus ejercicios por falta de orientación o por perder las recomendaciones en papel.",
        bold_prefix="• ¿Qué ocurre? "
    )

    add_body_p(
        "Afecta de forma crítica a personas de edad avanzada con polimedicación y a pacientes con fases tempranas de Alzheimer o deterioro cognitivo leve. Asimismo, repercute negativamente en sus cuidadores y familiares, quienes sufren una elevada sobrecarga mental al monitorizar las tomas diarias. En el plano físico, afecta a deportistas y personas sedentarias con dolores posturales o traumatismos que requieren fortalecimiento muscular asistido.",
        bold_prefix="• ¿A quién afecta? "
    )

    add_body_p(
        "Los teléfonos móviles están siempre presentes en la vida cotidiana. Una solución digital permite transformar pautas farmacológicas complejas en alarmas contextuales interactivas con explicaciones habladas y guías visuales de ejercicios. Esta propuesta se alinea directamente con el ODS 3 (Salud y Bienestar) al promover el uso seguro de medicamentos y la recuperación física, y con el ODS 10 (Reducción de las Desigualdades) al acercar la salud digital mediante interfaces accesibles y adaptadas.",
        bold_prefix="• ¿Por qué puede mejorarse y vinculación con ODS? "
    )

    # 2. SOLUCIÓN DIGITAL
    add_section_heading("2. Solución Digital Propuesta", "sec_solucion")

    add_body_p(
        "FarmaCare & Physio es una aplicación móvil multiplataforma (Android/iOS) diseñada para centralizar de forma sencilla la gestión de tratamientos farmacológicos y la rehabilitación física muscular, combinando alarmas explicativas con rutinas de ejercicio adaptadas a cada dolencia.",
        bold_prefix="• Explicación de la idea: "
    )

    add_body_p(
        "La aplicación permite programar alarmas sonoras y por voz que no solo recuerdan la hora de la toma, sino que reproducen una breve explicación auditiva sobre qué es el medicamento, para qué sirve y recomendaciones (ej. tomar con comida). Incluye un botón de confirmación rápida y alerta diferida a familiares. Además, cuenta con un módulo de prescripción de ejercicios activos con animaciones 3D y temporizadores guiados para fortalecer grupos musculares dañados o prevenir dolores posturales.",
        bold_prefix="• ¿Qué permitiría hacer? "
    )

    add_body_p(
        "1) Pacientes mayores o personas con despistes recurrentes (interfaz 'Modo Fácil' con tipografía ampliada); 2) Personas en recuperación motora o con dolores musculares cotidianos; 3) Cuidadores y familiares que supervisan el cumplimiento de tratamientos a distancia.",
        bold_prefix="• ¿Quién utilizaría la aplicación? "
    )

    # Salto de página para la página 3 (segunda página de contenido)
    doc.add_page_break()

    # =========================================================================
    # PÁGINA 3: TABLA DE FUNCIONALIDADES, MEJORA FUTURA, IMAGEN Y FUENTES
    # =========================================================================

    # 3. FUNCIONALIDADES
    add_section_heading("3. Funcionalidades de la Propuesta", "sec_funcionalidades")

    # Tabla de funcionalidades
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Formato de cabecera de la tabla
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Funcionalidad"
    hdr_cells[1].text = "Descripción"
    hdr_cells[0].width = Inches(2.2)
    hdr_cells[1].width = Inches(4.5)

    for cell in hdr_cells:
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="0A2540"/>')
        cell._tc.get_or_add_tcPr().append(shading)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.bold = True
                r.font.size = Pt(11)
                r.font.color.rgb = RGBColor(255, 255, 255)

    funcs_data = [
        ("Registro y Perfil Dual", "Permite configurar perfiles adaptados: modo autónomo, modo asistido (para mayores) y perfil de cuidador supervisor."),
        ("Alarmas con Locución", "Emite alarmas acústicas y reproduce por voz el nombre del fármaco, la dosis y advertencias clave de administración."),
        ("Confirmación de Toma", "Botón táctil de gran tamaño para confirmar la ingesta; registra fecha y hora para evitar tomas duplicadas u olvidos."),
        ("Alertas a Cuidadores", "Si tras 20 minutos no se confirma una toma prioritaria, envía una notificación push o SMS al contacto de emergencia."),
        ("Módulo de Ejercicios Físicos", "Catálogo interactivo con rutinas visuales para dolor lumbar, cervical, hombro o rodilla con tiempos de reposo y series."),
        ("Prospecto Accesible", "Ficha técnica resumida con lenguaje cotidiano que explica para qué sirve cada medicamento y qué evitar ingerir junto a él."),
        ("Historial de Adherencia", "Genera estadísticas mensuales de cumplimiento farmacológico y actividad física exportables en PDF para el médico.")
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
                    r.font.color.rgb = RGBColor(44, 62, 80)
                    if i_col == 0:
                        r.font.bold = True

    # Bordes de la tabla
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="0A2540"/>'
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
        "Como evolución técnica se prevé incorporar Visión Artificial (Computer Vision) mediante la cámara frontal para evaluar en tiempo real la técnica del usuario al realizar los ejercicios de fisioterapia, corrigiendo posturas incorrectas. Asimismo, se integrará con pulseras inteligentes (vibración háptica de recordatorio y detección de caídas), pastilleros IoT con apertura automatizada e interoperabilidad con los servicios de receta electrónica del sistema sanitario público.",
        bold_prefix="• Evolución del sistema: "
    )

    # 5. IMAGEN DE LA PROPUESTA
    add_section_heading("5. Imagen Ilustrativa de la Propuesta", "sec_imagen")
    
    img_path = os.path.join(os.path.dirname(__file__), "mockup_farmacare.jpg")
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(5.0))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(6)
        r_cap = p_cap.add_run("Figura 1: Prototipo visual de interfaz para FarmaCare & Physio (Alarma de Medicación y Rutina Muscular).")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

    # 6. FUENTES CONSULTADAS
    add_section_heading("6. Fuentes y Referencias Consultadas", "sec_fuentes")
    
    p_f1 = doc.add_paragraph()
    p_f1.paragraph_format.line_spacing = 1.2
    p_f1.paragraph_format.space_after = Pt(2)
    r1 = p_f1.add_run("• Organización Mundial de la Salud (OMS): ")
    r1.font.name = "Calibri"
    r1.font.size = Pt(11)
    r1.font.bold = True
    add_external_link(p_f1, "https://www.who.int/es/publications/i/item/9241545992", "Adherencia a los tratamientos a largo plazo: pruebas para la acción (Enlace web)")

    p_f2 = doc.add_paragraph()
    p_f2.paragraph_format.line_spacing = 1.2
    p_f2.paragraph_format.space_after = Pt(2)
    r2 = p_f2.add_run("• Sociedad Española de Geriatría y Gerontología (SEGG): ")
    r2.font.name = "Calibri"
    r2.font.size = Pt(11)
    r2.font.bold = True
    add_external_link(p_f2, "https://www.segg.es", "Guías de buena práctica clínica en polimedicación y personas mayores (Enlace web)")

    p_f3 = doc.add_paragraph()
    p_f3.paragraph_format.line_spacing = 1.2
    p_f3.paragraph_format.space_after = Pt(2)
    r3 = p_f3.add_run("• Naciones Unidas (ODS): ")
    r3.font.name = "Calibri"
    r3.font.size = Pt(11)
    r3.font.bold = True
    add_external_link(p_f3, "https://www.un.org/sustainabledevelopment/es/health/", "Objetivo 3: Garantizar una vida sana y promover el bienestar para todos (Enlace web)")

    output_path = os.path.join(os.path.dirname(__file__), "Tarea0_FarmaCare_Kevin.docx")
    doc.save(output_path)
    print(f"Document saved successfully at: {output_path}")

if __name__ == "__main__":
    create_document()
