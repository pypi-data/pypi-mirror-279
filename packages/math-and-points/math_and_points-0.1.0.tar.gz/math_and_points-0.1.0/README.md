# math_and_points library

Una biblioteca para realizar operaciones basicas como suma,resta,multiplicacion y division, pasando como parametros dos o mas numeros. Por otro lado operaciones con puntos en dos dimensiones como suma, resta, producto punto y la pendiente.

## Instalacion

Instala el paquete utilizando 'pip3':

```python3
pip3 install math_and_points
```
## Uso basico

### Operaciones aritmeticas basicas

```python
from math_and_points import suma,resta,multiplicacion,division
print(suma(1,2,3,4)) #1+2+3+4
print(resta(1,2,3,4)) #1-2-3-4
print(multiplicacion(1,2,3,4)) #1*2*3*4
print(division(1,2,3,4)) #1/2/3/4
```
### Operaciones con puntos

```python
rom math_and_points import punto,producto_punto,pendiente,suma_p
puntoA = punto(1,2)
puntoB = punto(3,4)
print(suma_p(PuntoA,puntoB))
print(producto_punto(PuntoA,puntoB))
print(pendiente(PuntoA,puntoB))
```
