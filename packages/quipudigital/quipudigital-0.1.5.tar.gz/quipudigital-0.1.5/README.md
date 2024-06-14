# Quipudigital

Una biblioteca de visualización de Quipus con Python

# Estructura del Proyecto

```
|--quipudigital/        <-- Archivos de python
|     |--assets/        <-- archivos GIF para construir un quipu
|
|--setup.py             <-- Define el Python build
```

# Uso

Un ejemplo de como usar la biblioteca

```
import quipudigital.main as qd
```

```
numbers =[1000, 2024, 1234 , 5234, 120, 1000]

quipu = qd.Quipu(numbers,x0=-300,y0=110)

quipu.screen.setup(width=0.59, height=0.99)  

quipu.draw()
```
<p align="center">
    <img  width="75%" src="https://raw.githubusercontent.com/jgomezz/quipudigital/main/quipu.png">
</p>
