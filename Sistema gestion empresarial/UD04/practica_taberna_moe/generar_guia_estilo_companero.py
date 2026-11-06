import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from pathlib import Path

DEST_DIR = Path(r"c:\Users\kevin\OneDrive\Documentos\GitHub\Curso-Dam2\Sistema gestion empresarial\UD04\practica_taberna_moe")
DOCX_PATH = DEST_DIR / "Guia_Backup_Restauracion_Docker_Kevin.docx"
PDF_PATH = DEST_DIR / "Guia_Backup_Restauracion_Docker_Kevin.pdf"

doc = docx.Document()

# Márgenes estándar (1 pulgada / 2.54 cm)
for section in doc.sections:
    section.top_margin = Inches(0.9)
    section.bottom_margin = Inches(0.9)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Colores fieles al estilo del compañero
COLOR_TEXT = RGBColor(0x11, 0x11, 0x11)
COLOR_MUTED = RGBColor(0x55, 0x55, 0x55)
COLOR_SHELL_LABEL = RGBColor(0x88, 0x88, 0x88)
COLOR_COMMENT = RGBColor(0xB0, 0x30, 0x60)   # Magenta suave para comentarios bash
COLOR_CMD = RGBColor(0x22, 0x22, 0x22)
COLOR_DEST = RGBColor(0x00, 0x5A, 0x9E)  # Azul oscuro para rutas de destino
BG_CODE_HEX = "F6F7F9"

def set_cell_background(cell, fill_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_code_block(doc, code_lines):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.2)
    set_cell_background(cell, BG_CODE_HEX)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    p_shell = cell.paragraphs[0]
    p_shell.paragraph_format.space_before = Pt(0)
    p_shell.paragraph_format.space_after = Pt(3)
    p_shell.paragraph_format.line_spacing = Pt(11)
    r_shell = p_shell.add_run("Shell")
    r_shell.font.name = "Arial"
    r_shell.font.size = Pt(8.5)
    r_shell.font.color.rgb = COLOR_SHELL_LABEL

    for line in code_lines:
        p_code = cell.add_paragraph()
        p_code.paragraph_format.space_before = Pt(0)
        p_code.paragraph_format.space_after = Pt(2)
        p_code.paragraph_format.line_spacing = Pt(12)
        
        r = p_code.add_run(line)
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
        if line.strip().startswith("#"):
            r.font.color.rgb = COLOR_COMMENT
        else:
            r.font.color.rgb = COLOR_CMD
            
    p_sep = doc.add_paragraph()
    p_sep.paragraph_format.space_before = Pt(0)
    p_sep.paragraph_format.space_after = Pt(4)

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = False
    r.font.color.rgb = COLOR_TEXT

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(11.5)
    r.font.bold = False
    r.font.color.rgb = COLOR_TEXT

