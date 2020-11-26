class NNTerminal:
	prod = {}
	etiqueta = 
	padre = None
	siguiente = None
	def __init__(self,etiqueta):
		self.padre=None
		self.etiqueta=etiqueta
		self.prod={}
		self.siguiente = None
	def imprimir(self):
		pivote=self
		while(True):
			if(len(pivote.hijos)>0):
				print(pivote.etiqueta,"->",end='')
				for h in pivote.hijos:
					print(,h.etiqueta,end='')
				print()
			if(len(pivote.hijos)>0):
				pivote=pivote.hijos[0]
			elif(pivote.siguiente!=None):
				pivote=pivote.siguiente
			else:
				while(pivote.siguiente==None):
					if(pivote.padre==None):
						return
					pivote=pivote.padre
				pivote=pivote.siguiente