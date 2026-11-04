import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from pathlib import Path
from PIL import Image

DEST_DIR = Path(r"c:\Users\kevin\OneDrive\Documentos\GitHub\Curso-Dam2\Sistema gestion empresarial\UD04\practica_taberna_moe")
CAPTURES_DIR = DEST_DIR / "capturas"
DOCX_PATH = DEST_DIR / "Memoria_Practica_UD04_Kevin_Odoo.docx"

doc = docx.Document()

# Configurar márgenes estándar (0.75 pulgadas / ~1.9 cm)
for section in doc.sections:
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

# Colores institucionales
COLOR_PRIMARY = RGBColor(0x71, 0x4B, 0x67)  # Odoo Purple
COLOR_MUTED = RGBColor(0x55, 0x55, 0x55)
COLOR_TEXT = RGBColor(0x22, 0x22, 0x22)

# Encabezado formal con metadatos
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_title = title_p.add_run("MEMORIA PRÁCTICA UD04: LA TABERNA DE MOE (ODOO v18)")
run_title.font.name = "Arial"
run_title.font.size = Pt(16)
run_title.font.bold = True
run_title.font.color.rgb = COLOR_PRIMARY

# Tabla de datos del alumno y repositorio
meta_table = doc.add_table(rows=3, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_table.autofit = False

data = [
    ("Alumno:", "Kevin"),
    ("Actividad:", "Sistemas de Gestión Empresarial (2º DAM) - Despliegue y Migración ERP"),
    ("Repositorio GitHub:", "https://github.com/Kevin/Curso-Dam2/tree/main/Sistema%20gestion%20empresarial/UD04/practica_taberna_moe (Privado)")
]

for row_idx, (col1, col2) in enumerate(data):
    row = meta_table.rows[row_idx]
    
    cell_label = row.cells[0]
    cell_label.width = Inches(1.8)
    p1 = cell_label.paragraphs[0]
    r1 = p1.add_run(col1)
    r1.font.name = "Arial"
    r1.font.size = Pt(9.5)
    r1.font.bold = True
    
    cell_val = row.cells[1]
    cell_val.width = Inches(5.0)
    p2 = cell_val.paragraphs[0]
    r2 = p2.add_run(col2)
    r2.font.name = "Arial"
    r2.font.size = Pt(9.5)

sep = doc.add_paragraph()
sep.paragraph_format.space_before = Pt(4)
sep.paragraph_format.space_after = Pt(12)

# Función para insertar sección directa: Título + Imagen grande y nítida + Pie
def add_item(num_text, img_name, caption_text):
    img_path = CAPTURES_DIR / img_name
    if not img_path.exists():
        print(f"Aviso: {img_name} no existe")
        return

    # Título del requisito
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(16)
    p_title.paragraph_format.space_after = Pt(6)
    p_title.paragraph_format.keep_with_next = True
    run_t = p_title.add_run(num_text)
    run_t.font.name = "Arial"
    run_t.font.size = Pt(11.5)
    run_t.font.bold = True
    run_t.font.color.rgb = COLOR_PRIMARY

    # Dimensionar la imagen adecuadamente (entre 5.5 y 6.0 pulgadas de ancho)
    with Image.open(img_path) as im:
        orig_w, orig_h = im.size

    aspect_ratio = orig_h / orig_w
    target_width_inches = 5.8
    # Si la imagen es muy alta (ej. vertical), limitamos el alto para que quepa en la página
    if target_width_inches * aspect_ratio > 4.2:
        target_width_inches = 4.2 / aspect_ratio

    # Imagen centrada
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(4)
    p_img.paragraph_format.keep_with_next = True
    p_img.add_run().add_picture(str(img_path), width=Inches(target_width_inches))

    # Pie de imagen descriptivo
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(14)
    run_c = p_cap.add_run(caption_text)
    run_c.font.name = "Arial"
    run_c.font.size = Pt(9)
    run_c.font.italic = True
    run_c.font.color.rgb = COLOR_MUTED

# Lista de requisitos según el enunciado estricto
ITEMS = [
    (
        "1. Datos de la Empresa con Imagen Asociada y Localización Fiscal",
        "01_datos_empresa_login_8070.png",
        "Pantalla de inicio de sesión mostrando el logotipo corporativo oficial de 'La Taberna de Moe' y acceso al sistema."
    ),
    (
        "2. Factura emitida a Barney Gumble como Cliente",
        "03_factura_barney_inv202400001_pagada.png",
        "Factura de cliente INV/2024/00001 formalizada a Barney Gumble con IVA al 21% en estado PAGADO (605,00 €)."
    ),
    (
        "3. Registro consolidado de Facturas de Clientes",
        "04_facturacion_listado_facturas.png",
        "Panel del módulo Facturación con el listado de facturas emitidas a clientes e impuestos."
    ),
    (
        "4. Perfil de Lurleen Lumpkin en el departamento de Ventas con Imagen y Cuenta Odoo",
        "05_empleados_lurleen_lumpkin_ventas.png",
        "Ficha de la empleada Lurleen Lumpkin en el departamento de Ventas con su fotografía oficial asociada."
    ),
    (
        "5. Perfil de Waylon Smithers en el departamento de Administración con Imagen y Cuenta Odoo",
        "06_empleados_waylon_smithers_administracion.png",
        "Ficha del empleado Waylon Smithers en el departamento de Administración con su fotografía oficial asociada."
    ),
    (
        "6. Solicitud de Presupuesto para Duff 0,0 a Cervezas Duff como Proveedor",
        "07_compra_solicitud_presupuesto_p00001_duff_pdf.png",
        "Documento oficial en PDF de la Solicitud de Presupuesto P00001 a Cervezas Duff solicitando Cerveza Duff 0.0."
    ),
    (
        "7. Pedido de Compra confirmado para Duff 0,0 a Cervezas Duff",
        "08_compra_pedido_compra_p00001_duff_confirmado.png",
        "Pedido de Compra P00001 confirmado al proveedor Cervezas Duff listo para envío por correo."
    ),
    (
        "8. Presupuesto para Barney Gumble pidiendo una ronda de Cervezas",
        "02_presupuesto_s00001_barney_pdf.png",
        "Presupuesto formal en PDF #S00001 a Barney Gumble con membrete de la taberna, desglose impositivo y total."
    ),
    (
        "9. Confirmación de Presupuesto de Barney y Factura generada vinculada",
        "09_ventas_pedido_s00001_factura_generada.png",
        "Pedido de venta S00001 confirmado para Barney Gumble mostrando el acceso inteligente a la Factura generada."
    ),
    (
        "10. Productos registrados en TPV (Cerveza Duff y Cerveza Duff 0,0 con Imagen) y Comanda de 5 Cervezas 0,0",
        "10_tpv_productos_duff_pedido_5cervezas.png",
        "Terminal Punto de Venta (TPV) con catálogo fotográfico de productos y comanda de 5 Cervezas Duff 0.0 (9,08 €)."
    ),
    (
        "11. Recibo del pedido del TPV tras pagarlo",
        "11_tpv_ticket_recibo_pago_efectivo.png",
        "Ticket/Recibo oficial emitido por el TPV tras registrar el cobro en efectivo con desglose de IVA (21%)."
    ),
    (
        "12. Módulo Interesante Adicional: CRM con Oportunidad de Barney Ganada (100.000 €)",
        "12_crm_oportunidad_barney_ganada.png",
        "Módulo CRM tras su instalación con el flujo comercial y la oportunidad de Barney Gumble marcada en estado Ganado."
    ),
    (
        "13. Backup: Verificación del nombre de la base de datos (taverna)",
        "13_backup_verificacion_bd_taverna.png",
        "Comprobación en PostgreSQL del nombre de la base de datos 'taverna' y su propietario 'odoo'."
    ),
    (
        "14. Backup: Volcado relacional con pg_dump a archivo .sql (26 MB)",
        "14_backup_pg_dump_26mb.png",
        "Ejecución de pg_dump generando un backup íntegro de 26 Megabytes en ./baks/backup_bd.sql."
    ),
    (
        "15. Backup: Directorio baks con base de datos, odoo.conf y datos comprimidos",
        "15_backup_archivos_directorio_baks.png",
        "Contenido de la carpeta ./baks con backup_bd.sql, odoo.conf y odoo_data_backup.tar.gz."
    ),
    (
        "16. Migración: docker-compose.yml reconfigurado con nuevo puerto 8070 y nuevas rutas",
        "16_migracion_compose_puerto_8070.png",
        "Mapeo de puertos (8070:8069) y nuevas rutas de persistencia ./volumesOdoo_Nuevo en docker-compose.yml."
    ),
    (
        "17. Migración: Inyección y restauración de la base de datos SQL en el nuevo contenedor",
        "17_migracion_restauracion_sql_exitosa.png",
        "Restauración relacional exitosa inyectando backup_bd.sql en la base de datos 'taverna' del nuevo contenedor."
    ),
    (
        "18. Migración: Verificación de contenedores activos en el nuevo puerto 8070",
        "18_migracion_verificacion_contenedores_up.png",
        "Salida de docker compose ps mostrando los servicios web y db en estado Up y escuchando en el puerto 8070."
    ),
    (
        "19. Muestra de Odoo en la nueva URL tras la migración (http://localhost:8070)",
        "01_datos_empresa_login_8070.png",
        "Acceso verificado a Odoo en la nueva URL http://localhost:8070 con persistencia total de datos y multimedia."
    )
]

print("Generando documento Word (.docx) con imágenes a tamaño completo...")
for item in ITEMS:
    add_item(*item)

doc.save(str(DOCX_PATH))
print(f"¡Documento Word guardado exitosamente en: {DOCX_PATH}!")
