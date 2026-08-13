# 🖼️ Laboratorio 1 — Carga y representación digital de imágenes

Este laboratorio es una introducción al **Procesamiento Digital de Imágenes (PDI)** utilizando Python y Jupyter Notebook.

El notebook principal es:

```text
cargar_imagen.ipynb
```

La idea del laboratorio no es únicamente aprender a abrir una imagen, sino comenzar a entender **cómo una computadora representa una imagen digital y qué información podemos obtener de ella**.

---

## 🎯 Propósito del laboratorio

Al visualizar una fotografía normalmente pensamos en objetos, colores, formas y escenas.

Sin embargo, para una computadora una imagen es esencialmente un conjunto organizado de **valores numéricos asociados a píxeles**.

En este laboratorio se busca conectar ambas perspectivas:

```text
Imagen que vemos
       ↓
Archivo digital
       ↓
Imagen cargada en Python
       ↓
Matriz de píxeles
       ↓
Valores de intensidad
       ↓
Procesamiento de la imagen
```

Comprender esta representación es fundamental antes de trabajar con operaciones como:

* brillo;
* contraste;
* histogramas;
* ecualización;
* filtros;
* segmentación;
* detección de bordes;
* visión por computadora.

---

# 🧠 Objetivos de aprendizaje

Al terminar este laboratorio deberíamos poder:

* comprender cómo se representa una imagen digital;
* cargar imágenes desde Python;
* visualizar imágenes dentro de un Jupyter Notebook;
* interpretar una imagen como una matriz de píxeles;
* identificar el tamaño o dimensiones de una imagen;
* comprender el concepto de intensidad de un píxel;
* relacionar una imagen con un espacio de posiciones discreto;
* reconocer la diferencia entre resolución espacial y niveles de intensidad;
* comprender conceptualmente el muestreo y la cuantización;
* preparar una imagen para operaciones posteriores de procesamiento digital.

---

# 1. ¿Qué es una imagen digital?

Una imagen puede entenderse como una función bidimensional:

```text
f(x, y)
```

donde:

* `x` representa una posición espacial;
* `y` representa otra posición espacial;
* `f(x, y)` representa el valor o intensidad de la imagen en esa posición.

Una vez digitalizada, las posiciones posibles dejan de ser continuas y pasan a estar organizadas en una cuadrícula.

Podemos imaginarla como:

```text
          columnas
       0   1   2   3
     ┌───┬───┬───┬───┐
  0  │   │   │   │   │
     ├───┼───┼───┼───┤
  1  │   │   │   │   │
     ├───┼───┼───┼───┤
  2  │   │   │   │   │
     └───┴───┴───┴───┘
       ↑
     píxeles
```

Cada una de estas posiciones corresponde a un **píxel**.

---

# 2. El píxel

El píxel es una de las unidades fundamentales de una imagen digital.

Podemos identificarlo mediante una posición:

```text
(x, y)
```

y asociarle uno o varios valores numéricos.

En una imagen en escala de grises, cada píxel posee principalmente un valor de intensidad.

Por ejemplo:

```text
0   → negro
...
128 → gris intermedio
...
255 → blanco
```

En una imagen de 8 bits existen:

```text
2⁸ = 256
```

niveles posibles de intensidad:

```text
0 ... 255
```

---

# 3. Una imagen como matriz

Cuando una imagen se carga en Python podemos comenzar a verla como una estructura numérica.

Una imagen de escala de grises puede representarse aproximadamente como:

```text
[
 [  0,  20,  80, 255],
 [ 15,  60, 120, 230],
 [ 30, 100, 180, 210]
]
```

Cada número representa la intensidad de un píxel.

Por eso muchos procedimientos de procesamiento de imágenes terminan siendo también **operaciones sobre matrices**.

Esta relación será importante posteriormente para trabajar con:

* transformaciones;
* filtros;
* histogramas;
* convoluciones;
* detección de características;
* procesamiento matemático de imágenes.