def add_body(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = Pt(13.5)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(9.5)
    r.font.color.rgb = COLOR_TEXT

def add_bullet(text, dest_text=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = Pt(13)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(9.5)
    r.font.color.rgb = COLOR_TEXT
    if dest_text:
        r2 = p.add_run(dest_text)
        r2.font.name = "Arial"
        r2.font.size = Pt(9.5)
        r2.font.bold = True
        r2.font.color.rgb = COLOR_DEST

# ==================== CONTENIDO COMPLETO ====================

# TÍTULO PRINCIPAL
p_title = doc.add_paragraph()
p_title.paragraph_format.space_before = Pt(8)
p_title.paragraph_format.space_after = Pt(10)
r_title = p_title.add_run("Guía de Copia de Seguridad y\nRestauración en Docker")
r_title.font.name = "Arial"
r_title.font.size = Pt(22)
r_title.font.bold = False
r_title.font.color.rgb = COLOR_TEXT

add_body("Esta guía detalla el procedimiento paso a paso para realizar una copia de seguridad (backup) y la posterior restauración de una instancia de Odoo y su base de datos PostgreSQL alojadas en contenedores Docker.")

# SECCIÓN 1
add_h1("1. Copia de Seguridad (Backup)")

add_h2("1.1 Exportar la base de datos (Directo desde el Host)")
add_body("Ejecute pg_dump directamente sobre el contenedor de PostgreSQL desde la terminal anfitriona sin necesidad de acceder a la terminal interna bash:")
add_code_block(doc, [
    "# Realizar el dump de la BD 'taverna' directamente hacia el archivo local",
    "docker exec -t odood-db-1 pg_dump -U odoo taverna > ./baks/backup_bd.sql"
])

add_h2("1.2 Copiar configuración y archivos adjuntos por comandos")
add_body("Copie el archivo de configuración odoo.conf desde el contenedor hacia su directorio local de backup:")
add_code_block(doc, [
    "docker cp odood-web-1:/etc/odoo/odoo.conf ./baks/odoo.conf"
])

add_body("A continuación, obtenga mediante comandos docker cp las carpetas con los archivos multimedia, sesiones y módulos:")
add_code_block(doc, [
    "# 1. Obtener filestore (logotipo de Moe, imágenes de productos y empleados)",
    "docker cp odood-web-1:/var/lib/odoo/filestore ./baks/filestore",
    "",
    "# 2. Obtener sesiones activas de usuario",
    "docker cp odood-web-1:/var/lib/odoo/sessions ./baks/sessions",
    "",
    "# 3. Obtener módulos adicionales (addons)",
    "docker cp odood-web-1:/mnt/extra-addons ./baks/addons"
])

add_body("Carpetas guardadas en el directorio de backup (./baks/):")
add_bullet("filestore ", "(imágenes de Duff, Barney, Smithers y logotipo corporativo)")
add_bullet("sessions ", "(tokens de inicio de sesión de Odoo)")
add_bullet("addons ", "(módulos personalizados instalados)")

# SECCIÓN 2
add_h1("2. Restauración del Entorno")

add_h2("2.1 Detener y reconfigurar el servicio")
add_body("Detenga los servicios actuales de Docker Compose:")
add_code_block(doc, [
    "docker compose down"
])
add_body("Modifique el puerto al 8070 y la configuración de los volúmenes para Odoo dentro del archivo docker-compose.yml según sea necesario:")
add_code_block(doc, [
    "# Fragmento modificado en docker-compose.yml:",
    "ports:",
    '  - "8070:8069"  # Nuevo puerto de acceso',
    "volumes:",
    "  - ./volumesOdoo_Nuevo/addons:/mnt/extra-addons",
    "  - ./volumesOdoo_Nuevo/odoo/filestore:/var/lib/odoo/filestore",
    "  - ./volumesOdoo_Nuevo/odoo/sessions:/var/lib/odoo/sessions"
])

add_h2("2.2 Iniciar servicio de BD y crear base de datos limpia")
add_body("Levante únicamente el servicio de base de datos e instancie la base de datos con el mismo nombre original:")
add_code_block(doc, [
    "# Iniciar contenedor de la base de datos",
    "docker compose up -d db",
    "",
    "# Crear la base de datos destino con nombre 'taverna'",
    'docker compose -p odood exec -T db psql -U odoo -d postgres -c "CREATE DATABASE taverna OWNER odoo;"'
])

add_h2("2.3 Restaurar el dump de la base de datos (Directo desde el Host)")
add_body("Inyecte el archivo backup_bd.sql directamente en la nueva base de datos sin necesidad de acceder a la terminal bash del contenedor:")
add_code_block(doc, [
    "# Inyectar el volcado relacional a la base de datos taverna",
    "cat ./baks/backup_bd.sql | docker compose -p odood exec -T db psql -U odoo -d taverna"
])

add_h2("2.4 Restablecer archivos de datos y configuración de Odoo")
add_body("Mueva las carpetas del backup a sus rutas de destino correspondientes dentro de los nuevos volúmenes montados:")
add_bullet("filestore ➔ ", "./volumesOdoo_Nuevo/odoo/filestore")
add_bullet("sessions ➔ ", "./volumesOdoo_Nuevo/odoo/sessions")
add_bullet("addons ➔ ", "./volumesOdoo_Nuevo/addons")

add_body("Comandos para copiar las carpetas a sus rutas definitivas:")
add_code_block(doc, [
    "# Crear directorios de destino en el host",
    "mkdir -p ./volumesOdoo_Nuevo/odoo ./volumesOdoo_Nuevo/addons",
    "",
    "# Mover/copiar las carpetas a sus rutas definitivas",
    "cp -r ./baks/filestore ./volumesOdoo_Nuevo/odoo/",
    "cp -r ./baks/sessions ./volumesOdoo_Nuevo/odoo/",
    "cp -r ./baks/addons/* ./volumesOdoo_Nuevo/addons/ 2>/dev/null || true"
])

add_body("Inicie todos los servicios definidos en el Compose:")
add_code_block(doc, [
    "docker compose up -d"
])

add_body("Sustituya el archivo de configuración odoo.conf dentro del contenedor:")
add_code_block(doc, [
    "docker cp ./baks/odoo.conf odood-web-1:/etc/odoo/odoo.conf"
])

p_final = doc.add_paragraph()
p_final.paragraph_format.space_before = Pt(14)
p_final.paragraph_format.space_after = Pt(8)
r_final = p_final.add_run("Ya puedes acceder a tu instancia de Odoo a través del puerto configurado (http://localhost:8070) y verificar que el proceso se ha completado con éxito con todos los datos y fotos recuperados.")
r_final.font.name = "Arial"
r_final.font.size = Pt(9.5)
r_final.font.color.rgb = COLOR_TEXT

# Guardar DOCX
doc.save(str(DOCX_PATH))
print(f"Word guardado en: {DOCX_PATH}")
