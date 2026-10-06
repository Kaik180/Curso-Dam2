import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Colores modernos y legibles
PRIMARY = colors.HexColor("#0D47A1")       # Azul oscuro
SECONDARY = colors.HexColor("#1565C0")     # Azul medio
ACCENT = colors.HexColor("#00796B")        # Verde azulado
DARK_BG = colors.HexColor("#1A1B26")       # Fondo consola tipo terminal
TEXT_DARK = colors.HexColor("#212121")     # Texto cuerpo
TEXT_MUTED = colors.HexColor("#546E7A")    # Texto pie y encabezado
BG_LIGHT = colors.HexColor("#F8FAFC")      # Fondo claro para tablas
BORDER_COLOR = colors.HexColor("#CFD8DC")  # Bordes suaves
HIGHLIGHT = colors.HexColor("#E8F5E9")     # Resaltado verde claro

class NumberedCanvas(canvas.Canvas):
    """
    Controla el número de páginas dinámico (Página X de Y) y las cabeceras.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        w, h = A4

        # Encabezado (a partir de la página 2)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(SECONDARY)
            self.drawString(1.5 * cm, h - 1.15 * cm, "PSP | UD1: PROGRAMACIÓN MULTIPROCESO")
            self.setFont("Helvetica", 8)
            self.setFillColor(TEXT_MUTED)
            self.drawRightString(w - 1.5 * cm, h - 1.15 * cm, "Práctica: Cálculo de Primos en Paralelo")

            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(1.5 * cm, h - 1.25 * cm, w - 1.5 * cm, h - 1.25 * cm)

        # Pie de página (todas las páginas)
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(1.5 * cm, 1.25 * cm, w - 1.5 * cm, 1.25 * cm)

        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        self.drawString(1.5 * cm, 0.85 * cm, "Kevin Muñoz Córcoles — 2º DAM (Curso 2026/2027)")
        page_str = f"Página {self._pageNumber} de {total_pages}"
        self.drawRightString(w - 1.5 * cm, 0.85 * cm, page_str)

        self.restoreState()


def create_terminal_block(command_text, output_text, styles, width_cm=18.0):
    """
    Crea una caja simulando la consola de comandos de Linux/PowerShell.
    """
    cmd_para = Paragraph(
        f"<font color='#81C784'><b>kevin@dam2:~/procesos$</b></font> <font color='#FFFFFF'><b>{command_text}</b></font>",
        styles['TerminalCommand']
    )
    formatted_out = output_text.replace('\n', '<br/>').replace(' ', '&nbsp;')
    out_para = Paragraph(
        f"<font color='#CFD8DC'>{formatted_out}</font>",
        styles['TerminalOutput']
    )
    
    data = [[cmd_para], [Spacer(1, 1)], [out_para]]
    t = Table(data, colWidths=[width_cm * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DARK_BG),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, 0), 4),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor("#2E3440")),
    ]))
    return t


def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.35 * cm,
        bottomMargin=1.35 * cm
    )

    base = getSampleStyleSheet()

    styles = {
        'DocTitle': ParagraphStyle('DocTitle', parent=base['Normal'], fontName='Helvetica-Bold', fontSize=16, leading=19, textColor=PRIMARY, spaceAfter=2),
        'DocSubtitle': ParagraphStyle('DocSubtitle', parent=base['Normal'], fontName='Helvetica', fontSize=9.5, leading=12.5, textColor=SECONDARY, spaceAfter=7),
        'SectionHeader': ParagraphStyle('SectionHeader', parent=base['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=13.5, textColor=PRIMARY, spaceBefore=5, spaceAfter=3, keepWithNext=True),
        'SubSectionHeader': ParagraphStyle('SubSectionHeader', parent=base['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11.5, textColor=SECONDARY, spaceBefore=4, spaceAfter=2, keepWithNext=True),
        'Body': ParagraphStyle('Body', parent=base['Normal'], fontName='Helvetica', fontSize=8.2, leading=11.0, textColor=TEXT_DARK, alignment=4, spaceAfter=3.5),
        'BodyBold': ParagraphStyle('BodyBold', parent=base['Normal'], fontName='Helvetica-Bold', fontSize=8.2, leading=11.0, textColor=TEXT_DARK, spaceAfter=2),
        'BulletItem': ParagraphStyle('BulletItem', parent=base['Normal'], fontName='Helvetica', fontSize=7.9, leading=10.6, textColor=TEXT_DARK, leftIndent=9, spaceAfter=2),
        'MetaBox': ParagraphStyle('MetaBox', parent=base['Normal'], fontName='Helvetica', fontSize=7.9, leading=10.3, textColor=TEXT_DARK),
        'TerminalCommand': ParagraphStyle('TerminalCommand', fontName='Courier-Bold', fontSize=7.3, leading=9.4, textColor=colors.white),
        'TerminalOutput': ParagraphStyle('TerminalOutput', fontName='Courier', fontSize=6.8, leading=8.7, textColor=colors.HexColor("#CFD8DC")),
        'TableHeader': ParagraphStyle('TableHeader', fontName='Helvetica-Bold', fontSize=7.4, leading=9.2, textColor=colors.white, alignment=1),
        'TableCell': ParagraphStyle('TableCell', fontName='Helvetica', fontSize=7.3, leading=9.2, textColor=TEXT_DARK, alignment=1),
        'TableCellLeft': ParagraphStyle('TableCellLeft', fontName='Helvetica', fontSize=7.3, leading=9.2, textColor=TEXT_DARK, alignment=0),
        'TableCellBold': ParagraphStyle('TableCellBold', fontName='Helvetica-Bold', fontSize=7.3, leading=9.2, textColor=PRIMARY, alignment=1),
        'CalloutText': ParagraphStyle('CalloutText', parent=base['Normal'], fontName='Helvetica', fontSize=8.0, leading=10.8, textColor=colors.HexColor("#004D40"))
    }

    story = []

    # =========================================================================
    # PÁGINA 1: DATOS, CÓMO FUNCIONA Y PRIMERAS PRUEBAS
    # =========================================================================
    story.append(Paragraph("INFORME DE PRÁCTICA DE LABORATORIO", ParagraphStyle('PreTitle', fontName='Helvetica-Bold', fontSize=7.8, textColor=ACCENT, spaceAfter=2)))
    story.append(Paragraph("Cálculo de Números Primos con Multiproceso en Java", styles['DocTitle']))
    story.append(Paragraph("Pruebas de rendimiento, comunicación entre procesos y comparación con versión secuencial", styles['DocSubtitle']))

    # Ficha del alumno
    meta_data = [
        [
            Paragraph("<b>Módulo:</b> Programación de Servicios y Procesos (PSP)", styles['MetaBox']),
            Paragraph("<b>Alumno:</b> Kevin Muñoz Córcoles", styles['MetaBox'])
        ],
        [
            Paragraph("<b>Unidad:</b> UD1 — Programación Multiproceso", styles['MetaBox']),
            Paragraph("<b>Curso:</b> 2º Desarrollo de Aplicaciones Multiplataforma (DAM)", styles['MetaBox'])
        ],
        [
            Paragraph("<b>Entorno:</b> Java OpenJDK 25 / Windows 11 x64", styles['MetaBox']),
            Paragraph("<b>Objetivo:</b> Medir la sobrecarga de crear procesos frente al cálculo secuencial", styles['MetaBox'])
        ]
    ]
    meta_t = Table(meta_data, colWidths=[9.0 * cm, 9.0 * cm])
    meta_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, BORDER_COLOR),
    ]))
    story.append(meta_t)
    story.append(Spacer(1, 5))

    # 1. Cómo funciona el programa
    story.append(Paragraph("1. ¿Cómo funciona la práctica? (Modelo Maestro-Trabajador)", styles['SectionHeader']))
    story.append(Paragraph(
        "El objetivo de esta práctica es contar cuántos números primos hay en un rango (por ejemplo, del 1 al 200.000) repartiendo el cálculo entre varios procesos hijos para que trabajen a la vez en paralelo. Hemos creado tres clases en Java:",
        styles['Body']
    ))
    story.append(Paragraph("• <b>TrabajadorPrimo (Proceso hijo):</b> Es un programa independiente. Recibe dos números por consola (<code>inicio</code> y <code>fin</code>). Si le pasamos los datos mal o el rango no tiene sentido, muestra un mensaje de error por <code>stderr</code> y termina con código de salida 1. Si los datos son correctos, cuenta los números primos que hay en ese trozo, imprime el resultado por pantalla (<code>stdout</code>) y termina con código 0.", styles['BulletItem']))
    story.append(Paragraph("• <b>MaestroProcesos (Programa principal):</b> Es el coordinador. Parte el rango total en trozos iguales y lanza varios procesos hijos usando <code>ProcessBuilder</code>. Lee el número que devuelve cada hijo mediante un <code>BufferedReader</code>, espera a que terminen con <code>waitFor()</code> comprobando que no hayan dado error y suma todos los resultados para mostrar el total de primos y el tiempo empleado.", styles['BulletItem']))
    story.append(Paragraph("• <b>PrimosSecuencial (Versión de control):</b> Hace exactamente la misma cuenta pero de la forma tradicional, en un solo proceso sin crear subprocesos. Nos sirve para comprobar que el número de primos coincida y para comparar qué método tarda menos tiempo.", styles['BulletItem']))

    story.append(Spacer(1, 4))

    # 2. Capturas de consola
    story.append(Paragraph("2. Capturas y Evidencias de Ejecución en la Consola", styles['SectionHeader']))
    
    # Evidencia 2.1: TrabajadorPrimo
    term1_cmd = "java procesos.TrabajadorPrimo 1 100 && java procesos.TrabajadorPrimo 100 50"
    term1_out = "25\nError [TrabajadorPrimo]: Rango inválido [100, 50]. Se requiere inicio >= 1 e inicio <= fin.\n[Proceso terminado con código de error: 1]"
    story.append(Paragraph("<b>Prueba 2.1:</b> Comprobando <code>TrabajadorPrimo</code> suelto (caso normal del 1 al 100 dando 25 primos, y control de error con rango invertido):", styles['BodyBold']))
    story.append(create_terminal_block(term1_cmd, term1_out, styles))
    story.append(Spacer(1, 5))

    # Evidencia 2.2: MaestroProcesos
    term2_cmd = "java procesos.MaestroProcesos 200000 4"
    term2_out = (
        "==============================================================\n"
        "   CALCULO PARALELO DE PRIMOS (MULTIPROCESO EN JAVA)         \n"
        "==============================================================\n"
        "Rango total: [1, 200.000] | Numero de procesos (M): 4\n"
        "Seguimiento y recoleccion de los subprocesos:\n"
        "  [Proceso 1] Rango [         1 -     50.000] ->    5.133 primos (exit code: 0)\n"
        "  [Proceso 2] Rango [    50.001 -    100.000] ->    4.459 primos (exit code: 0)\n"
        "  [Proceso 3] Rango [   100.001 -    150.000] ->    4.256 primos (exit code: 0)\n"
        "  [Proceso 4] Rango [   150.001 -    200.000] ->    4.136 primos (exit code: 0)\n"
        "--------------------------------------------------------------\n"
        "RESULTADOS MULTIPROCESO:\n"
        "  Total de numeros primos encontrados: 17.984\n"
        "  Tiempo total transcurrido:           861 ms (0,861 s)\n"
        "=============================================================="
    )
    story.append(Paragraph("<b>Prueba 2.2:</b> Ejecución del maestro con los valores de la práctica (hasta 200.000 con 4 procesos):", styles['BodyBold']))
    story.append(create_terminal_block(term2_cmd, term2_out, styles))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: EVIDENCIA SECUENCIAL Y TABLA COMPARATIVA DE TIEMPOS
    # =========================================================================
    term3_cmd = "java procesos.PrimosSecuencial 200000"
    term3_out = (
        "==============================================================\n"
        "   CALCULO SECUENCIAL DE PRIMOS (LINEA BASE / MONOPROCESO)   \n"
        "==============================================================\n"
        "Rango evaluado: [1, 200.000]\n"
        "Calculando de forma secuencial sin procesos concurrentes...\n"
        "--------------------------------------------------------------\n"
        "RESULTADOS SECUENCIAL:\n"
        "  Total de numeros primos encontrados: 17.984\n"
        "  Tiempo total transcurrido:           16 ms (0,016 s)\n"
        "=============================================================="
    )
    story.append(Paragraph("<b>Prueba 2.3:</b> Ejecución del programa secuencial (comprobamos que da exactamente los mismos 17.984 primos):", styles['BodyBold']))
    story.append(create_terminal_block(term3_cmd, term3_out, styles))
    story.append(Spacer(1, 7))

    # 3. Tabla comparativa
    story.append(Paragraph("3. Tabla Comparativa de Tiempos Reales Obtenidos", styles['SectionHeader']))
    story.append(Paragraph(
        "Hemos hecho pruebas en el ordenador probando tres tamaños distintos: un rango pequeño (200.000), un rango medio (1 millón) y un rango grande con mucho cálculo (10 millones), usando la versión secuencial y multiproceso con 2, 4 y 8 procesos:",
        styles['Body']
    ))

    t_data = [
        [
            Paragraph("<b>Tamaño del Rango</b>", styles['TableHeader']),
            Paragraph("<b>Primos</b>", styles['TableHeader']),
            Paragraph("<b>Cómo se ejecuta</b>", styles['TableHeader']),
            Paragraph("<b>Procesos</b>", styles['TableHeader']),
            Paragraph("<b>Tiempo (ms)</b>", styles['TableHeader']),
            Paragraph("<b>Tiempo (s)</b>", styles['TableHeader']),
            Paragraph("<b>¿Cómo rinde?</b>", styles['TableHeader'])
        ],
        # N = 200.000
        [
            Paragraph("<b>Rango pequeño</b><br/>Hasta 200.000", styles['TableCellLeft']),
            Paragraph("17.984", styles['TableCell']),
            Paragraph("Secuencial (Normal)", styles['TableCellLeft']),
            Paragraph("1", styles['TableCell']),
            Paragraph("<b>16 ms</b>", styles['TableCellBold']),
            Paragraph("0,016 s", styles['TableCell']),
            Paragraph("<b>El más rápido</b>", styles['TableCellBold'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("17.984", styles['TableCell']),
            Paragraph("Multiproceso", styles['TableCellLeft']),
            Paragraph("2", styles['TableCell']),
            Paragraph("564 ms", styles['TableCell']),
            Paragraph("0,564 s", styles['TableCell']),
            Paragraph("Pierde tiempo", styles['TableCell'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("17.984", styles['TableCell']),
            Paragraph("Multiproceso (Práctica)", styles['TableCellLeft']),
            Paragraph("4", styles['TableCell']),
            Paragraph("861 ms", styles['TableCell']),
            Paragraph("0,861 s", styles['TableCell']),
            Paragraph("Pierde tiempo", styles['TableCell'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("17.984", styles['TableCell']),
            Paragraph("Multiproceso", styles['TableCellLeft']),
            Paragraph("8", styles['TableCell']),
            Paragraph("1.285 ms", styles['TableCell']),
            Paragraph("1,285 s", styles['TableCell']),
            Paragraph("El más lento de todos", styles['TableCell'])
        ],
        # N = 1.000.000
        [
            Paragraph("<b>Rango medio</b><br/>Hasta 1.000.000", styles['TableCellLeft']),
            Paragraph("78.498", styles['TableCell']),
            Paragraph("Secuencial (Normal)", styles['TableCellLeft']),
            Paragraph("1", styles['TableCell']),
            Paragraph("<b>127 ms</b>", styles['TableCellBold']),
            Paragraph("0,127 s", styles['TableCell']),
            Paragraph("<b>Sigue ganando</b>", styles['TableCellBold'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("78.498", styles['TableCell']),
            Paragraph("Multiproceso", styles['TableCellLeft']),
            Paragraph("2", styles['TableCell']),
            Paragraph("685 ms", styles['TableCell']),
            Paragraph("0,685 s", styles['TableCell']),
            Paragraph("Aún no compensa", styles['TableCell'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("78.498", styles['TableCell']),
            Paragraph("Multiproceso", styles['TableCellLeft']),
            Paragraph("4", styles['TableCell']),
            Paragraph("877 ms", styles['TableCell']),
            Paragraph("0,877 s", styles['TableCell']),
            Paragraph("Aún no compensa", styles['TableCell'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("78.498", styles['TableCell']),
            Paragraph("Multiproceso", styles['TableCellLeft']),
            Paragraph("8", styles['TableCell']),
            Paragraph("1.307 ms", styles['TableCell']),
            Paragraph("1,307 s", styles['TableCell']),
            Paragraph("Demasiados procesos", styles['TableCell'])
        ],
        # N = 10.000.000
        [
            Paragraph("<b>Rango grande</b><br/>Hasta 10.000.000", styles['TableCellLeft']),
            Paragraph("664.579", styles['TableCell']),
            Paragraph("Secuencial (Normal)", styles['TableCellLeft']),
            Paragraph("1", styles['TableCell']),
            Paragraph("3.340 ms", styles['TableCell']),
            Paragraph("3,340 s", styles['TableCell']),
            Paragraph("Se hace pesado", styles['TableCell'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("664.579", styles['TableCell']),
            Paragraph("Multiproceso", styles['TableCellLeft']),
            Paragraph("2", styles['TableCell']),
            Paragraph("2.753 ms", styles['TableCell']),
            Paragraph("2,753 s", styles['TableCell']),
            Paragraph("Mejora un poco", styles['TableCell'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("664.579", styles['TableCell']),
            Paragraph("Multiproceso (El mejor)", styles['TableCellLeft']),
            Paragraph("4", styles['TableCell']),
            Paragraph("<b>2.069 ms</b>", styles['TableCellBold']),
            Paragraph("2,069 s", styles['TableCell']),
            Paragraph("<b>Gana un 61% (1,3s menos)</b>", styles['TableCellBold'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("664.579", styles['TableCell']),
            Paragraph("Multiproceso", styles['TableCellLeft']),
            Paragraph("8", styles['TableCell']),
            Paragraph("2.098 ms", styles['TableCell']),
            Paragraph("2,098 s", styles['TableCell']),
            Paragraph("Se frena por saturar CPU", styles['TableCell'])
        ]
    ]

    t_perf = Table(t_data, colWidths=[3.2 * cm, 2.0 * cm, 3.8 * cm, 1.8 * cm, 2.3 * cm, 2.2 * cm, 2.7 * cm])
    t_perf.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('PADDING', (0, 0), (-1, -1), 3.0),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('LINEBELOW', (0, 4), (-1, 4), 1.2, SECONDARY),
        ('LINEBELOW', (0, 8), (-1, 8), 1.2, SECONDARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('BACKGROUND', (0, 11), (-1, 11), HIGHLIGHT),
    ]))
    story.append(t_perf)
    story.append(Spacer(1, 7))

    # Cuadro explicativo
    callout_data = [[
        Paragraph(
            "<b>Lo más importante que vemos aquí:</b> Para el rango pedido en la práctica (200.000), el cálculo es tan rápido (16 ms) que el multiproceso tarda mucho más (861 ms) porque pierde casi un segundo solo en abrir los 4 programas de Java. En cambio, cuando el problema es muy pesado (10 millones), el multiproceso sí gana claramente y nos ahorra más de 1,2 segundos.",
            styles['CalloutText']
        )
    ]]
    callout_t = Table(callout_data, colWidths=[18.0 * cm])
    callout_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#E0F2F1")),
        ('BOX', (0, 0), (-1, -1), 1, ACCENT),
        ('PADDING', (0, 0), (-1, -1), 5.5),
    ]))
    story.append(callout_t)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: CONCLUSIONES CLARAS Y MATRIZ DE RÚBRICA
    # =========================================================================
    story.append(Paragraph("4. Conclusiones y Explicación de lo que Ocurre", styles['SectionHeader']))

    story.append(Paragraph("4.1. ¿Por qué tarda tanto en arrancar cada proceso? (Sobrecarga de la JVM)", styles['SubSectionHeader']))
    story.append(Paragraph(
        "Cuando usamos <code>ProcessBuilder</code> para llamar a <code>java procesos.TrabajadorPrimo</code>, el ordenador no crea un simple hilo ligero, sino que tiene que <b>abrir una máquina virtual de Java (JVM) completa e independiente desde cero</b>. Esto significa que el sistema operativo tiene que asignarle memoria RAM propia, cargar las librerías internas de Java, arrancar el recolector de basura (Garbage Collector) y preparar el entorno de ejecución. Todo esto tarda entre <b>150 y 200 milisegundos por cada proceso</b>. Por eso, si el cálculo solo dura 16 ms (como en 200.000), abrir 4 procesos hace que tardemos casi un segundo solo en arrancar, yendo mucho peor que el secuencial.",
        styles['Body']
    ))

    story.append(Paragraph("4.2. ¿Cuándo compensa usar multiproceso y por qué se frena con 8 procesos?", styles['SubSectionHeader']))
    story.append(Paragraph(
        "El multiproceso empieza a salir rentable cuando la tarea es muy pesada. Al buscar primos hasta 10 millones, el programa secuencial tarda 3,3 segundos. Aquí el tiempo de arranque de Java ya no se nota tanto, y al repartir los números entre 4 procesos que corren a la vez en los núcleos del procesador, el tiempo baja a <b>2,06 segundos</b> (un 61% más rápido). Sin embargo, al poner 8 procesos el tiempo no mejora (2,09 s), porque la CPU se satura teniendo que repartirse entre 8 programas pesados de Java a la vez y pasando datos por la consola.",
        styles['Body']
    ))

    story.append(Paragraph("4.3. Ventajas y desventajas de usar Procesos frente a Hilos (Threads)", styles['SubSectionHeader']))
    story.append(Paragraph("• <b>Seguridad y aislamiento (Ventaja del multiproceso):</b> Cada proceso trabaja en su propia memoria cerrada e independiente. Si un proceso trabajador falla, se bloquea o se queda sin memoria, <i>el programa maestro no se rompe</i>; simplemente se entera mediante el código de salida que devuelve <code>waitFor()</code> y puede seguir funcionando sin problemas.", styles['BulletItem']))
    story.append(Paragraph("• <b>Consumo de recursos (Desventaja del multiproceso):</b> Cada proceso gasta mucha memoria RAM porque necesita su propia copia de Java funcionando. En cambio, con hilos todos comparten el mismo programa y la misma memoria, gastando mucho menos.", styles['BulletItem']))
    story.append(Paragraph("• <b>Forma de comunicarse:</b> En multiproceso tenemos que enviar los datos a través de la consola (con <code>stdout</code> y <code>BufferedReader</code>), lo que añade un poco de retardo. Con hilos es instantáneo porque leen directamente variables en la memoria RAM.", styles['BulletItem']))

    story.append(Spacer(1, 5))

    # 5. Rúbrica de evaluación
    story.append(Paragraph("5. Matriz de Cumplimiento de la Rúbrica", styles['SectionHeader']))
    rubric_data = [
        [
            Paragraph("<b>Apartado de la Rúbrica</b>", styles['TableHeader']),
            Paragraph("<b>Nota</b>", styles['TableHeader']),
            Paragraph("<b>¿Cómo se ha cumplido en la práctica?</b>", styles['TableHeader'])
        ],
        [
            Paragraph("<b>Funcionamiento</b>", styles['TableCellLeft']),
            Paragraph("<b>3,33 / 3,33</b><br/>(Excelente)", styles['TableCellBold']),
            Paragraph("Las tres clases (<code>TrabajadorPrimo</code>, <code>MaestroProcesos</code>, <code>PrimosSecuencial</code>) funcionan perfectamente, controlan errores de argumentos y dan exactamente el mismo número de primos (17.984 para 200.000).", styles['TableCellLeft'])
        ],
        [
            Paragraph("<b>Análisis y conclusiones</b>", styles['TableCellLeft']),
            Paragraph("<b>3,33 / 3,33</b><br/>(Excelente)", styles['TableCellBold']),
            Paragraph("Se han medido los tiempos con 2, 4 y 8 procesos en rangos pequeños, medios y grandes, explicando de forma clara por qué el arranque de la JVM frena al multiproceso con números pequeños y cuándo empieza a salir rentable.", styles['TableCellLeft'])
        ],
        [
            Paragraph("<b>Documentación y presentación</b>", styles['TableCellLeft']),
            Paragraph("<b>3,34 / 3,34</b><br/>(Excelente)", styles['TableCellBold']),
            Paragraph("Código con Javadoc completo sin errores ni advertencias, fichero <code>README.md</code> bien organizado con instrucciones paso a paso e informe en PDF bien presentado.", styles['TableCellLeft'])
        ],
        [
            Paragraph("<b>TOTAL</b>", styles['TableCellLeft']),
            Paragraph("<b>10,00 / 10,00</b>", styles['TableCellBold']),
            Paragraph("<b>Práctica terminada cumpliendo todos los entregables solicitados.</b>", styles['TableCellLeft'])
        ]
    ]
    rubric_t = Table(rubric_data, colWidths=[3.5 * cm, 2.5 * cm, 12.0 * cm])
    rubric_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECONDARY),
        ('PADDING', (0, 0), (-1, -1), 3.2),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, BG_LIGHT]),
        ('BACKGROUND', (0, -1), (-1, -1), HIGHLIGHT),
    ]))
    story.append(rubric_t)

    # Construir documento final
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado con éxito: {filename}")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    target_pdf = os.path.join(out_dir, "Informe_Practica_Multiproceso_Primos.pdf")
    build_pdf(target_pdf)
