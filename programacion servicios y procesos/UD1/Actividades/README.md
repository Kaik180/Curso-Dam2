# Práctica: Multiproceso en Java — Cálculo Paralelo de Números Primos

**Módulo:** Programación de Servicios y Procesos (PSP)  
**Curso:** 2º Desarrollo de Aplicaciones Multiplataforma (DAM)  
**Unidad:** UD1 — Programación Multiproceso  
**Autor:** Kevin Muñoz Córcoles  

---

## 1. Descripción del Proyecto

Esta práctica implementa una arquitectura **Maestro-Trabajador (*Master-Worker*)** en Java para resolver de forma distribuida y concurrente el cálculo y conteo de números primos en un intervalo numérico cerrado $[1, N]$.

El objetivo central es comprender el ciclo de vida de los procesos en los sistemas operativos modernos, la creación y gestión de subprocesos mediante la API `ProcessBuilder` de Java, la sincronización entre procesos mediante `waitFor()` y la comunicación interproceso (**IPC**) básica a través de flujos estándar de entrada/salida (`stdout`, `stderr`).

Adicionalmente, se incluye una implementación secuencial de referencia (`PrimosSecuencial`) para medir empíricamente la sobrecarga asociada al arranque de múltiples Máquinas Virtuales de Java (JVM) y el *speedup* alcanzable frente a cargas de trabajo computacionalmente intensivas.

---

## 2. Arquitectura y Estructura de Clases

El proyecto está organizado dentro del paquete `procesos` (y replicado en `Practicas01` para compatibilidad completa en el IDE):

```
Actividades/
├── src/main/java/
│   ├── procesos/
│   │   ├── TrabajadorPrimo.java   # Proceso Worker independiente (subproceso)
│   │   ├── MaestroProcesos.java   # Proceso Master orquestador (proceso principal)
│   │   └── PrimosSecuencial.java  # Benchmark monoproceso secuencial (baseline)
│   └── Practicas01/
│       ├── TrabajadorPrimo.java
│       ├── MaestroProcesos.java
│       └── PrimosSecuencial.java
├── pom.xml
├── README.md
└── Informe_Practica_Multiproceso_Primos.pdf  # Informe técnico y comparativa
```

### 2.1. `TrabajadorPrimo` (Worker)
- **Rol:** Proceso secundario e independiente.
- **Argumentos recibidos:** `<inicio> <fin>` (rango cerrado $[inicio, fin]$ a procesar).
- **Comportamiento:**
  - Valida que se reciban exactamente dos argumentos numéricos enteros válidos, con $inicio \ge 1$ e $inicio \le fin$.
  - Si los argumentos son inválidos, imprime un mensaje descriptivo por **`stderr`** y finaliza inmediatamente con código de salida **`System.exit(1)`**.
  - Si los argumentos son válidos, cuenta los números primos en el rango mediante un algoritmo de división por tentativa optimizado ($6k \pm 1$, complejidad $\mathcal{O}(\sqrt{n})$).
  - Emite el total de primos por **`stdout`** y concluye exitosamente con **`System.exit(0)`**.

### 2.2. `MaestroProcesos` (Master / Coordinator)
- **Rol:** Proceso principal y coordinador del cálculo distribuido.
- **Parámetros configurables:** 
  - `args[0]` = $N$ (Límite superior, por defecto $200.000$).
  - `args[1]` = $M$ (Número de procesos paralelos, por defecto $4$).
- **Ciclo de orquestación:**
  1. **Partición equitativa:** Divide el rango $[1, N]$ en $M$ subintervalos homogéneos contiguos, distribuyendo el residuo ($N \pmod M$) equitativamente entre los primeros bloques.
  2. **Lanzamiento paralelo:** Instancia de forma no bloqueante $M$ procesos hijos ejecutando `TrabajadorPrimo` mediante `ProcessBuilder`, resolviendo automáticamente el binario de Java y el classpath en ejecución.
  3. **Recolección y sincronización:** Lee la salida estándar de cada subproceso mediante `BufferedReader` y sincroniza su finalización con `process.waitFor()`, verificando el código de retorno.
  4. **Agregación y métricas:** Suma las cuentas parciales de cada subproceso y cronometra el tiempo total transcurrido.

### 2.3. `PrimosSecuencial` (Monoproceso de referencia)
- **Rol:** Versión secuencial de control ejecutada en un único hilo dentro de un único proceso JVM.
- **Propósito:** Validar que el resultado total de primos coincida con exactitud y proporcionar una línea base (*baseline*) para cuantificar el impacto y sobrecarga del modelo multiproceso.

---

## 3. Instrucciones de Compilación y Ejecución

### 3.1. Requisitos Previos
- **JDK 17 o superior** (OpenJDK / Oracle JDK).
- Terminal de comandos (PowerShell, Bash o CMD) o un IDE compatible (IntelliJ IDEA, Eclipse, VS Code).

### 3.2. Compilación desde Terminal

Navegar hasta la carpeta `src/main/java` del proyecto:

```bash
cd "src/main/java"
javac procesos/*.java
```

### 3.3. Ejecución de las Clases

#### A) Proceso Maestro (Multiproceso)
Ejecución con parámetros sugeridos por defecto ($N=200.000, M=4$):
```bash
java procesos.MaestroProcesos
```

Ejecución personalizada pasando $N$ y $M$:
```bash
# Ejemplo: N = 10.000.000 con 8 procesos trabajadores
java procesos.MaestroProcesos 10000000 8
```

#### B) Versión Secuencial (Monoproceso)
Ejecución con valor por defecto ($N=200.000$):
```bash
java procesos.PrimosSecuencial
```

