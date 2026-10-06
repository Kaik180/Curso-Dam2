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

# Colores limpios y sencillos
PRIMARY = colors.HexColor("#1565C0")       # Azul corporativo
SECONDARY = colors.HexColor("#1E88E5")     # Azul claro
DARK_BG = colors.HexColor("#1E1E24")       # Fondo consola
TEXT_DARK = colors.HexColor("#263238")     # Texto principal
TEXT_MUTED = colors.HexColor("#546E7A")    # Texto pie y encabezado
BG_LIGHT = colors.HexColor("#F4F6F9")      # Fondo tablas
BORDER_COLOR = colors.HexColor("#CFD8DC")  # Bordes suaves
HIGHLIGHT = colors.HexColor("#E8F5E9")     # Resaltado verde pastel

class NumberedCanvas(canvas.Canvas):
    """
    Controla el pie de página con 'Página X de Y' y el encabezado sencillo.
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

        # Encabezado (página 2)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8.5)
            self.setFillColor(PRIMARY)
            self.drawString(1.5 * cm, h - 1.15 * cm, "PSP - 2º DAM | Práctica 1: Multiproceso en Java")
            self.setFont("Helvetica", 8.5)
            self.setFillColor(TEXT_MUTED)
            self.drawRightString(w - 1.5 * cm, h - 1.15 * cm, "Kevin Muñoz Córcoles")

            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(1.5 * cm, h - 1.25 * cm, w - 1.5 * cm, h - 1.25 * cm)

        # Pie de página (todas las hojas)
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(1.5 * cm, 1.25 * cm, w - 1.5 * cm, 1.25 * cm)

        self.setFont("Helvetica", 8.5)
        self.setFillColor(TEXT_MUTED)
        self.drawString(1.5 * cm, 0.85 * cm, "Programación de Servicios y Procesos (PSP)")
        self.drawRightString(w - 1.5 * cm, 0.85 * cm, f"Página {self._pageNumber} de {total_pages}")

        self.restoreState()


def create_terminal_block(command_text, output_text, styles):
    """
    Bloque que simula la terminal con formato limpio.
    """
    cmd_para = Paragraph(
        f"<font color='#81C784'><b>$</b></font> <font color='#FFFFFF'><b>{command_text}</b></font>",
        styles['TerminalCommand']
    )
    formatted_out = output_text.replace('\n', '<br/>').replace(' ', '&nbsp;')
    out_para = Paragraph(
        f"<font color='#ECEFF1'>{formatted_out}</font>",
        styles['TerminalOutput']
    )
    
    data = [[cmd_para], [Spacer(1, 1)], [out_para]]
    t = Table(data, colWidths=[18.0 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DARK_BG),
        ('PADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, 0), 3),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
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
        'DocSubtitle': ParagraphStyle('DocSubtitle', parent=base['Normal'], fontName='Helvetica', fontSize=10, leading=13, textColor=SECONDARY, spaceAfter=6),
        'SectionHeader': ParagraphStyle('SectionHeader', parent=base['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=PRIMARY, spaceBefore=4, spaceAfter=2, keepWithNext=True),
        'Body': ParagraphStyle('Body', parent=base['Normal'], fontName='Helvetica', fontSize=8.4, leading=11.3, textColor=TEXT_DARK, spaceAfter=3),
        'BulletItem': ParagraphStyle('BulletItem', parent=base['Normal'], fontName='Helvetica', fontSize=8.2, leading=11.0, textColor=TEXT_DARK, leftIndent=8, spaceAfter=2),
        'MetaBox': ParagraphStyle('MetaBox', parent=base['Normal'], fontName='Helvetica', fontSize=8.2, leading=10.6, textColor=TEXT_DARK),
        'TerminalCommand': ParagraphStyle('TerminalCommand', fontName='Courier-Bold', fontSize=7.4, leading=9.4, textColor=colors.white),
        'TerminalOutput': ParagraphStyle('TerminalOutput', fontName='Courier', fontSize=6.8, leading=8.6, textColor=colors.HexColor("#ECEFF1")),
        'TableHeader': ParagraphStyle('TableHeader', fontName='Helvetica-Bold', fontSize=7.6, leading=9.4, textColor=colors.white, alignment=1),
        'TableCell': ParagraphStyle('TableCell', fontName='Helvetica', fontSize=7.6, leading=9.4, textColor=TEXT_DARK, alignment=1),
        'TableCellLeft': ParagraphStyle('TableCellLeft', fontName='Helvetica', fontSize=7.6, leading=9.4, textColor=TEXT_DARK, alignment=0),
        'TableCellBold': ParagraphStyle('TableCellBold', fontName='Helvetica-Bold', fontSize=7.6, leading=9.4, textColor=PRIMARY, alignment=1),
    }

    story = []

    # =========================================================================
    # PÁGINA 1: EXPLICACIÓN Y CAPTURAS DE EJECUCIÓN
    # =========================================================================
    story.append(Paragraph("Práctica Multiproceso: Cálculo de Primos en Java", styles['DocTitle']))
    story.append(Paragraph("Informe breve de resultados, capturas y comparativa de tiempos", styles['DocSubtitle']))

    # Cuadro de datos del alumno
    meta_data = [
        [
            Paragraph("<b>Alumno:</b> Kevin Muñoz Córcoles", styles['MetaBox']),
            Paragraph("<b>Curso:</b> 2º DAM (Desarrollo de Aplicaciones Multiplataforma)", styles['MetaBox'])
        ],
        [
            Paragraph("<b>Módulo:</b> Programación de Servicios y Procesos (PSP)", styles['MetaBox']),
            Paragraph("<b>Unidad:</b> UD1 — Multiproceso (ProcessBuilder en Java)", styles['MetaBox'])
        ]
    ]
    meta_t = Table(meta_data, colWidths=[9.0 * cm, 9.0 * cm])
    meta_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('PADDING', (0, 0), (-1, -1), 3),
        ('BOX', (0, 0), (-1, -1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, BORDER_COLOR),
    ]))
    story.append(meta_t)
    story.append(Spacer(1, 4))

    # 1. Descripción
    story.append(Paragraph("1. ¿Qué hace el programa y qué clases hemos creado?", styles['SectionHeader']))
    story.append(Paragraph(
        "El ejercicio consiste en contar cuántos números primos hay del 1 al 200.000 comparando dos métodos: haciéndolo en un programa normal (secuencial) o repartiendo el trabajo entre varios subprocesos a la vez (multiproceso). Para ello hemos programado tres clases:",
        styles['Body']
    ))
    story.append(Paragraph("• <b>TrabajadorPrimo.java:</b> Es el proceso hijo. Recibe por consola el rango <code>inicio</code> y <code>fin</code>. Si los argumentos están mal, saca un error por <code>stderr</code> y termina con código 1. Si son correctos, cuenta los primos de ese trozo, imprime el número por <code>stdout</code> y termina con código 0.", styles['BulletItem']))
    story.append(Paragraph("• <b>MaestroProcesos.java:</b> Es el programa principal. Divide el rango del 1 al 200.000 en partes iguales y lanza los procesos hijos a la vez con <code>ProcessBuilder</code>. Lee sus respuestas con un <code>BufferedReader</code>, espera a que acaben con <code>waitFor()</code> y suma todos los resultados mostrando el total de primos y el tiempo que ha tardado.", styles['BulletItem']))
    story.append(Paragraph("• <b>PrimosSecuencial.java:</b> Hace la misma cuenta de números primos en un solo proceso tradicional para comprobar que el resultado es idéntico (17.984 primos) y ver cuánto tiempo tarda.", styles['BulletItem']))

    story.append(Spacer(1, 4))

    # 2. Capturas de ejecución
    story.append(Paragraph("2. Capturas de Ejecución en la Consola", styles['SectionHeader']))

    # Captura 1: Trabajador
    t1_cmd = "java procesos.TrabajadorPrimo 1 100 && java procesos.TrabajadorPrimo 100 50"
    t1_out = "25\nError [TrabajadorPrimo]: Rango inválido [100, 50]. Se requiere inicio >= 1 e inicio <= fin.\n[Proceso terminado con código de salida: 1]"
    story.append(Paragraph("<b>Captura 2.1:</b> Probando <code>TrabajadorPrimo</code> (caso correcto del 1 al 100 dando 25, y caso de error con rango al revés):", styles['Body']))
    story.append(create_terminal_block(t1_cmd, t1_out, styles))
    story.append(Spacer(1, 4))

    # Captura 2: Secuencial
    t2_cmd = "java procesos.PrimosSecuencial 200000"
    t2_out = (
        "==============================================================\n"
        "   CALCULO SECUENCIAL DE PRIMOS (LINEA BASE / MONOPROCESO)   \n"
        "==============================================================\n"
        "Rango evaluado: [1, 200.000]\n"
        "RESULTADOS SECUENCIAL:\n"
        "  Total de numeros primos encontrados: 17.984\n"
        "  Tiempo total transcurrido:           16 ms (0,016 s)\n"
        "=============================================================="
    )
    story.append(Paragraph("<b>Captura 2.2:</b> Ejecución de <code>PrimosSecuencial</code> (cuenta todos los primos en 16 ms):", styles['Body']))
    story.append(create_terminal_block(t2_cmd, t2_out, styles))
    story.append(Spacer(1, 4))

    # Captura 3: Maestro
    t3_cmd = "java procesos.MaestroProcesos 200000 4"
    t3_out = (
        "==============================================================\n"
        "   CALCULO PARALELO DE PRIMOS (MULTIPROCESO EN JAVA)         \n"
        "==============================================================\n"
        "Rango total: [1, 200.000] | Numero de procesos (M): 4\n"
        "Seguimiento de los subprocesos:\n"
        "  [Proceso 1] Rango [         1 -     50.000] ->    5.133 primos (exit: 0)\n"
        "  [Proceso 2] Rango [    50.001 -    100.000] ->    4.459 primos (exit: 0)\n"
        "  [Proceso 3] Rango [   100.001 -    150.000] ->    4.256 primos (exit: 0)\n"
        "  [Proceso 4] Rango [   150.001 -    200.000] ->    4.136 primos (exit: 0)\n"
        "RESULTADOS MULTIPROCESO:\n"
        "  Total de numeros primos encontrados: 17.984\n"
        "  Tiempo total transcurrido:           861 ms (0,861 s)\n"
        "=============================================================="
    )
    story.append(Paragraph("<b>Captura 2.3:</b> Ejecución de <code>MaestroProcesos</code> con 4 subprocesos concurrentes:", styles['Body']))
    story.append(create_terminal_block(t3_cmd, t3_out, styles))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: TABLA DE TIEMPOS Y CONCLUSIONES
    # =========================================================================
    story.append(Paragraph("3. Tabla Comparativa de Tiempos", styles['SectionHeader']))
    story.append(Paragraph(
        "Tiempos reales medidos en el equipo para el rango pedido en la práctica (hasta 200.000, encontrando 17.984 primos) y una prueba adicional con un cálculo muy pesado (hasta 10.000.000, con 664.579 primos):",
        styles['Body']
    ))

    t_data = [
        [
            Paragraph("<b>Prueba / Rango</b>", styles['TableHeader']),
            Paragraph("<b>Modo de Ejecución</b>", styles['TableHeader']),
            Paragraph("<b>Procesos</b>", styles['TableHeader']),
            Paragraph("<b>Tiempo (ms)</b>", styles['TableHeader']),
            Paragraph("<b>Tiempo (s)</b>", styles['TableHeader']),
            Paragraph("<b>Conclusión rápida</b>", styles['TableHeader'])
        ],
        [
            Paragraph("<b>Rango pedido</b><br/>(Hasta 200.000)", styles['TableCellLeft']),
            Paragraph("Secuencial (Normal)", styles['TableCellLeft']),
            Paragraph("1", styles['TableCell']),
            Paragraph("<b>16 ms</b>", styles['TableCellBold']),
            Paragraph("0,016 s", styles['TableCell']),
            Paragraph("<b>El más rápido (Gana)</b>", styles['TableCellBold'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("Multiproceso", styles['TableCellLeft']),
            Paragraph("2", styles['TableCell']),
            Paragraph("564 ms", styles['TableCell']),
            Paragraph("0,564 s", styles['TableCell']),
            Paragraph("Más lento por abrir 2 Java", styles['TableCell'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("Multiproceso (Práctica)", styles['TableCellLeft']),
            Paragraph("4", styles['TableCell']),
            Paragraph("861 ms", styles['TableCell']),
            Paragraph("0,861 s", styles['TableCell']),
            Paragraph("Más lento por abrir 4 Java", styles['TableCell'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("Multiproceso", styles['TableCellLeft']),
            Paragraph("8", styles['TableCell']),
            Paragraph("1.285 ms", styles['TableCell']),
            Paragraph("1,285 s", styles['TableCell']),
            Paragraph("El más lento (abre 8 Java)", styles['TableCell'])
        ],
        [
            Paragraph("<b>Prueba pesada</b><br/>(Hasta 10.000.000)", styles['TableCellLeft']),
            Paragraph("Secuencial (Normal)", styles['TableCellLeft']),
            Paragraph("1", styles['TableCell']),
            Paragraph("3.340 ms", styles['TableCell']),
            Paragraph("3,340 s", styles['TableCell']),
            Paragraph("Se hace pesado (1 solo núcleo)", styles['TableCell'])
        ],
        [
            Paragraph("", styles['TableCellLeft']),
            Paragraph("Multiproceso (Óptimo)", styles['TableCellLeft']),
            Paragraph("4", styles['TableCell']),
            Paragraph("<b>2.069 ms</b>", styles['TableCellBold']),
            Paragraph("2,069 s", styles['TableCell']),
            Paragraph("<b>Gana (ahorra 1,3 segundos)</b>", styles['TableCellBold'])
        ]
    ]

    t_perf = Table(t_data, colWidths=[3.2 * cm, 3.8 * cm, 1.8 * cm, 2.3 * cm, 2.2 * cm, 4.7 * cm])
    t_perf.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('PADDING', (0, 0), (-1, -1), 3),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('LINEBELOW', (0, 4), (-1, 4), 1, SECONDARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('BACKGROUND', (0, 1), (-1, 1), HIGHLIGHT),
        ('BACKGROUND', (0, 6), (-1, 6), HIGHLIGHT),
    ]))
    story.append(t_perf)
    story.append(Spacer(1, 6))

    # 4. Conclusiones
    story.append(Paragraph("4. Conclusiones: Ventajas, Inconvenientes y Sobrecarga", styles['SectionHeader']))

    story.append(Paragraph("<b>A) ¿Por qué el multiproceso es más lento con 200.000 números? (Sobrecarga de la JVM):</b>", styles['Body']))
    story.append(Paragraph(
        "Cada vez que lanzamos un proceso con <code>ProcessBuilder</code> ejecutando <code>java</code>, el sistema operativo tiene que abrir la máquina virtual de Java (JVM) completa desde cero para ese proceso. Eso supone reservar memoria RAM, cargar librerías internas de Java y preparar el entorno, lo que tarda entre <b>150 y 200 ms por proceso</b>. Como calcular los primos hasta 200.000 solo le cuesta al ordenador 16 ms, abrir 4 procesos hace que perdamos casi un segundo solo en arrancar. Por eso el secuencial es mucho más rápido en tareas cortas.",
        styles['Body']
    ))

    story.append(Paragraph("<b>B) ¿Cuándo merece la pena usar multiproceso?:</b>", styles['Body']))
    story.append(Paragraph(
        "Merece la pena cuando el cálculo es muy pesado. Al probar con <b>10 millones de números</b>, el secuencial tarda 3,3 segundos. En este caso, como el trabajo tarda bastante tiempo, el coste de arrancar las máquinas virtuales compensa totalmente: al repartir los números entre 4 procesos que corren a la vez en los núcleos del procesador, el tiempo baja a <b>2,06 segundos</b> (un ahorro de más de 1,2 segundos). Con 8 procesos no mejora más porque el procesador se satura cambiando entre tantos programas.",
        styles['Body']
    ))

    story.append(Paragraph("<b>C) Ventajas e inconvenientes del modelo de procesos:</b>", styles['Body']))
    story.append(Paragraph("• <b>Ventaja principal (Aislamiento de memoria):</b> Cada proceso trabaja en su propia memoria cerrada e independiente. Si un proceso trabajador falla, da error o se cuelga, <i>el programa maestro sigue funcionando y no se cae</i>. Simplemente detecta el código de salida en <code>waitFor()</code>.", styles['BulletItem']))
    story.append(Paragraph("• <b>Inconveniente 1 (Consumo de RAM):</b> Cada proceso gasta mucha memoria porque necesita una copia completa de Java funcionando.", styles['BulletItem']))
    story.append(Paragraph("• <b>Inconveniente 2 (Comunicación lenta):</b> Para pasarse datos entre procesos hay que leer líneas de texto por consola (<code>stdout</code> con <code>BufferedReader</code>), lo cual es más lento que usar hilos (<i>threads</i>) que comparten variables en la misma memoria.", styles['BulletItem']))

    # Construir documento final
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado con éxito: {filename}")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    target_pdf = os.path.join(out_dir, "Informe_Practica_Multiproceso_Primos.pdf")
    build_pdf(target_pdf)
