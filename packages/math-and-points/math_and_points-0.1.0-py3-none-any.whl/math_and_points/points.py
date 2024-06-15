

class Punto:
	def __init__(self,x,y):
		self._x=x
		self._y=y
	def __str__(self):
		return f"({self._x},{self._y})"
	@property
	def x(self):
		return self._x
	@x.setter
	def x(self,valor):
		self._x=valor

	@property
	def y(self):
		return self._y
	@y.setter
	def y(self,valor):
		self._y=valor
	def __add__(self,otro):
		return Punto(self._x+otro._x,self._y+otro._y)
	def __mul__(self,otro):
		return self._x*otro._x+self._y*otro._y

	def __truediv__ (self,otro):
		return (otro._y-self._y)/(otro._x-self._x) if otro._x-self._x != 0 else "La pendiente es infinita" 

def punto(a,b):
	return Punto(a,b)

def suma_p(puntoA,puntoB):
	return puntoA + puntoB

def producto_punto(puntoA,puntoB):
	return puntoA * puntoB

def pendiente(puntoA,puntoB):
	return puntoA / puntoB


