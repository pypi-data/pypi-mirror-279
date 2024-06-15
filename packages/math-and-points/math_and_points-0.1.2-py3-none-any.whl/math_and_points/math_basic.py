
from functools import reduce
def suma (*args):
	return sum(args)

def resta(*args):
	return reduce(lambda x,y:x-y,args)

def multiplicacion(*args):
	return reduce(lambda x,y:x*y,args)

def division(*args):
	return reduce(lambda x,y:x/y if y!=0 else 9999999,args)



