class NTerminal:
	val = 0
	etiqueta = 
	padre = None
	siguiente = None
	def __init__(self,etiqueta):
		self.padre=None
		self.etiqueta=etiqueta
		self.val=0
		self.siguiente = None