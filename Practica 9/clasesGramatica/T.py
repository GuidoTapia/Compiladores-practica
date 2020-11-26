import NNTerminalclass T(NNTerminal):
	#diccionario<NombreClase, Objeto >
	def __init__(self):
		super().__init__('T')
		self.prod['F'] = None
		self.prod['Tp'] = None
	def interpret(self):
		return self.prod['F'].interpret()*self.prod['Tp'].interpret()