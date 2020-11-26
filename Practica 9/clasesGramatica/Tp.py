import NNTerminalclass Tp(NNTerminal):
	#diccionario<NombreClase, Objeto >
	def __init__(self):
		super().__init__('Tp')
		self.prod['*'] = None
		self.prod['F'] = None
		self.prod['Tp'] = None
		self.prod['lambda'] = None
	def interpret(self,anterior):
		if self.prod['*'] != None:
			return self.prod['F'].interpret()*self.prod['Tp'].interpret()
		else:
			return 1