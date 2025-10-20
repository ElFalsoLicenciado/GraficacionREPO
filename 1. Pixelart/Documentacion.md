Para esta actividad, se tiene que crear una imagen tipo pixel en escala de grises (1 canal). El rango de valores es de 0 a 255 (de 8 bits).


Primero lo primero, se importan las librerias:
```python
    import cv2 as cv
    import numpy as np
    from PIL import Image
    import os
```

- *cv2* es *opencv* que nos ayuda para la edicion de la imagen.
- *numpy* es una libreria que nos facilita la vida con matrices y vectores.
- *PIL* no es esencial pero me sirve para crear una imagen que guarde el resultado final.