Ejecución con límite personalizado:
```bash
java procesos.PrimosSecuencial 10000000
```

#### C) Proceso Trabajador Individual (Pruebas unitarias y de validación)
Caso exitoso (cuenta primos entre 1 y 100, devuelve 25):
```bash
java procesos.TrabajadorPrimo 1 100
echo $LASTEXITCODE  # Devuelve 0
```

Casos de error de argumentos (devuelven código 1):
```bash
java procesos.TrabajadorPrimo 100 50    # Rango invertido
java procesos.TrabajadorPrimo abc def   # Parámetros no numéricos
java procesos.TrabajadorPrimo 50        # Falta un parámetro
```

---

## 4. Tabla Comparativa de Rendimiento

A continuación se presentan los resultados empíricos obtenidos en las pruebas de laboratorio bajo el mismo entorno de hardware:

### Caso A: Carga Ligera ($N = 200.000$, $17.984$ primos)
| Modelo de Ejecución | Procesos ($M$) | Tiempo Total (ms) | Tiempo (s) | Speedup vs. Secuencial |
| :--- | :---: | :---: | :---: | :---: |
| **Secuencial (Baseline)** | 1 | **19 ms** | 0,019 s | **1,00x** (Referencia) |
| **Multiproceso** | 2 | **594 ms** | 0,594 s | 0,03x (31x más lento) |
| **Multiproceso (Recomendado)** | 4 | **984 ms** | 0,984 s | 0,02x (51x más lento) |
| **Multiproceso** | 8 | **1.343 ms** | 1,343 s | 0,01x (70x más lento) |

### Caso B: Carga Intensiva ($N = 10.000.000$, $664.579$ primos)
| Modelo de Ejecución | Procesos ($M$) | Tiempo Total (ms) | Tiempo (s) | Speedup vs. Secuencial |
| :--- | :---: | :---: | :---: | :---: |
| **Secuencial (Baseline)** | 1 | **3.270 ms** | 3,270 s | **1,00x** (Referencia) |
| **Multiproceso** | 2 | **2.623 ms** | 2,623 s | **1,25x** (20% más rápido) |
| **Multiproceso** | 4 | **2.064 ms** | 2,064 s | **1,58x** (37% más rápido) |
| **Multiproceso** | 8 | **2.232 ms** | 2,232 s | **1,46x** (saturación por sobrecarga) |

---

## 5. Análisis y Conclusiones Técnicas

### 5.1. Sobrecarga del Arranque de la JVM (*Cold Start Overhead*)
En Java, cuando se lanza un proceso independiente mediante `ProcessBuilder` invocando el comando `java`, el sistema operativo debe:
1. Crear una nueva estructura de proceso en el kernel (PCB, tablas de páginas, descriptores de fichero).
2. Reservar un espacio de direcciones de memoria virtual exclusivo y desacoplado.
3. Cargar las librerías nativas de la JVM, inicializar subsistemas internos (Garbage Collector, compilador JIT, ClassLoader bootstrap y del sistema) y cargar las clases base de la plataforma Java.

Esta inicialización consume aproximadamente **$150 - 250\text{ ms}$ por proceso**. Por consiguiente:
- En rangos reducidos ($N \le 200.000$), el tiempo de computación pura es insignificante ($\approx 19\text{ ms}$). Lanzar 4 procesos introduce una penalización acumulada cercana al segundo, haciendo que la solución multiproceso sea sustancialmente más lenta que la secuencial.
- En rangos pesados ($N \ge 10.000.000$), el trabajo matemático a repartir supera con creces el coste de inicialización de las JVMs, traduciéndose en una reducción efectiva del tiempo de respuesta (*speedup* de hasta 1,58x con 4 procesos).

### 5.2. Ventajas e Inconvenientes del Modelo Multiproceso
- **Ventajas:**
  - **Aislamiento total de memoria:** Cada proceso trabajador opera en su propio espacio de memoria virtual protegido. Un fallo crítico o desbordamiento de memoria (`OutOfMemoryError`) en un trabajador no compromete al proceso maestro ni a los demás trabajadores.
  - **Aprovechamiento directo de múltiples núcleos (CPU Multi-core):** El planificador del sistema operativo distribuye los procesos pesados entre los núcleos físicos disponibles de forma transparente.
  - **Modularidad y desacoplamiento:** `TrabajadorPrimo` es un programa autocontenido que puede ser reutilizado por otros sistemas, scripts de shell o aplicaciones escritas en otros lenguajes.
- **Inconvenientes:**
  - **Elevado consumo de recursos:** Cada proceso requiere su propia memoria heap y stack, así como el runtime completo de Java.
  - **Comunicación Interproceso (IPC) más costosa:** Los datos deben serializarse y transmitirse a través de tuberías (*pipes* del sistema operativo), a diferencia del modelo multihilo (*multithreading*) donde la memoria se comparte de forma directa y ultrarrápida.
  - **Saturación en exceso de procesos:** Lanzar más procesos que núcleos lógicos disponibles genera contención por cambios de contexto (*context switching*) y sobrecarga de I/O, como se evidencia al pasar de 4 a 8 procesos.

---

## 6. Documentación Javadoc

El código fuente ha sido documentado exhaustivamente siguiendo el estándar Javadoc y las directrices HTML5:
- Comentarios completos para cada clase, método, parámetro (`@param`), retorno (`@return`) y códigos de salida.
- Constructores privados explícitos documentados para prevenir la instanciación de clases estáticas y utilitarias.
- Validación de generación sin errores ni advertencias mediante:
  ```bash
  javadoc -d docs -encoding UTF-8 -charset UTF-8 procesos/*.java
  ```