---

# 4. Dimensiones de una imagen

Una imagen digital posee un tamaño determinado.

Para una imagen podemos encontrar dimensiones similares a:

```text
alto × ancho
```

o, cuando existen canales:

```text
alto × ancho × canales
```

Por ejemplo:

```text
720 × 1280 × 3
```

puede representar una imagen con:

* `720` píxeles de alto;
* `1280` píxeles de ancho;
* `3` canales de color.

Comprender las dimensiones nos ayuda a saber **cuánta información contiene una imagen y cómo está organizada**.

---

# 5. Digitalización

Una imagen del mundo real puede considerarse inicialmente como información continua.

Para representarla en una computadora es necesario **digitalizarla**.

Este proceso está relacionado principalmente con dos conceptos:

```text
Digitalización
     │
     ├── Muestreo
     │
     └── Cuantización
```

---

## 5.1 Muestreo — Sampling

El **muestreo** está relacionado con la discretización de las posiciones espaciales de la imagen.

Conceptualmente podemos pensar:

```text
Escena continua
      ↓
Tomar muestras espaciales
      ↓
Cuadrícula de píxeles
```

Un mayor número de muestras permite representar más posiciones espaciales de la imagen.

Por eso este concepto está relacionado con la cantidad de píxeles disponibles para representar una escena.

---

## 5.2 Cuantización — Quantization

La **cuantización** se relaciona con los valores que puede tomar cada píxel.

Por ejemplo, una imagen puede representarse utilizando:

```text
256 niveles
```

o reducirse conceptualmente a:

```text
8 niveles
```

o incluso:

```text
4 niveles
```

Al reducir la cantidad de niveles posibles, también disminuye la precisión con la que representamos las variaciones de intensidad de la imagen.

Una forma sencilla de recordarlo es:

```text
Muestreo     → ¿Dónde están los píxeles?
Cuantización → ¿Qué valores pueden tomar?
```

---

# 6. Resolución

La resolución está relacionada con la cantidad y densidad espacial de información utilizada para representar una imagen.

Una mayor resolución espacial permite representar detalles más pequeños.

Esto explica por qué, al reducir excesivamente el tamaño de una imagen, eventualmente comenzamos a distinguir claramente sus píxeles.

---

# 7. Intensidad

Cada píxel contiene información numérica.

En una imagen de escala de grises podemos pensar en:

```text
I(x, y)
```

donde `I` representa la intensidad correspondiente al píxel situado en `(x, y)`.

Para una imagen típica de 8 bits:

```text
I(x, y) ∈ [0, 255]
```

Estos valores numéricos permiten realizar operaciones matemáticas sobre la imagen.

---

# 🔍 ¿Qué debemos observar al ejecutar `cargar_imagen.ipynb`?

Al trabajar con el notebook es importante no limitarse a observar que “la imagen aparece”.

Debemos preguntarnos:

### 1. ¿La imagen se cargó correctamente?

Verificar visualmente que el archivo leído sea el esperado.

---

### 2. ¿Qué tipo de objeto creó Python?

Observar cómo la librería utilizada representa internamente la imagen.

---

### 3. ¿Cuáles son sus dimensiones?

Identificar:

```text
alto
ancho
canales
```

cuando corresponda.

---

### 4. ¿Cómo podemos acceder a un píxel?

Examinar una posición específica permite conectar la teoría:

```text
Pixel (x, y)
```

con su representación dentro del programa.

---

### 5. ¿Qué valores encontramos?

Los valores permiten comenzar a comprender que la imagen que vemos en pantalla está formada por información numérica.

---

# 🌗 Relación con brillo

El brillo de una imagen está directamente relacionado con los valores de intensidad de sus píxeles.

Conceptualmente:

```text
Aumentar intensidad
        ↓
Imagen más clara
```

y:

```text
Disminuir intensidad
        ↓
Imagen más oscura
```

