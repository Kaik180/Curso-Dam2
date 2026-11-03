import os
import shutil
from pathlib import Path
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

USER_UPLOADED_DIR = Path(r"C:\Users\kevin\.gemini\antigravity\brain\caa8573a-9486-4e92-b02f-12db2bbc0546\.user_uploaded")
DEST_DIR = Path(r"c:\Users\kevin\OneDrive\Documentos\GitHub\Curso-Dam2\Sistema gestion empresarial\UD04\practica_taberna_moe")
CAPTURES_DIR = DEST_DIR / "capturas"
CAPTURES_DIR.mkdir(parents=True, exist_ok=True)

# Mapeo de archivos fuente a nombres descriptivos
IMAGE_MAPPING = {
    "media_1793729739358_975b38ac.png": ("01_datos_empresa_login_8070.png", "Figura 1: Pantalla de inicio de sesión con el logotipo corporativo de 'La Taberna de Moe' tras la migración al puerto 8070."),
    "media_1793729464278_b64591c6.png": ("02_presupuesto_s00001_barney_pdf.png", "Figura 2: Presupuesto formal #S00001 emitido a Barney Gumble con membrete, localización (España) e IVA al 21%."),
    "media_1793729681428_796e4357.png": ("03_factura_barney_inv202400001_pagada.png", "Figura 3: Factura de cliente INV/2024/00001 formalizada y marcada en estado 'PAGADO' por valor de 605,00 €."),
    "media_1793729689941_db5eb686.png": ("04_facturacion_listado_facturas.png", "Figura 4: Panel del módulo Facturación con el registro consolidado de facturas de clientes e impuestos repercutidos."),
    "media_1793729776087_542afd9d.png": ("05_empleados_lurleen_lumpkin_ventas.png", "Figura 5: Ficha de la empleada Lurleen Lumpkin con fotografía asociada en el departamento de Ventas."),
    "media_1793729681423_1c6616fb.png": ("06_empleados_waylon_smithers_administracion.png", "Figura 6: Ficha del empleado Waylon Smithers con fotografía oficial en el departamento de Administración."),
    "media_1793729681409_59223702.png": ("07_compra_solicitud_presupuesto_p00001_duff_pdf.png", "Figura 7: Solicitud de Presupuesto P00001 para el proveedor Cervezas Duff solicitando el producto 'Cerveza Duff 0.0'."),
    "media_1793729681428_b05bf52e.png": ("08_compra_pedido_compra_p00001_duff_confirmado.png", "Figura 8: Confirmación del Pedido de Compra P00001 a Cervezas Duff y envío automático por correo electrónico."),
    "media_1793729464308_2bac51fc.png": ("09_ventas_pedido_s00001_factura_generada.png", "Figura 9: Pedido de venta S00001 confirmado para Barney Gumble con acceso directo a la Factura generada vinculada."),
    "media_1793729464290_b08fc864.png": ("10_tpv_productos_duff_pedido_5cervezas.png", "Figura 10: Terminal Punto de Venta (TPV) mostrando productos ilustrados y comanda de 5 Cervezas Duff 0.0."),
    "media_1793729464311_2c0017e2.png": ("11_tpv_ticket_recibo_pago_efectivo.png", "Figura 11: Ticket/Recibo oficial emitido por el TPV tras completar el cobro en efectivo con desglose de base imponible e IVA."),
    "media_1793729456813_82b8ebac.png": ("12_crm_oportunidad_barney_ganada.png", "Figura 12: Módulo CRM con el flujo comercial y la oportunidad ganada de Barney Gumble por importe de 100.000 €."),
    "media_1793714194720_94547698.png": ("13_backup_verificacion_bd_taverna.png", "Figura 13: Verificación de la base de datos 'taverna' y su propietario 'odoo' en PostgreSQL mediante docker exec."),
    "media_1793714522200_f149a06a.png": ("14_backup_pg_dump_26mb.png", "Figura 14: Extracción exitosa del dump de la base de datos con pg_dump generando un backup consistente de 26 MB."),
    "media_1793713212995_93250e00.png": ("15_backup_archivos_directorio_baks.png", "Figura 15: Directorio ./baks conteniendo el volcado SQL, odoo.conf y el tar.gz comprimido del filestore y sesiones."),
    "media_1793713584986_981917a7.png": ("16_migracion_compose_puerto_8070.png", "Figura 16: Modificación en docker-compose.yml mapeando el nuevo puerto 8070 y las nuevas rutas de persistencia."),
    "media_1793726986532_f41a4d35.png": ("17_migracion_restauracion_sql_exitosa.png", "Figura 17: Inyección del script SQL en la nueva base de datos y arranque del servicio PostgreSQL."),
    "media_1793727996650_3fdc95c7.png": ("18_migracion_verificacion_contenedores_up.png", "Figura 18: Verificación final con docker compose ps mostrando los servicios web y db activos en el puerto 8070.")
}

