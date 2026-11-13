import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from pathlib import Path

DEST_DIR = Path(r"c:\Users\kevin\OneDrive\Documentos\GitHub\Curso-Dam2\Sistema gestion empresarial\UD04\practica_taberna_moe")
DOCX_PATH = DEST_DIR / "Chuleta_Odoo_Desordenada_Kevin.docx"
PDF_PATH = DEST_DIR / "Chuleta_Odoo_Desordenada_Kevin.pdf"

# Lista en el ORDEN REAL DE EJECUCIÓN (Paso 1 al Paso 22)
# Incluye el paso salvavidas de DELETE FROM ir_attachment para que siempre salgan las cajas de login a la primera
ORDERED_STEPS = [
    # 1. Verificar nombre de la BD y propietario
    ('docker exec odood-db-1 psql -U odoo -l', 'listar BD y propietario'),
    # 2. Verificar espacio libre
    ('df -h .', 'espacio libre'),
    # 3. Parar el contenedor de Odoo
    ('docker stop odood-web-1', 'parar Odoo (contenedor)'),
    # 4. Hacer backup de la BD con pg_dump
    ('docker exec -t odood-db-1 pg_dump -U odoo taverna > ./baks/backup_bd.sql', 'volcar BD a .sql'),
    # 5. Hacer backup del archivo odoo.conf
    ('docker cp odood-web-1:/etc/odoo/odoo.conf ./baks/odoo.conf', 'sacar conf de Odoo'),
    # 6. Comprimir filestore limpio con -C
    ('tar -cvf ./baks/backupfile.tar -C ./volumesOdoo/odoo filestore', 'comprimir filestore limpio'),
    # 7. Comprimir sessions limpio con -C
    ('tar -cvf ./baks/backupsessions.tar -C ./volumesOdoo/odoo sessions', 'comprimir sessions limpio'),
    # 8. Comprimir addons limpio con -C
    ('tar -cvf ./baks/backupaddons.tar -C ./volumesOdoo addons', 'comprimir addons limpio'),
    # 9. Parar por completo todo el sistema Odoo
    ('docker compose down', 'parar y quitar todo'),
    # 10. Editar docker-compose.yml (cambiar puerto y rutas)
    ('nano docker-compose.yml', 'cambiar puerto (8080:8069) y rutas nuevas'),
    # 11. Lanzar compose pero solo la parte de la BD
    ('docker compose up -d db', 'arrancar solo la BD'),
    # 12. Dar permisos y crear carpetas en destino
    ('mkdir -p ./volumesOdoo_migracion2/odoo ./volumesOdoo_migracion2/addons && sudo chmod -R 777 ./volumesOdoo_migracion2', 'crear carpetas destino y dar permisos'),
    # 13. Extraer backupfile.tar y asegurar ruta filestore/taverna
    ('sudo tar -xvf ./baks/backupfile.tar -C ./volumesOdoo_migracion2/odoo/', 'extraer filestore (-C = destino)'),
    # 14. Extraer backupsessions.tar
    ('sudo tar -xvf ./baks/backupsessions.tar -C ./volumesOdoo_migracion2/odoo/', 'extraer sessions (-C = destino)'),
    # 15. Extraer backupaddons.tar
    ('sudo tar -xvf ./baks/backupaddons.tar -C ./volumesOdoo_migracion2/', 'extraer addons (-C = destino)'),
    # 16. Crear la BD vacía con el mismo nombre y propietario
    ('docker compose exec -T db psql -U odoo -d postgres -c "CREATE DATABASE taverna OWNER odoo;"', 'crear BD vacía con propietario'),
    # 17. Inyectar el script .sql contra el nuevo contenedor
    ('docker compose exec -T db psql -U odoo -d taverna < ./baks/backup_bd.sql', 'restaurar .sql en BD vacía'),
    # 18. Limpiar caché de estilos para que SIEMPRE salgan las cajas de login
    ('docker compose exec -T db psql -U odoo -d taverna -c "DELETE FROM ir_attachment WHERE url LIKE \'/web/assets/%\';"', 'arreglar cajas de login en blanco'),
    # 19. Lanzar todo el compose.yaml (el nuevo Odoo)
    ('docker compose up -d', 'arrancar todo'),
    # 20. Copiar el backup del archivo .conf al contenedor nuevo
    ('docker compose cp ./baks/odoo.conf web:/etc/odoo/odoo.conf', 'meter conf en Odoo'),
    # 21. Dar permisos finales y reiniciar contenedor web
    ('sudo chmod -R 777 ./volumesOdoo_migracion2 && docker compose restart web', 'permisos finales y reiniciar Odoo'),
    # 22. Tumbar/borrar el volumen del Odoo viejo
    ('sudo rm -rf ./volumesOdoo', 'borrar lo viejo')
]