En imágenes de 8 bits debemos mantener los valores dentro del rango:

```text
0 ≤ intensidad ≤ 255
```

Esta es una de las razones por las que resulta tan importante comprender primero cómo se representan los píxeles.

---

# ◐ Relación con contraste

El contraste representa la diferencia entre intensidades claras y oscuras.

Una imagen con mayor contraste presenta diferencias más marcadas entre distintas regiones.

Una imagen con menor contraste presenta intensidades más similares y puede verse más uniforme.

Para poder modificar el contraste primero necesitamos comprender los valores de intensidad almacenados en la imagen.

---

# 📊 Relación con el histograma

El histograma permite estudiar **cómo se distribuyen las intensidades de una imagen**.

En una imagen de escala de grises podemos contar cuántos píxeles poseen cada intensidad:

```text
Intensidad → cantidad de píxeles
```

Por ejemplo:

```text
0      → ███
50     → █████
100    → █████████
150    → ██████
200    → ███
255    → █
```

Esto permite analizar numéricamente características relacionadas con:

* iluminación;
* brillo;
* contraste;
* distribución de intensidades.

Por lo tanto:

```text
Cargar imagen
      ↓
Obtener píxeles
      ↓
Obtener intensidades
      ↓
Contar intensidades
      ↓
Construir histograma
```

---

# 📈 Ecualización de histograma

Una aplicación posterior del histograma es la **ecualización**.

Su objetivo es redistribuir los valores de intensidad para modificar o mejorar el contraste de una imagen.

Conceptualmente:

```text
Imagen
   ↓
Calcular histograma
   ↓
Calcular distribución acumulada
   ↓
Normalizar
   ↓
Reasignar intensidades
   ↓
Nueva imagen
```

Este procedimiento será mucho más fácil de comprender después de dominar:

* píxeles;
* intensidad;
* matrices;
* histogramas.

---

# 🔗 Conexión entre los conceptos

Una forma útil de estudiar esta parte del curso es verla como una cadena:

```text
Imagen del mundo real
        ↓
Digitalización
        ↓
 ┌───────────────┐
 │               │
Muestreo     Cuantización
 │               │
 ↓               ↓
Posiciones     Intensidades
discretas       discretas
 │               │
 └───────┬───────┘
         ↓
       Píxeles
         ↓
  Matriz de imagen
         ↓
   Cargar en Python
         ↓
  Analizar valores
         ↓
 ┌───────┼─────────┐
 ↓       ↓         ↓
Brillo Contraste Histograma
                   ↓
              Ecualización
```

Esta relación es uno de los puntos más importantes del laboratorio.

---

# 🧪 ¿Qué podemos experimentar?

Una vez que el notebook funcione correctamente, podemos repetir el procedimiento utilizando diferentes imágenes del repositorio.

Por ejemplo:

```text
gato_carpintero.jpg
gato_con_pelotitas.jpg
gato_mono.bmp
gato.bmp
llama.jpg
```

Podemos comparar:

* dimensiones;
* formato;
* cantidad de canales;
* valores de píxeles;
* apariencia visual;
* representación numérica.

---

# 📁 Estructura del laboratorio

La carpeta puede verse aproximadamente así:

```text
Sem1_PDI/
│
├── README.md
├── cargar_imagen.ipynb
│
├── gato_carpintero.jpg
├── gato_con_pelotitas.jpg
├── gato_mono.bmp
├── gato.bmp
├── llama.jpg
│
├── histograma.ipynb
├── operaciones_matrices.ipynb
├── pdi_vision.ipynb
└── Pixel importance.ipynb
```

---

# ⚙️ Requisitos

Para ejecutar este laboratorio se recomienda tener:

* Python 3;
* Visual Studio Code;
* extensión de Jupyter para VS Code;
* Jupyter Notebook;
* las librerías utilizadas por el notebook.

Entre las librerías comúnmente utilizadas en estos ejercicios pueden encontrarse:

