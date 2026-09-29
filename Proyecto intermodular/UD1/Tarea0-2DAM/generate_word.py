import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

def create_document():
    doc = docx.Document()
    curr_dir = os.path.dirname(__file__)

    # Margins setup: 0.8 inches all around for clean A4 layout
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)
        section.different_first_page_header_footer = True

        # Header on content pages
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("Proyecto Intermodular - 2º DAM  |  Tarea 0: Memorix")
        r_hdr.font.name = "Calibri"
        r_hdr.font.size = Pt(9)
        r_hdr.font.color.rgb = RGBColor(120, 144, 156)

        # Footer on content pages
        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ftr_l = p_ftr.add_run("Memorix  •  Kevin Muñoz Córcoles\t\tPágina ")
        r_ftr_l.font.name = "Calibri"
        r_ftr_l.font.size = Pt(9)
        r_ftr_l.font.color.rgb = RGBColor(120, 144, 156)
        
        # Word dynamic page number XML field
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
    font_normal.color.rgb = RGBColor(35, 47, 62)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(3)

    # Bookmark generator
    bookmark_id = 0
    def add_bookmark(paragraph, name):
        nonlocal bookmark_id
        bookmark_id += 1
        b_start = parse_xml(f'<w:bookmarkStart {nsdecls("w")} w:id="{bookmark_id}" w:name="{name}"/>')
        b_end = parse_xml(f'<w:bookmarkEnd {nsdecls("w")} w:id="{bookmark_id}"/>')
        paragraph._p.insert(0, b_start)
        paragraph._p.append(b_end)

    # External Hyperlink generator
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

    # Internal TOC Link generator
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

        r_dots = paragraph.add_run(f"  {'.' * 44}  ")
        r_dots.font.color.rgb = RGBColor(160, 174, 192)
        r_dots.font.name = "Calibri"
        r_dots.font.size = Pt(11)

        r_p = paragraph.add_run(page_num_str)
        r_p.font.name = "Calibri"
        r_p.font.size = Pt(11)
        r_p.font.bold = True
        r_p.font.color.rgb = RGBColor(5, 12, 38)

    # Section Headings (strictly Calibri 14pt Bold as required)
    def add_section_heading(title_text, anchor_name=None, space_before=6, space_after=2):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        
        run = p.add_run(title_text)
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(5, 12, 38)
        
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
            r_b.font.color.rgb = RGBColor(0, 150, 136)
        r_t = p.add_run(text)
        r_t.font.name = 'Calibri'
        r_t.font.size = Pt(12)
        r_t.font.color.rgb = RGBColor(40, 50, 60)
        return p

    # =========================================================================
    # PÁGINA 1: PORTADA
    # =========================================================================
    logo_light = os.path.join(curr_dir, "logo_memorix_light.png")

    p_sp_top = doc.add_paragraph()
    p_sp_top.paragraph_format.space_before = Pt(25)

    if os.path.exists(logo_light):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(10)
        r_l = p_logo.add_run()
        r_l.add_picture(logo_light, width=Inches(1.8))

    p_subbadge = doc.add_paragraph()
    p_subbadge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subbadge.paragraph_format.space_after = Pt(6)
    r_sb = p_subbadge.add_run("PROYECTO INTERMODULAR • 2º DAM")
    r_sb.font.name = "Calibri"
    r_sb.font.size = Pt(11)
    r_sb.font.bold = True
    r_sb.font.color.rgb = RGBColor(0, 150, 136)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.line_spacing = 1.1
    r_tit = p_title.add_run("Memorix")
    r_tit.font.name = "Calibri"
    r_tit.font.size = Pt(32)
    r_tit.font.bold = True
    r_tit.font.color.rgb = RGBColor(5, 12, 38)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(16)
    p_sub.paragraph_format.line_spacing = 1.2
    r_sub = p_sub.add_run("Asistente Móvil de Tratamientos Farmacológicos y Rehabilitación Muscular Guiada")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0, 56, 255)

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_after = Pt(16)
    r_d = p_div.add_run("—" * 30)
    r_d.font.color.rgb = RGBColor(203, 213, 225)

    p_desc_cov = doc.add_paragraph()
    p_desc_cov.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_desc_cov.paragraph_format.space_after = Pt(70)
    p_desc_cov.paragraph_format.line_spacing = 1.3
    r_dc = p_desc_cov.add_run("Tarea 0: Una Solución Digital para un Problema Real\nPropuesta Inicial y Definición del Proyecto Intermodular")
    r_dc.font.name = "Calibri"
    r_dc.font.size = Pt(11)
    r_dc.font.color.rgb = RGBColor(100, 116, 139)

    # Student metadata
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.line_spacing = 1.3
    p_meta.paragraph_format.space_after = Pt(0)
    
    r_aut_lbl = p_meta.add_run("Nombre y apellidos: ")
    r_aut_lbl.font.bold = True
    r_aut_lbl.font.size = Pt(12)
    r_aut_val = p_meta.add_run("Kevin Muñoz Córcoles\n")
    r_aut_val.font.size = Pt(12)
    
    r_cur_lbl = p_meta.add_run("Curso: ")
    r_cur_lbl.font.bold = True
    r_cur_lbl.font.size = Pt(12)
    r_cur_val = p_meta.add_run("2º Desarrollo de Aplicaciones Multiplataforma (DAM)\n")
    r_cur_val.font.size = Pt(12)

    r_mod_lbl = p_meta.add_run("Módulo: ")
    r_mod_lbl.font.bold = True
    r_mod_lbl.font.size = Pt(12)
    r_mod_val = p_meta.add_run("Proyecto Intermodular | Convocatoria 2026/2027")
    r_mod_val.font.size = Pt(12)

    # PAGE BREAK TO PAGE 2 (Content Page 1)
    doc.add_page_break()

    # =========================================================================
    # PÁGINA 2: ÍNDICE, PROBLEMA O NECESIDAD Y SOLUCIÓN DIGITAL
    # =========================================================================
    
    # Índice enlazable
    add_section_heading("Índice de Contenidos", "toc", space_before=0, space_after=3)
    
    toc_items = [
        ("1. Problema o Necesidad Detectada", "sec_problema", "Pág. 2"),
        ("2. Propuesta de Solución Digital: Memorix", "sec_solucion", "Pág. 2"),
        ("3. Funcionalidades del Sistema", "sec_funcionalidades", "Pág. 3"),
        ("4. Mejora Futura y Escalabilidad", "sec_mejora", "Pág. 3"),
        ("5. Prototipo e Identidad Visual", "sec_imagen", "Pág. 3"),
        ("6. Fuentes y Referencias Consultadas", "sec_fuentes", "Pág. 3"),
    ]
    for title, anchor, pag in toc_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.line_spacing = 1.15
        p_item.paragraph_format.space_after = Pt(2)
        add_toc_item(p_item, title, anchor, pag)

    # 1. PROBLEMA O NECESIDAD DETECTADA
    add_section_heading("1. Problema o Necesidad Detectada", "sec_problema", space_before=8, space_after=2)
    
    add_body_p(
        "El problema principal que he detectado surge de dos dificultades muy habituales en la vida diaria: los olvidos en la medicación y el abandono de la rehabilitación física en casa. En tratamientos de media o larga duración, muchas personas olvidan tomas o confunden las horas, lo que hace que los medicamentos no hagan el efecto deseado. Además, los prospectos médicos suelen tener una letra diminuta y explicaciones técnicas difíciles de entender para la mayoría de la gente. Al mismo tiempo, cuando una persona sufre una lesión muscular, un esguince o dolores de espalda por malas posturas o traumatismos, el médico o fisioterapeuta suele darle una hoja de papel con ejercicios para hacer en casa. En la práctica, esa hoja casi siempre termina perdiéndose o el paciente no recuerda bien cómo hacer el movimiento, por lo que acaba dejando de hacerlos y la recuperación se alarga.",
        bold_prefix="• ¿Qué ocurre? "
    )

    add_body_p(
        "Esta situación afecta de forma directa a personas mayores que toman varias pastillas al día y a pacientes en fases iniciales de Alzheimer o deterioro cognitivo leve, que todavía mantienen autonomía en casa pero necesitan ayuda para no equivocarse. También repercute intensamente en sus familiares y cuidadores, que sufren la preocupación constante de no saber si se han tomado las pastillas a tiempo. En la parte física, afecta a deportistas, trabajadores con sobrecargas o cualquier persona en recuperación de un traumatismo que necesita fortalecer músculos específicos.",
        bold_prefix="• ¿A quién afecta? "
    )

    add_body_p(
        "Conviene mejorar esta situación porque un error en la dosis o una toma omitida de medicamentos para la tensión o el corazón puede provocar un ingreso hospitalario evitable. En el plano físico, no realizar bien la rehabilitación puede cronificar una lesión. Hoy en día casi todo el mundo tiene un móvil a mano, por lo que podemos sustituir los papeles y los pastilleros de plástico por una herramienta accesible con avisos sonoros hablados y vídeos sencillos de ejercicios. Esta propuesta conecta directamente con el ODS 3 (Salud y Bienestar) y el ODS 10 (Reducción de las Desigualdades).",
        bold_prefix="• ¿Por qué debería mejorarse? "
    )

    # 2. PROPUESTA DE SOLUCIÓN DIGITAL
    add_section_heading("2. Propuesta de Solución Digital: Memorix", "sec_solucion", space_before=8, space_after=2)

    add_body_p(
        "Memorix es una aplicación móvil multiplataforma (diseñada para Android e iOS) pensada específicamente para ser muy intuitiva y limpia. Integra en un mismo lugar la gestión de los tratamientos farmacológicos diarios y una guía de ejercicios activos de fortalecimiento muscular, todo ello bajo una interfaz adaptada con botones grandes y colores de alto contraste que facilitan su lectura a personas con dificultades visuales o mayores.",
        bold_prefix="• Explicación de la idea: "
    )

    add_body_p(
        "La aplicación permite registrar la medicación con alarmas que suenan de forma clara y que además reproducen por voz qué pastilla toca y cómo tomarla (por ejemplo: 'Toca tomar Enalapril, una pastilla con un vaso de agua después de comer'). Incluye un botón grande para confirmar la toma y avisa automáticamente al cuidador si pasan más de 20 minutos sin confirmarse. En la parte física, ofrece un catálogo de ejercicios guiados con temporizador y demostraciones visuales para zonas concretas como hombros, espalda, cuello o piernas tras un traumatismo o sobrecarga.",
        bold_prefix="• ¿Qué permitiría hacer? "
    )

    add_body_p(
        "La utilizarán principalmente: 1) Personas mayores o con despistes frecuentes que necesitan un recordatorio claro; 2) Cuidadores y familiares que supervisan a distancia el cumplimiento del tratamiento; 3) Personas de cualquier edad en recuperación física que necesitan tablas guiadas de ejercicios musculares para hacer en su domicilio.",
        bold_prefix="• ¿Quién utilizaría la solución? "
    )

    # PAGE BREAK TO PAGE 3 (Content Page 2)
    doc.add_page_break()

    # =========================================================================
    # PÁGINA 3: FUNCIONALIDADES, MEJORA FUTURA, PROTOTIPO Y FUENTES
    # =========================================================================

    # 3. FUNCIONALIDADES DEL SISTEMA
    add_section_heading("3. Funcionalidades del Sistema", "sec_funcionalidades", space_before=0, space_after=2)

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
            p.paragraph_format.space_before = Pt(2.5)
            p.paragraph_format.space_after = Pt(2.5)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.bold = True
                r.font.size = Pt(10.5)
                r.font.color.rgb = RGBColor(255, 255, 255)

    funcs_data = [
        ("Perfiles de Paciente y Cuidador", "Permite configurar un modo fácil para el paciente y vincularlo con el móvil del familiar para supervisión a distancia."),
        ("Alarmas con Locución por Voz", "Avisos sonoros que leen en voz alta el nombre del medicamento, la dosis y consejos claros de toma (ej. tomar con comida)."),
        ("Confirmación de Toma y Registro", "Botón táctil grande para confirmar la ingesta; guarda la hora exacta para evitar tomas dobles accidentales."),
        ("Aviso de Seguridad al Cuidador", "Envía una alerta automática al móvil del cuidador si pasan 20 minutos desde la alarma sin confirmación de la toma."),
        ("Ejercicios Musculares Guiados", "Rutinas visuales para dolores o traumatismos (cuello, espalda, hombro, pierna) con temporizador, series y descansos."),
        ("Modo Contraste Accesible", "Esquemas de color de alto contraste (azul marino, cian, menta y blanco) diseñados para máxima legibilidad visual.")
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
    add_section_heading("4. Mejora Futura y Escalabilidad", "sec_mejora", space_before=6, space_after=2)
    add_body_p(
        "Como mejora futura para más adelante, la idea es incorporar visión artificial (Computer Vision) usando la cámara frontal del teléfono. De este modo, mientras el paciente realiza los ejercicios de rehabilitación delante del móvil, la aplicación podrá evaluar en tiempo real la postura del cuerpo y avisarle por voz si está curvando mal la espalda o forzando la articulación, evitando nuevas lesiones. Además, se contempla la vinculación con pulseras inteligentes (smartwatch) para avisar de las pastillas mediante vibración en la muñeca y detectar posibles caídas en personas mayores.",
        bold_prefix="• Evolución prevista: "
    )

    # 5. PROTOTIPO E IDENTIDAD VISUAL
    add_section_heading("5. Prototipo e Identidad Visual de la Propuesta", "sec_imagen", space_before=6, space_after=2)
    
    img_mockup = os.path.join(curr_dir, "mockup_memorix.jpg")
    if os.path.exists(img_mockup):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(2)
        p_img.paragraph_format.space_after = Pt(1)
        r_img = p_img.add_run()
        r_img.add_picture(img_mockup, width=Inches(3.8))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(4)
        r_cap = p_cap.add_run("Figura 1: Prototipo de Memorix mostrando la alarma con audio-guía y la rutina de ejercicios con temporizador.")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 116, 139)

    # 6. FUENTES CONSULTADAS
    add_section_heading("6. Fuentes y Referencias Consultadas", "sec_fuentes", space_before=5, space_after=2)
    
    p_f1 = doc.add_paragraph()
    p_f1.paragraph_format.line_spacing = 1.15
    p_f1.paragraph_format.space_after = Pt(1.5)
    r1 = p_f1.add_run("• Organización Mundial de la Salud (OMS): ")
    r1.font.name = "Calibri"
    r1.font.size = Pt(10.5)
    r1.font.bold = True
    add_external_link(p_f1, "https://www.who.int/es/publications/i/item/9241545992", "Informe sobre adherencia a los tratamientos a largo plazo (Enlace web)")

    p_f2 = doc.add_paragraph()
    p_f2.paragraph_format.line_spacing = 1.15
    p_f2.paragraph_format.space_after = Pt(1.5)
    r2 = p_f2.add_run("• Sociedad Española de Geriatría y Gerontología (SEGG): ")
    r2.font.name = "Calibri"
    r2.font.size = Pt(10.5)
    r2.font.bold = True
    add_external_link(p_f2, "https://www.segg.es", "Guía de buena práctica clínica en polimedicación en el anciano (Enlace web)")

    p_f3 = doc.add_paragraph()
    p_f3.paragraph_format.line_spacing = 1.15
    p_f3.paragraph_format.space_after = Pt(1.5)
    r3 = p_f3.add_run("• Naciones Unidas: ")
    r3.font.name = "Calibri"
    r3.font.size = Pt(10.5)
    r3.font.bold = True
    add_external_link(p_f3, "https://www.un.org/sustainabledevelopment/es/health/", "Objetivo de Desarrollo Sostenible 3: Salud y Bienestar (Enlace web)")

    output_path = os.path.join(curr_dir, "Tarea0_Memorix_Kevin.docx")
    doc.save(output_path)
    print(f"Document saved successfully at: {output_path}")

if __name__ == "__main__":
    create_document()
