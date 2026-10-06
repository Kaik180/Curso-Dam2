# Práctica Multiproceso: Cálculo de Primos en Java

* **Alumno:** Kevin Muñoz Córcoles
* **Curso:** 2º DAM (Desarrollo de Aplicaciones Multiplataforma)
* **Asignatura:** Programación de Servicios y Procesos (PSP)
* **Unidad:** UD1 - Programación Multiproceso

---

## 1. ¿De qué trata la práctica?

La práctica consiste en contar cuántos números primos hay entre 1 y 200.000 comparando dos formas de trabajar:
1. **Secuencial:** Un solo programa normal que hace toda la cuenta seguida.
2. **Multiproceso:** Un programa maestro que divide el rango en partes iguales y lanza varios procesos hijos a la vez usando `ProcessBuilder` para que trabajen en paralelo.

---

## 2. Clases creadas

* **`TrabajadorPrimo.java`**: Es el proceso hijo. Recibe dos números (`inicio` y `fin`). Si los argumentos están mal, muestra un error por `stderr` y se cierra con código 1. Si están bien, cuenta los primos de ese trozo, imprime el resultado por pantalla (`stdout`) y termina con código 0.
* **`MaestroProcesos.java`**: Es el programa principal. Divide el rango del 1 al 200.000 entre los procesos que le digamos (por defecto 4), lanza los trabajadores con `ProcessBuilder`, lee los resultados con `BufferedReader`, espera a que terminen con `waitFor()` y suma los totales mostrando el tiempo empleado.
* **`PrimosSecuencial.java`**: Hace la misma cuenta de forma secuencial (sin procesos). Nos sirve para comprobar que el resultado de primos es el mismo y ver la diferencia de tiempos.

---

## 3. Cómo compilar y ejecutar

Abrir la terminal en la carpeta `src/main/java`:

### 1. Compilar todas las clases
```bash
javac procesos/*.java
```

### 2. Ejecutar el maestro (Multiproceso)
Por defecto calcula hasta 200.000 con 4 procesos:
```bash
java procesos.MaestroProcesos
```
También le puedes pasar otros valores: `java procesos.MaestroProcesos <N> <numProcesos>`  
*(Ejemplo con 10 millones y 4 procesos: `java procesos.MaestroProcesos 10000000 4`)*.

### 3. Ejecutar la versión secuencial
```bash
java procesos.PrimosSecuencial
```

### 4. Probar un trabajador suelto
```bash
# Caso normal (primos del 1 al 100 -> devuelve 25):
java procesos.TrabajadorPrimo 1 100

# Casos con error (da aviso y código de salida 1):
java procesos.TrabajadorPrimo 100 50
java procesos.TrabajadorPrimo hola adios
```

---

## 4. Tabla de tiempos (N = 200.000)

En todos los casos encontramos exactamente **17.984 números primos**.

| Modo de ejecución | Nº de Procesos | Tiempo (ms) | Tiempo (s) |
| :--- | :---: | :---: | :---: |
| **Secuencial (Normal)** | 1 | **16 ms** | 0,016 s |
| **Multiproceso** | 2 | 564 ms | 0,564 s |
| **Multiproceso (Práctica)** | 4 | 861 ms | 0,861 s |
| **Multiproceso** | 8 | 1.285 ms | 1,285 s |

---

## 5. Conclusiones

1. **¿Por qué el multiproceso es más lento aquí?**  
   Porque para un rango de 200.000 números el cálculo es casi instantáneo (solo tarda 16 milisegundos). Al usar `ProcessBuilder` para llamar a `java`, el sistema tiene que abrir una máquina virtual de Java (JVM) completa para cada proceso hijo, lo que tarda unos 150-200 ms por proceso. Abrir 4 procesos nos hace perder casi un segundo solo en arrancar.

2. **¿Cuándo merece la pena usar multiproceso?**  
   Cuando el cálculo es muy pesado de verdad. Por ejemplo, si buscamos primos hasta **10 millones**, el secuencial tarda **3.340 ms**, mientras que con 4 procesos baja a **2.069 ms** (un 61% más rápido). Ahí el tiempo de arranque de Java ya compensa porque el trabajo se reparte entre los núcleos de la CPU.

3. **Ventajas del multiproceso:**  
   * **Aislamiento de fallos:** Cada proceso tiene su propia memoria. Si un trabajador se cuelga o da un fallo grave, el programa maestro sigue vivo y no se cae.

4. **Inconvenientes del multiproceso:**  
   * **Mucho gasto de memoria RAM:** Cada proceso necesita su propia copia de Java funcionando.
   * **Comunicación más lenta:** Hay que pasar los datos leyendo texto de la consola (`stdout`), lo que es más lento que compartir variables en memoria como se hace con los hilos (*threads*).