# Algoritmo de reordenación en Zig-Zag:
# 1º en ejecutar -> Última fila (N-1)
# 2º en ejecutar -> Primera fila (0)
# 3º en ejecutar -> Penúltima fila (N-2)
# 4º en ejecutar -> Segunda fila (1)
N = len(ORDERED_STEPS)
zig_zag_table = [None] * N

for k, step in enumerate(ORDERED_STEPS):
    if k % 2 == 0:
        row_idx = N - 1 - (k // 2)
    else:
        row_idx = k // 2
    zig_zag_table[row_idx] = step

doc = docx.Document()

# Márgenes ajustados para que quepa todo en 1 sola página
for section in doc.sections:
    section.top_margin = Inches(0.45)
    section.bottom_margin = Inches(0.45)
    section.left_margin = Inches(0.6)
    section.right_margin = Inches(0.6)

COLOR_BLACK = RGBColor(0x00, 0x00, 0x00)
BORDER_GRAY = "AAAAAA"

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{BORDER_GRAY}"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{BORDER_GRAY}"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="{BORDER_GRAY}"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="{BORDER_GRAY}"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{BORDER_GRAY}"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="{BORDER_GRAY}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def set_cell_margins(cell, top=36, bottom=36, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_section_header(title_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title_text)
    r.font.name = "Arial"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLACK

def build_two_col_table(rows_data):
    table = doc.add_table(rows=len(rows_data), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)

    for idx, (cmd_str, desc_str) in enumerate(rows_data):
        row = table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(5.05)
        c1.width = Inches(2.15)
        set_cell_margins(c0)
        set_cell_margins(c1)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(cmd_str)
        r0.font.name = "Consolas"
        r0.font.size = Pt(7.8)
        r0.font.color.rgb = COLOR_BLACK

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(desc_str)
        r1.font.name = "Arial"
        r1.font.size = Pt(7.8)
        r1.font.color.rgb = COLOR_BLACK

# Cabecera idéntica a la original
p_title = doc.add_paragraph()
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(1)
r_t = p_title.add_run("Chuleta Odoo (desordenada)")
r_t.font.name = "Arial"
r_t.font.size = Pt(16)
r_t.font.bold = True
r_t.font.color.rgb = COLOR_BLACK

p_sub = doc.add_paragraph()
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(4)
r_sub = p_sub.add_run("Sustituye las MAYÚSCULAS o rutas si cambian. El orden lo pones tú.")
r_sub.font.name = "Arial"
r_sub.font.size = Pt(8.5)
r_sub.font.italic = True
r_sub.font.color.rgb = COLOR_BLACK

# Tabla Principal con el orden secreto (Última, Primera, Penúltima, Segunda...)
add_section_header("COMANDOS DE BACKUP Y MIGRACIÓN")
build_two_col_table(zig_zag_table)

# Tablas auxiliares de apoyo
add_section_header("CAMBIOS SUELTOS EN docker-compose.yml (nano docker-compose.yml, luego up -d)")
cambios_data = [
    ('"8080:8069"', 'puerto nuevo (lado izquierdo)'),
    ('- ./volumesOdoo_migracion2/odoo/filestore:/var/lib/odoo/filestore', 'ruta nueva de filestore de Odoo'),
    ('- ./volumesOdoo_migracion2/odoo/sessions:/var/lib/odoo/sessions', 'ruta nueva de sessions de Odoo'),
    ('- ./volumesOdoo_migracion2/addons:/mnt/extra-addons', 'ruta nueva de addons de Odoo'),
    ('- ./volumesOdoo_migracion2/dataPostgreSQL:/var/lib/postgresql/data', 'ruta nueva de datos de PostgreSQL')
]
build_two_col_table(cambios_data)

add_section_header("COMANDOS SALVAVIDAS Y CREDENCIALES")
nombres_data = [
    ('sudo cp -r ./volumesOdoo/odoo/filestore/taverna/* ./volumesOdoo_migracion2/odoo/filestore/taverna/', 'si el .tar metió subcarpeta volumesOdoo'),
    ('docker compose exec -T db psql -U odoo -d taverna -c "SELECT id, login FROM res_users;"', 'ver correo login (a@a.com)'),
    ('docker compose exec -T db psql -U odoo -d taverna -c "UPDATE res_users SET password=\'admin\' WHERE id=2;"', 'resetear contraseña a admin'),
    ('a@a.com  /  contraseña: a (o admin)', 'datos para iniciar sesión en Odoo')
]
build_two_col_table(nombres_data)

doc.save(str(DOCX_PATH))
print(f"Word Chuleta guardado en: {DOCX_PATH}")