print("Copiando imágenes a la carpeta de capturas del repositorio...")
for src_name, (dest_name, _) in IMAGE_MAPPING.items():
    src_file = USER_UPLOADED_DIR / src_name
    dest_file = CAPTURES_DIR / dest_name
    if src_file.exists():
        shutil.copy2(src_file, dest_file)
        print(f"  OK: {dest_name}")
    else:
        print(f"  AVISO: No se encontró {src_name}")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Portada sin cabecera ni pie

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))

        # Cabecera
        self.drawString(54, A4[1] - 36, "SGE - UD04: Implantación y Migración de ERP/CRM (Odoo v18) | La Taberna de Moe")
        self.drawRightString(A4[0] - 54, A4[1] - 36, "2º DAM - Kevin")
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(54, A4[1] - 42, A4[0] - 54, A4[1] - 42)

        # Pie de página
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawString(54, 34, "Memoria Oficial de Prácticas | Repositorio GitHub Privado")
        self.drawRightString(A4[0] - 54, 34, page_str)
        self.line(54, 44, A4[0] - 54, 44)
        self.restoreState()

def create_memory_pdf():
    pdf_path = DEST_DIR / "Memoria_Practica_UD04_Kevin_Odoo.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#714B67") # Odoo purple
    dark_gray = colors.HexColor("#2C3E50")
    code_bg = colors.HexColor("#F8F9FA")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=primary_color,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=dark_gray,
        alignment=TA_CENTER
    )

    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=dark_gray,
        alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=dark_gray,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#222222"),
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )

    caption_style = ParagraphStyle(
        'CaptionCustom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#444444"),
        alignment=TA_CENTER,
        spaceBefore=3,
        spaceAfter=10
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1A252F")
    )

    story = []

    # ========================== PORTADA ==========================
    story.append(Spacer(1, 40))
    story.append(Paragraph("SISTEMAS DE GESTIÓN EMPRESARIAL", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("MEMORIA TÉCNICA DE IMPLANTACIÓN,<br/>PARAMETRIZACIÓN Y MIGRACIÓN ERP (ODOO v18)", title_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="60%", thickness=2, color=primary_color, spaceBefore=10, spaceAfter=15))
    story.append(Paragraph("<b>Supuesto Práctico: Despliegue de 'La Taberna de Moe'</b><br/>Unidad Didáctica 04: Implantación de un ERP en la Empresa con Contenedores Docker", subtitle_style))
    
    story.append(Spacer(1, 50))

    # Portada Metadata Table
    meta_data = [
        [Paragraph("<b>Alumno:</b>", meta_style), Paragraph("Kevin", meta_style)],
        [Paragraph("<b>Curso y Grupo:</b>", meta_style), Paragraph("2º DAM (Desarrollo de Aplicaciones Multiplataforma)", meta_style)],
        [Paragraph("<b>Módulo Profesional:</b>", meta_style), Paragraph("Sistemas de Gestión Empresarial (SGE)", meta_style)],
        [Paragraph("<b>Entorno Tecnológico:</b>", meta_style), Paragraph("Debian GNU/Linux 12 (VM), Docker & Docker Compose, Odoo v18, PostgreSQL 15", meta_style)],
        [Paragraph("<b>Repositorio GitHub:</b>", meta_style), Paragraph("Privado | Curso-Dam2 / Sistema gestion empresarial / UD04", meta_style)],
        [Paragraph("<b>Fecha de Ejecución:</b>", meta_style), Paragraph("Noviembre 2026", meta_style)]
    ]
    meta_table = Table(meta_data, colWidths=[150, 310])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#DDDDDD")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EAEAEA")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 40))
    story.append(Paragraph("<i>Documento técnico de entrega con evidencias gráficas, comandos de despliegue, configuración modular y procedimiento completo de migración y backup con persistencia de datos.</i>", caption_style))
    story.append(PageBreak())

    # Helper para insertar imágenes ajustadas
    def add_figure(img_filename, caption_text, max_h=230):
        img_path = CAPTURES_DIR / img_filename
        if not img_path.exists():
            return
        
        with Image.open(img_path) as im:
            orig_w, orig_h = im.size

        avail_w = 480
        scale = min(avail_w / orig_w, max_h / orig_h)
        target_w = orig_w * scale
        target_h = orig_h * scale

        flowables = [
            Spacer(1, 4),
            RLImage(str(img_path), width=target_w, height=target_h),
            Paragraph(caption_text, caption_style),
            Spacer(1, 4)
        ]
        story.append(KeepTogether(flowables))

    def add_code(text):
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
        p = Paragraph(f"<font face='Courier'>{escaped}</font>", code_style)
        t = Table([[p]], colWidths=[490])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), code_bg),
            ('BOX', (0,0), (-1,-1), 0.7, colors.HexColor("#CCCCCC")),
            ('PADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(KeepTogether([Spacer(1, 3), t, Spacer(1, 5)]))

    # ========================== SECCIÓN 1 ==========================
    story.append(Paragraph("1. Introducción y Configuración Corporativa de la Empresa", h1_style))
    story.append(Paragraph(
        "En esta práctica se lleva a cabo el despliegue e implantación modular del sistema ERP Odoo v18 sobre una máquina virtual Debian mediante orquestación de contenedores Docker. El caso de estudio simula la operativa integral de <b>'La Taberna de Moe'</b>, un establecimiento de hostelería que requiere automatizar sus compras, stock, facturación comercial, ventas por Punto de Venta (TPV), gestión laboral de empleados y ciclo CRM.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Datos fiscales y localización:</b> Se configuró la empresa con domicilio fiscal en España (Calle del Doctor Fleming, 5), plan general contable español y régimen impositivo general de IVA al 21%. Se vinculó el logotipo oficial obtenido a través de recursos de Los Simpson.",
        body_style
    ))
    add_figure("01_datos_empresa_login_8070.png", "Figura 1: Pantalla de inicio de sesión con el logotipo corporativo de 'La Taberna de Moe' y acceso verificado.")

    # ========================== SECCIÓN 2 ==========================
    story.append(Paragraph("2. Módulos de Facturación, Clientes y Proveedores", h1_style))
    story.append(Paragraph(
        "Se activaron los módulos de Facturación y Conversaciones. Se dio de alta al cliente habitual <b>Barney Gumble</b> y al proveedor estratégico <b>Cervezas Duff</b>. Para corroborar la correcta localización española y cálculo de retenciones e IVA (21%), se emitió y liquidó la factura <code>INV/2024/00001</code> correspondiente a 1.000 unidades de Cerveza Duff (base 500,00 €, IVA 105,00 €, Total 605,00 €), quedando en estado completamente <b>PAGADO</b>.",
        body_style
    ))
    add_figure("03_factura_barney_inv202400001_pagada.png", "Figura 2: Factura de cliente INV/2024/00001 pagada y conciliada con desglose impositivo reglamentario.")
    add_figure("04_facturacion_listado_facturas.png", "Figura 3: Vista centralizada del libro de Facturas de Clientes emitidas en el ERP.")

    # ========================== SECCIÓN 3 ==========================
    story.append(Paragraph("3. Gestión de Recursos Humanos: Departamentos y Empleados", h1_style))
    story.append(Paragraph(
        "A través del módulo <code>hr</code> (Empleados), se estructuró el organigrama de la taberna definiendo los departamentos de <b>Ventas</b> y <b>Administración</b>. Posteriormente se dieron de alta las fichas de personal con imagen identificativa y cuenta de usuario vinculada (<code>res_users</code>):",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Lurleen Lumpkin:</b> Puesto de Camarera, asignada al departamento de <b>Ventas</b>.<br/>"
        "• <b>Waylon Smithers:</b> Puesto de Contable, asignado al departamento de <b>Administración</b>.",
        body_style
    ))
    add_figure("05_empleados_lurleen_lumpkin_ventas.png", "Figura 4: Ficha de personal de Lurleen Lumpkin integrada en el departamento de Ventas.")
    add_figure("06_empleados_waylon_smithers_administracion.png", "Figura 5: Ficha de personal de Waylon Smithers asignado al departamento de Administración.")

    # ========================== SECCIÓN 4 ==========================
    story.append(Paragraph("4. Gestión de Aprovisionamiento y Compras (Cervezas Duff)", h1_style))
    story.append(Paragraph(
        "Se procedió a la instalación del módulo de <b>Compras</b> (<code>purchase</code>) para gestionar los pedidos a proveedores. Se registró el artículo <b>'Cerveza Duff 0.0'</b> y se generó la <b>Solicitud de Presupuesto P00001</b> a nombre del proveedor <i>Cervezas Duff</i>. A continuación, se confirmó convirtiéndose formalmente en <b>Pedido de Compra</b> con emisión de documento PDF y envío telemático por correo.",
        body_style
    ))
    add_figure("07_compra_solicitud_presupuesto_p00001_duff_pdf.png", "Figura 6: Documento oficial en PDF de la Solicitud de Presupuesto P00001 a Cervezas Duff.")
    add_figure("08_compra_pedido_compra_p00001_duff_confirmado.png", "Figura 7: Pedido de compra P00001 confirmado y ventana modal para notificación de email al proveedor.")

    # ========================== SECCIÓN 5 ==========================
    story.append(Paragraph("5. Circuito Comercial de Ventas y Facturación a Clientes", h1_style))
    story.append(Paragraph(
        "Mediante el módulo de <b>Ventas</b> (<code>sale_management</code>), se elaboró el <b>Presupuesto formal #S00001</b> para Barney Gumble pidiendo una ronda de cervezas. Tras la aceptación del cliente, se confirmó el pedido y se procesó la generación automática de su correspondiente factura comercial.",
        body_style
    ))
    add_figure("02_presupuesto_s00001_barney_pdf.png", "Figura 8: Presupuesto oficial en PDF #S00001 emitido a Barney Gumble con membrete e impuestos.")
    add_figure("09_ventas_pedido_s00001_factura_generada.png", "Figura 9: Pedido de venta S00001 confirmado con acceso directo al botón inteligente de Factura vinculada.")

    # ========================== SECCIÓN 6 ==========================
    story.append(Paragraph("6. Terminal Punto de Venta (TPV / POS) y Expedición de Tickets", h1_style))
    story.append(Paragraph(
        "Para agilizar el despacho de barra de la taberna, se implantó el módulo <b>Punto de Venta</b> (<code>point_of_sale</code>). Se habilitaron los artículos con fotografía corporativa (Cerveza Duff y Cerveza Duff 0.0). Durante la sesión de caja, se atendió una comanda de <b>5 unidades de Cerveza Duff 0.0</b>, procesándose el cobro en efectivo y emitiéndose el ticket simplificado correspondiente.",
        body_style
    ))
    add_figure("10_tpv_productos_duff_pedido_5cervezas.png", "Figura 10: Interfaz táctil del TPV con comanda activa de 5 unidades de Cerveza Duff 0.0.")
    add_figure("11_tpv_ticket_recibo_pago_efectivo.png", "Figura 11: Ticket oficial impreso por el TPV reflejando pago exitoso en efectivo y desglose de IVA.")

    # ========================== SECCIÓN 7 ==========================
    story.append(Paragraph("7. Módulo Adicional Especializado: CRM y Pipeline Comercial", h1_style))
    story.append(Paragraph(
        "Como módulo complementario dentro de la selección de módulos de interés empresarial, se instaló y configuró el sistema de <b>Gestión de Relaciones con Clientes (CRM)</b>. Se creó una oportunidad de negocio asociada a Barney Gumble por valor de 100.000,00 €, logrando avanzar su ciclo de cualificación por el embudo de ventas hasta marcarla como <b>Ganado</b>.",
        body_style
    ))
    add_figure("12_crm_oportunidad_barney_ganada.png", "Figura 12: Embudo de ventas del módulo CRM con oportunidad comercial en estado 'Ganado'.")

    # ========================== SECCIÓN 8 ==========================
    story.append(PageBreak())
    story.append(Paragraph("8. Procedimiento Técnico de Copia de Seguridad (Backup)", h1_style))
    story.append(Paragraph(
        "Siguiendo estrictamente las pautas de persistencia en Odoo y PostgreSQL, se procedió a realizar un respaldo consistente en frío de los 3 pilares del ERP: la Base de Datos relacional, la configuración del servicio y los ficheros multimedia/sesiones.",
        body_style
    ))
    story.append(Paragraph("<b>Paso 8.1: Comprobación del nombre de la base de datos y espacio disponible</b>", h2_style))
    story.append(Paragraph(
        "Se ejecutó una consulta sobre el motor PostgreSQL para corroborar el nombre exacto de la base de datos de producción (<code>taverna</code>) y su usuario propietario (<code>odoo</code>):",
        body_style
    ))
    add_code("docker compose exec db psql -U odoo -l\ndf -h")
    add_figure("13_backup_verificacion_bd_taverna.png", "Figura 13: Salida de psql verificando la existencia de la base de datos 'taverna' propiedad de 'odoo'.")

    story.append(Paragraph("<b>Paso 8.2: Volcado relacional con pg_dump y empaquetado de assets</b>", h2_style))
    story.append(Paragraph(
        "Con el contenedor web temporalmente detenido para evitar escrituras concurrentes, se extrajo el dump SQL completo de la base de datos (alcanzando 26 MB de datos relacionales reales) y se respaldaron la configuración y el filestore:",
        body_style
    ))
    add_code(
        "# 1. Volcado completo de la base de datos relacional (26 MB)\n"
        "docker compose exec -T db pg_dump -U odoo taverna > ./baks/backup_bd.sql\n\n"
        "# 2. Respaldo de la configuracion de Odoo\n"
        "docker cp odood-web-1:/etc/odoo/odoo.conf ./baks/odoo.conf\n\n"
        "# 3. Empaquetado comprimido del filestore y sesiones (6.3 MB)\n"
        "tar -czvf ./baks/odoo_data_backup.tar.gz -C ./volumesOdoo_NUEVO/odoo filestore sessions"
    )
    add_figure("14_backup_pg_dump_26mb.png", "Figura 14: Verificación en terminal del volcado consistente de 26 Megabytes en backup_bd.sql.")
    add_figure("15_backup_archivos_directorio_baks.png", "Figura 15: Directorio ./baks con los tres archivos íntegros de respaldo.")

    # ========================== SECCIÓN 9 ==========================
    story.append(Paragraph("9. Simulación de Migración Geográfica a Nuevo Host / Puerto", h1_style))
    story.append(Paragraph(
        "Para simular la migración de Odoo a una nueva ubicación o servidor anfitrión, se modificó el archivo de orquestación <code>docker-compose.yml</code> redirigiendo los volúmenes persistentes a nuevas rutas (<code>./volumesOdoo_Nuevo</code>) y reasignando el puerto de acceso anfitrión al <b>8070</b> (<code>8070:8069</code>).",
        body_style
    ))
    add_code(
        "# Fragmento de docker-compose.yml adaptado para la migracion:\n"
        "services:\n"
        "  web:\n"
        "    image: odoo:18\n"
        "    ports:\n"
        "      - \"8070:8069\"  # Nuevo puerto de servicio migrado\n"
        "    volumes:\n"
        "      - ./volumesOdoo_Nuevo/addons:/mnt/extra-addons\n"
        "      - ./volumesOdoo_Nuevo/odoo/filestore:/var/lib/odoo/filestore\n"
        "      - ./volumesOdoo_Nuevo/odoo/sessions:/var/lib/odoo/sessions\n"
        "  db:\n"
        "    image: postgres:15\n"
        "    volumes:\n"
        "      - ./volumesOdoo_Nuevo/dataPostgreSQL:/var/lib/postgresql/data"
    )
    add_figure("16_migracion_compose_puerto_8070.png", "Figura 16: Mapeo de puertos 8070:8069 en el fichero de despliegue docker-compose.yml.")

    story.append(Paragraph("<b>Paso 9.1: Restauración de base de datos e inyección de datos</b>", h2_style))
    story.append(Paragraph(
        "Se levantó de forma aislada el servicio de base de datos, se creó la base de datos limpia con el propietario original y se inyectó el script SQL:",
        body_style
    ))
    add_code(
        "# 1. Arrancar el motor de base de datos limpio\n"
        "docker compose up -d db\n\n"
        "# 2. Crear la base de datos 'taverna' con propietario 'odoo'\n"
        "docker compose exec -T db psql -U odoo -d postgres -c \"CREATE DATABASE taverna OWNER odoo;\"\n\n"
        "# 3. Inyectar el volcado relacional\n"
        "cat ./baks/backup_bd.sql | docker compose exec -T db psql -U odoo -d taverna"
    )
    add_figure("17_migracion_restauracion_sql_exitosa.png", "Figura 17: Inyección SQL finalizada con éxito mediante sentencias ALTER TABLE y GRANT.")

    story.append(Paragraph("<b>Paso 9.2: Descompresión de filestore, arranque y verificación</b>", h2_style))
    story.append(Paragraph(
        "Se restauraron los ficheros multimedia en la nueva estructura de volúmenes y se inició el conjunto de contenedores con <code>docker compose up -d</code>, comprobando que ambos contenedores operaban con normalidad:",
        body_style
    ))
    add_code(
        "# Descomprimir filestore en la nueva ruta\n"
        "sudo tar -xzvf ./baks/odoo_data_backup.tar.gz -C ./volumesOdoo_Nuevo/odoo/\n\n"
        "# Arrancar el stack completo\n"
        "docker compose up -d\n\n"
        "# Comprobar estado de los servicios\n"
        "docker compose ps"
    )
    add_figure("18_migracion_verificacion_contenedores_up.png", "Figura 18: Comando docker compose ps confirmando ambos contenedores Up en el puerto 8070.")

    # ========================== SECCIÓN 10 ==========================
    story.append(Paragraph("10. Comprobación Final en Navegador y Conclusiones", h1_style))
    story.append(Paragraph(
        "Se accedió a la nueva dirección web <b><code>http://localhost:8070</code></b>. Se constató que el sistema conservaba la totalidad de los datos empresariales: catálogo de artículos con imágenes, perfiles de personal en sus departamentos respectivos, facturas emitidas, oportunidades del CRM y sesiones del TPV, validando el éxito íntegro de la migración y la solidez del esquema de persistencia.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Buenas prácticas de control de versiones (Git):</b> De acuerdo con las instrucciones de la asignatura, el repositorio se mantuvo en modo privado realizando commits parciales y descriptivos por cada fase de trabajo, estructurando el proyecto con documentación complementaria en formato Markdown (README) y preservando los scripts de orquestación necesarios para reproducir el despliegue en cualquier equipo anfitrión.",
        body_style
    ))

    # Construir documento
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"\n¡PDF generado exitosamente en: {pdf_path}!")

if __name__ == "__main__":
    create_memory_pdf()
