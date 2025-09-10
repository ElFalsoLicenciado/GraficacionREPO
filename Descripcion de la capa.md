# Documentación del programa: La capa de invisibilidad del Harry

Empezamos con nuestros *imports* básicos:

```python
import cv2
import numpy as np
```

Siendo las libreria para las matrices **numpy** y **cv2** para la visión artificial.

Con la siguiente linea de código agregamos una variable para **capturar vídeo** con nuestra **cámara web**. Y la última línea se pone en espera para estabilizar (evitar potenciales errores o bajones de rendimiento).

```python
cap = cv2.VideoCaptura(0)

cv2.waitKey(2000)
```
Ahora, se guarda el primer fotograma que se usará como el fondo para la capa. La condición *if* es para asegurarnos que no haya ocurrido ningún error en la captura de ese fotograma.

```python
ret, background = cap.read()
if not ret:
    print("Error al capturar el fondo.")
    cap.release()
    exit()
```

Mientras la camara está encencida la variable **frame** ira guardando un fotograma, esto se va ir haciendo en un ciclo *while* de forma indefinida hasta que el usuario decida terminar el programa. Si **ret** es nulo entonces se termina el ciclo.

```python
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
```

**hsv** guarda la conversión de la imagen de RGB al modelo HSV para siquiera poder realizar las operaciones de manejo de pixeles con facilidad. Ahora las 2 últimas variables serán nuestras matrices, la primera matriz son los verdes más obscuros o inferiores y la segunda los verdes más claros.


Cada matriz tiene 3 valores o 3 dimensiones esto nos servira para definir el rango de color para detectar nuestro capa, el primer numero de cada matriz se refiere al **Hue** o tono. El segundo numero es **Saturation** o saturación, esto define que tan claro queremos el color. Finalmente, el tercer número es **Brightness** o brillo para que tan obscuro queremos el color. 

```python
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 20, 20])
    upper_green = np.array([90, 255, 255])
```

Creamos una máscara tomando al cuadro **hsv** para guardar los pixeles verdes.

```python
    mask = cv2.inRange(hsv, lower_green, upper_green)
```

Invertimos la máscara, entonces los pixeles verdes que se habian guardado como pixeles negros pasan a ser blancos, mientras que los otros colores se guardaban como blanco.

```python
    mask_inv = cv2.bitwise_not(mask)
```

**res1** es la combinacion del la captura del video más la máscara de blancos y negros esto para tener en cuenta los pixeles del color que nos interesa que serán sustituidos. Digamos que donde hay el color que nos interesa hay un *agujero negro*.

**res2** será la combinación del fotograma guardado al principio que servirá de fondo y la máscara original del color elegido. Donde se localizan los verdes se guardan los pixeles del fotograma.

```python
    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    res2 = cv2.bitwise_and(background, background, mask=mask)
```

Combinamos ambas imagenes en una solo y vuala.

```python
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) 
    cv2.imshow("Capa de Invisibilidad", final_output)
    cv2.imshow('mask', mask)

```