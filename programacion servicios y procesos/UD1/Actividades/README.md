# Práctica: Multiproceso en Java — Cálculo de Números Primos

* **Asignatura:** Programación de Servicios y Procesos (PSP)
* **Curso:** 2º DAM (Desarrollo de Aplicaciones Multiplataforma)
* **Tema:** Unidad 1 - Programación Multiproceso
* **Alumno:** Kevin Muñoz Córcoles

---

## 1. ¿De qué va esta práctica?

En esta práctica hemos creado un programa en Java para contar cuántos números primos hay dentro de un rango (por ejemplo, del 1 al 200.000), pero dividiendo el trabajo entre **varios procesos a la vez** para aprovechar los núcleos del procesador.

Para ver si realmente merece la pena usar multiproceso o no, hemos montado el sistema usando el patrón **Maestro-Trabajador** y lo hemos comparado con una versión **secuencial** (que hace todo el trabajo en un solo programa tradicional).

---

## 2. ¿Cómo está organizado el código?

Hemos creado tres clases principales dentro del paquete `procesos` (y una copia en `Practicas01` por si se ejecuta directamente en el IDE):

```text
Actividades/
├── src/main/java/
│   ├── procesos/
│   │   ├── TrabajadorPrimo.java   # El proceso hijo (calcula su parte)
│   │   ├── MaestroProcesos.java   # El programa principal (reparte el trabajo)
│   │   └── PrimosSecuencial.java  # Versión normal de toda la vida (para comparar)
│   └── Practicas01/
│       ├── TrabajadorPrimo.java
│       ├── MaestroProcesos.java
│       └── PrimosSecuencial.java
├── pom.xml
├── README.md
└── Informe_Practica_Multiproceso_Primos.pdf
```

### Explicación sencilla de cada clase:

1. **`TrabajadorPrimo.java` (El trabajador):**
   * Es un programa independiente. Le pasamos dos números por argumentos: el `inicio` y el `fin`.
   * Si le pasamos mal los argumentos (por ejemplo si faltan números, no son enteros o el inicio es mayor que el fin), muestra el mensaje de error por la salida de errores (`System.err`) y se cierra con código de salida `1` (`System.exit(1)`).
   * Si todo está bien, calcula cuántos primos hay en ese trozo, imprime el número por pantalla (`System.out.println`) y termina con código `0` (`System.exit(0)`).

2. **`MaestroProcesos.java` (El jefe / coordinador):**
   * Es el programa principal. Por defecto busca primos del 1 al 200.000 usando 4 procesos, pero se le pueden pasar otros valores por argumentos.
   * **¿Qué hace paso a paso?**
     1. Parte el rango total en trozos iguales para que cada trabajador tenga la misma cantidad de trabajo.
     2. Lanza los procesos hijos en paralelo usando `ProcessBuilder` llamando a `TrabajadorPrimo`.
     3. Lee el número que devuelve cada hijo por la consola usando un `BufferedReader`.
     4. Espera a que terminen con `waitFor()` y comprueba que el código de salida sea `0`.
     5. Suma los resultados de todos los procesos y nos muestra por pantalla el total de primos y cuánto tiempo ha tardado en milisegundos.

3. **`PrimosSecuencial.java` (El programa de comparación):**
   * Hace exactamente la misma cuenta de números primos, pero sin crear procesos ni hilos: todo seguido en el mismo programa.
   * Nos sirve para comprobar dos cosas:
     * Que el resultado de primos sea exactamente el mismo (para estar seguros de que no nos hemos dejado ningún número al dividir los rangos).
     * Comparar los tiempos y ver cuándo es más rápido el secuencial y cuándo el multiproceso.

---

## 3. Cómo compilar y ejecutar los programas

### 3.1. Compilar desde la terminal
Nos situamos en la carpeta `src/main/java`:

```bash
cd "src/main/java"
javac procesos/*.java
```

### 3.2. Ejecutar los programas

#### A) Ejecutar el Maestro (Multiproceso)
Si lo ejecutamos sin argumentos, usa los valores pedidos en la práctica ($N = 200.000$ y $4$ procesos):
```bash
java procesos.MaestroProcesos
```

Si queremos probar con otros números (por ejemplo hasta 10 millones con 4 procesos):
```bash
java procesos.MaestroProcesos 10000000 4
```

#### B) Ejecutar la versión Secuencial (Monoproceso)
Por defecto calcula hasta 200.000:
```bash
java procesos.PrimosSecuencial
```

O indicando el número límite:
```bash
java procesos.PrimosSecuencial 10000000
```

#### C) Probar un Trabajador suelto (Pruebas individuales)
Podemos llamar al trabajador directamente para ver cómo responde:
```bash
# Caso correcto: cuenta los primos del 1 al 100 (da 25)
java procesos.TrabajadorPrimo 1 100

# Casos de error: nos avisa por stderr y devuelve código de salida 1
java procesos.TrabajadorPrimo 100 50    # Rango al revés
java procesos.TrabajadorPrimo hola adios # No son números
java procesos.TrabajadorPrimo 50        # Falta un parámetro
```

---

## 4. Pruebas y Tiempos Reales Obtenidos

