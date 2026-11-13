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

for section in doc.sections:
    section.top_margin = Inches(0.85)
    section.bottom_margin = Inches(0.85)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

COLOR_TEXT = RGBColor(0x11, 0x11, 0x11)
COLOR_MUTED = RGBColor(0x55, 0x55, 0x55)
COLOR_SHELL_LABEL = RGBColor(0x88, 0x88, 0x88)
COLOR_COMMENT = RGBColor(0xB0, 0x30, 0x60)
COLOR_CMD = RGBColor(0x22, 0x22, 0x22)
COLOR_DEST = RGBColor(0x00, 0x5A, 0x9E)
BG_CODE_HEX = "F6F7F9"

def set_cell_background(cell, fill_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=110, bottom=110, left=180, right=180):
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
    set_cell_margins(cell, top=110, bottom=110, left=180, right=180)
    
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
    p.paragraph_format.space_before = Pt(15)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = False
    r.font.color.rgb = COLOR_TEXT

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
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

p_title = doc.add_paragraph()
p_title.paragraph_format.space_before = Pt(6)
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
add_body("Detenga el contenedor de Odoo web y ejecute pg_dump sobre PostgreSQL para volcar la base de datos 'taverna' en formato .sql:")
add_code_block(doc, [
    "# 1. Parar contenedor web de Odoo",
    "docker stop odood-web-1",
    "",
    "# 2. Realizar el dump de la BD 'taverna' hacia ./baks/backup_bd.sql",
    "docker exec -t odood-db-1 pg_dump -U odoo taverna > ./baks/backup_bd.sql"
])

add_h2("1.2 Copiar configuración y empaquetar carpetas con tar -C")
add_body("Copie el archivo de configuración odoo.conf hacia su directorio local de backup:")
add_code_block(doc, [
    "docker cp odood-web-1:/etc/odoo/odoo.conf ./baks/odoo.conf"
])

add_body("Comprima las carpetas filestore, sessions y addons usando el flag -C para que no se guarden subcarpetas contenedoras extra dentro del .tar:")
add_code_block(doc, [
    "# Comprimir filestore, sessions y addons limpios",
    "tar -cvf ./baks/backupfile.tar -C ./volumesOdoo/odoo filestore",
    "tar -cvf ./baks/backupsessions.tar -C ./volumesOdoo/odoo sessions",
    "tar -cvf ./baks/backupaddons.tar -C ./volumesOdoo addons"
])

# SECCIÓN 2
add_h1("2. Restauración del Entorno (Migración)")

add_h2("2.1 Detener y reconfigurar el servicio")
add_body("Detenga todos los servicios actuales y edite docker-compose.yml cambiando puerto (8080:8069) y rutas nuevas:")
add_code_block(doc, [
    "docker compose down",
    "nano docker-compose.yml"
])
add_code_block(doc, [
    "# Rutas nuevas en docker-compose.yml:",
    "ports:",
    '  - "8080:8069"',
    "volumes:",
    "  - ./volumesOdoo_migracion2/addons:/mnt/extra-addons",
    "  - ./volumesOdoo_migracion2/odoo/filestore:/var/lib/odoo/filestore",
    "  - ./volumesOdoo_migracion2/odoo/sessions:/var/lib/odoo/sessions"
])

add_h2("2.2 Iniciar servicio de BD y crear base de datos limpia")
add_body("Levante únicamente el servicio de base de datos e instancie la base de datos vacía 'taverna':")
add_code_block(doc, [
    "docker compose up -d db",
    'docker compose exec -T db psql -U odoo -d postgres -c "CREATE DATABASE taverna OWNER odoo;"'
])

add_h2("2.3 Restaurar el dump de la BD y limpiar caché de estilos")
add_body("Inyecte el archivo backup_bd.sql y limpie la caché de adjuntos (/web/assets) para garantizar que se muestren las cajas de inicio de sesión:")
add_code_block(doc, [
    "# 1. Inyectar el volcado relacional a la base de datos taverna",
    "docker compose exec -T db psql -U odoo -d taverna < ./baks/backup_bd.sql",
    "",
    "# 2. Limpiar caché de estilos para que aparezcan las cajas de Correo y Contraseña",
    'docker compose exec -T db psql -U odoo -d taverna -c "DELETE FROM ir_attachment WHERE url LIKE \'/web/assets/%\';"'
])

add_h2("2.4 Extraer archivos de datos y levantar Odoo")
add_body("Rutas exactas donde deben quedar las 3 carpetas:")
add_bullet("filestore ➔ ", "./volumesOdoo_migracion2/odoo/filestore")
add_bullet("sessions ➔ ", "./volumesOdoo_migracion2/odoo/sessions")
add_bullet("addons ➔ ", "./volumesOdoo_migracion2/addons")

add_code_block(doc, [
    "# Crear carpetas de destino y dar permisos",
    "mkdir -p ./volumesOdoo_migracion2/odoo ./volumesOdoo_migracion2/addons",
    "sudo chmod -R 777 ./volumesOdoo_migracion2",
    "",
    "# Descomprimir archivos .tar en sus destinos",
    "sudo tar -xvf ./baks/backupfile.tar -C ./volumesOdoo_migracion2/odoo/",
    "sudo tar -xvf ./baks/backupsessions.tar -C ./volumesOdoo_migracion2/odoo/",
    "sudo tar -xvf ./baks/backupaddons.tar -C ./volumesOdoo_migracion2/",
    "",
    "# (Si el tar creó una subcarpeta volumesOdoo extra, mover su contenido así):",
    "sudo cp -r ./volumesOdoo_migracion2/odoo/volumesOdoo/odoo/filestore/* ./volumesOdoo_migracion2/odoo/filestore/ 2>/dev/null || true",
    "sudo rm -rf ./volumesOdoo_migracion2/odoo/volumesOdoo ./volumesOdoo_migracion2/odoo/addons"
])

add_body("Inicie todo el sistema, copie el archivo odoo.conf y reinicie el contenedor web:")
add_code_block(doc, [
    "docker compose up -d",
    "docker compose cp ./baks/odoo.conf web:/etc/odoo/odoo.conf",
    "sudo chmod -R 777 ./volumesOdoo_migracion2",
    "docker compose restart web"
])

add_h2("2.5 Credenciales de acceso y limpieza final")
add_bullet("URL de acceso: ", "http://localhost:8080 (pulsar Ctrl + F5 para recargar)")
add_bullet("Usuario / Correo: ", "a@a.com")
add_bullet("Contraseña: ", "a  (o 'admin')")
add_code_block(doc, [
    "# Eliminar el volumen antiguo una vez comprobado que todo funciona",
    "sudo rm -rf ./volumesOdoo"
])

doc.save(str(DOCX_PATH))
print(f"Word Guia guardado en: {DOCX_PATH}")
