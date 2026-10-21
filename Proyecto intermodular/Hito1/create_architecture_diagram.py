import os
from PIL import Image, ImageDraw, ImageFont

def create_architecture_diagram(output_path):
    width, height = 1200, 680
    im = Image.new("RGBA", (width, height), (248, 250, 252, 255)) # #F8FAFC
    draw = ImageDraw.Draw(im)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 24)
        font_box_title = ImageFont.truetype("arialbd.ttf", 16)
        font_text = ImageFont.truetype("arial.ttf", 13)
        font_badge = ImageFont.truetype("arialbd.ttf", 11)
    except:
        font_title = font_box_title = font_text = font_badge = ImageFont.load_default()

    # Header Bar
    draw.rectangle([(0, 0), (width, 60)], fill=(10, 25, 47, 255))
    draw.text((40, 18), "ARQUITECTURA DE COMPONENTES • LEADCRAFT AI", fill=(0, 210, 180, 255), font=font_title)

    # Layers / Sections:
    # 1. CLIENT LAYER (Frontend)
    # 2. APPLICATION / BACKEND LAYER (FastAPI API Gateway)
    # 3. CORE PROCESSING ENGINES (Maps/Auditor, AI Engine, CRM)
    # 4. DATA & STORAGE LAYER (DB, Templates, Cloud Hosting)

    # 1. CLIENT LAYER
    draw.rounded_rectangle([(40, 90), (320, 310)], radius=12, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=2)
    draw.rounded_rectangle([(40, 90), (320, 130)], radius=12, fill=(13, 110, 253, 255))
    draw.rectangle([(40, 120), (320, 130)], fill=(13, 110, 253, 255))
    draw.text((60, 100), "1. CAPA CLIENTE (FRONTEND)", fill=(255, 255, 255, 255), font=font_box_title)

    frontend_items = [
        "• Dashboard en Flutter / Web Desktop",
        "• Visualizador interactivo de Google Maps",
        "• Panel de Auditoría Digital Express",
        "• Editor & Previsualizador Web en vivo",
        "• Tablero Kanban CRM (Gestión de Leads)"
    ]
    y = 150
    for item in frontend_items:
        draw.text((55, y), item, fill=(30, 41, 59, 255), font=font_text)
        y += 28

    # 2. BACKEND API GATEWAY
    draw.rounded_rectangle([(360, 90), (740, 310)], radius=12, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=2)
    draw.rounded_rectangle([(360, 90), (740, 130)], radius=12, fill=(10, 37, 64, 255))
    draw.rectangle([(360, 120), (740, 130)], fill=(10, 37, 64, 255))
    draw.text((380, 100), "2. SERVICIOS Y PROCESOS (BACKEND)", fill=(255, 255, 255, 255), font=font_box_title)

    backend_items = [
        "• API REST Gateway (FastAPI / Python)",
        "• Router de Prospección Geográfica",
        "• Orquestador Asíncrono de Auditorías",
        "• Gestor de Solicitudes y Cuotas de IA",
        "• Autenticación y Control de Accesos JWT"
    ]
    y = 150
    for item in backend_items:
        draw.text((375, y), item, fill=(30, 41, 59, 255), font=font_text)
        y += 28

    # 3. EXTERNAL APIS & INTEGRATIONS
    draw.rounded_rectangle([(780, 90), (1160, 310)], radius=12, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=2)
    draw.rounded_rectangle([(780, 90), (1160, 130)], radius=12, fill=(0, 180, 150, 255))
    draw.rectangle([(780, 120), (1160, 130)], fill=(0, 180, 150, 255))
    draw.text((800, 100), "3. INTEGRACIONES & APIS EXTERNAS", fill=(255, 255, 255, 255), font=font_box_title)

    ext_items = [
        "• Google Places API (Datos & Reseñas)",
        "• Scraper Engine (Detección web/citas)",
        "• LLM Engine (Google Gemini / OpenAI)",
        "• WhatsApp Business API / Click-to-Chat",
        "• Motor de Render HTML / PDF (ReportLab)"
    ]
    y = 150
    for item in ext_items:
        draw.text((795, y), item, fill=(30, 41, 59, 255), font=font_text)
        y += 28

    # Arrows connecting layers
    draw.line([(320, 200), (360, 200)], fill=(0, 180, 150, 255), width=3)
    draw.polygon([(358, 195), (368, 200), (358, 205)], fill=(0, 180, 150, 255))

    draw.line([(740, 200), (780, 200)], fill=(0, 180, 150, 255), width=3)
    draw.polygon([(778, 195), (788, 200), (778, 205)], fill=(0, 180, 150, 255))

    # BOTTOM: DATA, TEMPLATES & STORAGE LAYER
    draw.rounded_rectangle([(40, 360), (1160, 630)], radius=12, fill=(255, 255, 255, 255), outline=(203, 213, 225, 255), width=2)
    draw.rounded_rectangle([(40, 360), (1160, 400)], radius=12, fill=(71, 85, 105, 255))
    draw.rectangle([(40, 390), (1160, 400)], fill=(71, 85, 105, 255))
    draw.text((60, 370), "4. CAPA DE DATOS, PLANTILLAS Y PERSISTENCIA (ACCESO A DATOS)", fill=(255, 255, 255, 255), font=font_box_title)

    # Subcolumns in storage layer
    cols_data = [
        ("Base de Datos Relacional", [
            "• PostgreSQL / SQLite con SQLAlchemy",
            "• Tabla de Negocios y Ubicaciones",
            "• Tabla de Auditorías y Carencias",
            "• Tabla de Leads y Estados del CRM"
        ]),
        ("Catálogo de Plantillas Web", [
            "• Plantilla Hostelería (Menú digital)",
            "• Plantilla Servicios (Citas/Reservas)",
            "• Plantilla Comercio (Catálogo básico)",
            "• Componentes Tailwind CSS responsive"
        ]),
        ("Almacenamiento & Exportación", [
            "• Repositorio de Webs Generadas (HTML/JS)",
            "• Informes de Auditoría en PDF descargables",
            "• Paquetes ZIP listos para alojar",
            "• Cloud Hosting / GitHub Pages deployer"
        ])
    ]

    cx = 60
    for col_title, col_lines in cols_data:
        draw.rounded_rectangle([(cx, 420), (cx + 340, 610)], radius=8, fill=(241, 245, 249, 255))
        draw.text((cx + 15, 430), col_title, fill=(10, 37, 64, 255), font=font_box_title)
        cy = 465
        for line in col_lines:
            draw.text((cx + 15, cy), line, fill=(51, 65, 85, 255), font=font_text)
            cy += 26
        cx += 370

    # Downward connection arrows
    draw.line([(550, 310), (550, 360)], fill=(13, 110, 253, 255), width=3)
    draw.polygon([(545, 355), (550, 365), (555, 355)], fill=(13, 110, 253, 255))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path, "PNG")
    print(f"Architecture diagram saved at: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Users\kevin\OneDrive\Documentos\GitHub\Curso-Dam2\Proyecto intermodular\Hito1"
    create_architecture_diagram(os.path.join(out_dir, "diagrama_arquitectura_leadcraft.png"))