Hemos hecho pruebas en el ordenador midiendo los tiempos con el secuencial y con multiproceso usando 2, 4 y 8 procesos:

### Prueba 1: Rango pequeño ($N = 200.000$ — Total: 17.984 primos)
| Modo de ejecución | Nº de Procesos | Tiempo (ms) | Tiempo (s) | ¿Qué ocurre? |
| :--- | :---: | :---: | :---: | :--- |
| **Secuencial (Normal)** | 1 | **16 ms** | 0,016 s | **El más rápido.** Va directo al grano. |
| **Multiproceso** | 2 | 564 ms | 0,564 s | Mucho más lento. |
| **Multiproceso (Práctica)** | 4 | 861 ms | 0,861 s | Más lento todavía. |
| **Multiproceso** | 8 | 1.285 ms | 1,285 s | El más lento de todos. |

### Prueba 2: Rango medio ($N = 1.000.000$ — Total: 78.498 primos)
| Modo de ejecución | Nº de Procesos | Tiempo (ms) | Tiempo (s) | ¿Qué ocurre? |
| :--- | :---: | :---: | :---: | :--- |
| **Secuencial (Normal)** | 1 | **127 ms** | 0,127 s | Sigue ganando el secuencial. |
| **Multiproceso** | 2 | 685 ms | 0,685 s | Sigue pesando el arranque de Java. |
| **Multiproceso** | 4 | 877 ms | 0,877 s | Cerca del punto de equilibrio. |
| **Multiproceso** | 8 | 1.307 ms | 1,307 s | Tantos procesos siguen frenando. |

### Prueba 3: Rango grande y pesado ($N = 10.000.000$ — Total: 664.579 primos)
| Modo de ejecución | Nº de Procesos | Tiempo (ms) | Tiempo (s) | ¿Qué ocurre? |
| :--- | :---: | :---: | :---: | :--- |
| **Secuencial (Normal)** | 1 | 3.340 ms | 3,340 s | El cálculo se vuelve pesado. |
| **Multiproceso** | 2 | 2.753 ms | 2,753 s | Empieza a mejorar al secuencial. |
| **Multiproceso (El mejor)** | 4 | **2.069 ms** | 2,069 s | **El más rápido.** Gana un 61% de velocidad. |
| **Multiproceso** | 8 | 2.098 ms | 2,098 s | Se estanca porque satura la CPU. |

---

## 5. Conclusiones y Explicación de lo que pasa

### 1. ¿Por qué el multiproceso es más lento con números pequeños (200.000)?
En Java, cuando lanzamos un proceso con `ProcessBuilder` ejecutando el comando `java`, no estamos creando simplemente un hilito ligero: **el ordenador tiene que abrir una máquina virtual de Java (JVM) completa desde cero para cada proceso**. 

Esto significa que el sistema operativo tiene que reservar memoria, cargar librerías de Java, inicializar el recolector de basura (Garbage Collector) y preparar todo el entorno. Eso tarda unos **150 a 200 milisegundos por cada proceso**.

* Si el cálculo en sí solo tarda **16 milisegundos** (como pasa con 200.000), abrir 4 máquinas virtuales nos hace perder casi un segundo solo en arrancar. Por eso el secuencial le da mil vueltas en tareas pequeñas.

### 2. ¿Cuándo merece la pena usar multiproceso?
Merece la pena cuando el trabajo matemático es muy grande y pesado (como con 10 millones de números). 
* Ahí el secuencial tarda más de 3 segundos seguidos. Como el trabajo tarda bastante, los ~200 ms que tardan en arrancar los procesos ya no importan tanto, y al repartir los números entre 4 procesos que corren en paralelo en los núcleos del procesador, el tiempo baja a **2 segundos**.
* Con 8 procesos ya no mejora más porque el procesador se satura cambiando de un proceso a otro y arrancando 8 JVMs a la vez.

### 3. Ventajas y desventajas de usar Procesos frente a Hilos (*Threads*)

* **Ventajas de los procesos:**
  * **Seguridad y aislamiento total:** Cada proceso tiene su propia memoria independiente. Si un trabajador se cuelga, se queda sin memoria o da un fallo grave, **el programa maestro no se cae ni se rompe**. El maestro simplemente recibe el código de error en `waitFor()` y puede seguir funcionando.
  * **Aprovechamiento directo del procesador:** El sistema operativo reparte los procesos automáticamente entre los núcleos de la CPU.

* **Desventajas de los procesos:**
  * **Mucha sobrecarga y gasto de memoria:** Cada proceso gasta mucha memoria RAM porque tiene su propia JVM completa.
  * **Comunicación más lenta y pesada:** Para pasarse datos entre procesos hay que hacerlo mediante la consola (`stdout`/`stderr`), leyendo líneas de texto con `BufferedReader`. En cambio, con hilos se comparten variables directamente en la memoria RAM de forma inmediata.

---

## 6. Documentación Javadoc
Todas las clases, métodos y parámetros tienen sus comentarios Javadoc listos. Se puede generar la documentación HTML ejecutando:
```bash
javadoc -d docs -encoding UTF-8 -charset UTF-8 procesos/*.java
```