```bash
pip install numpy matplotlib pillow opencv-python
```

Solo es necesario instalar las que realmente utilice el notebook.

---

# ▶️ Cómo ejecutar el laboratorio

## 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

---

## 2. Entrar a la carpeta

```bash
cd Sem1_PDI
```

---

## 3. Abrir el proyecto en VS Code

```bash
code .
```

---

## 4. Abrir el notebook

Seleccionar:

```text
cargar_imagen.ipynb
```

---

## 5. Seleccionar el kernel

En la parte superior del notebook seleccionar un entorno de **Python** que tenga instaladas las dependencias necesarias.

---

## 6. Ejecutar las celdas

Ejecutar las celdas de arriba hacia abajo.

Se puede utilizar:

```text
Shift + Enter
```

o el botón:

```text
▶ Run
```

---

# ⚠️ Errores comunes

## `FileNotFoundError`

Significa que Python no encontró la imagen.

Verificar:

* nombre del archivo;
* extensión;
* ruta;
* carpeta desde la cual se está ejecutando el notebook.

---

## `ModuleNotFoundError`

Indica que falta instalar alguna librería.

Por ejemplo:

```bash
pip install numpy
```

---

## Kernel incorrecto

Si una librería está instalada pero Jupyter no logra encontrarla, comprobar que el notebook esté utilizando el entorno correcto de Python.

---

# 📝 Preguntas de repaso

Después de ejecutar el laboratorio deberíamos ser capaces de responder:

1. ¿Qué es un píxel?
2. ¿Cómo se representa una imagen digital?
3. ¿Qué representa la posición `(x, y)`?
4. ¿Qué es la intensidad de un píxel?
5. ¿Qué significa que una imagen tenga valores entre `0` y `255`?
6. ¿Qué información nos entregan las dimensiones de una imagen?
7. ¿Cuál es la diferencia entre muestreo y cuantización?
8. ¿Cómo se relaciona la resolución con los píxeles?
9. ¿Por qué podemos tratar una imagen como una matriz?
10. ¿Cómo se relacionan los valores de intensidad con el brillo?
11. ¿Qué representa el contraste?
12. ¿Qué información entrega un histograma?
13. ¿Por qué debemos aprender a cargar una imagen antes de aplicar procesamiento sobre ella?

---

# ✅ Checklist de estudio

Antes de considerar terminado este laboratorio, debería poder explicar con mis propias palabras:

* [ ] Qué es una imagen digital.
* [ ] Qué es un píxel.
* [ ] Qué representa `(x, y)`.
* [ ] Qué significa intensidad.
* [ ] Cómo se representa una imagen como matriz.
* [ ] Qué significan las dimensiones de una imagen.
* [ ] Qué es muestreo.
* [ ] Qué es cuantización.
* [ ] Qué relación existe entre resolución y píxeles.
* [ ] Qué relación existe entre intensidad y brillo.
* [ ] Qué significa contraste.
* [ ] Qué representa un histograma.
* [ ] Para qué sirve la ecualización de histograma.
* [ ] Cómo cargar y visualizar una imagen utilizando Python.

---

# 🚀 ¿Qué sigue?

Este laboratorio sirve como base para continuar con temas como:

```text
Carga de imágenes
       ↓
Píxeles e intensidades
       ↓
Operaciones con matrices
       ↓
Brillo y contraste
       ↓
Histogramas
       ↓
Ecualización
       ↓
Procesamiento digital de imágenes
```

La idea principal es dejar de pensar en una imagen únicamente como algo visual y comenzar a interpretarla también como **información numérica que podemos analizar y transformar**.

---

## 📌 Idea para recordar

> Una imagen digital es una representación discreta de información visual formada por píxeles cuyos valores pueden analizarse y modificarse numéricamente.

Comprender esta idea es la base para los siguientes laboratorios de Procesamiento Digital de Imágenes y Visión por Computadora.
