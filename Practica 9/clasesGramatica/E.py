import NNTerminalclass E(NNTerminal):
	#diccionario<NombreClase, Objeto >
	def __init__(self):
		super().__init__('E')
		self.prod['T'] = None
		self.prod['Ep'] = None
	def interpret(self):
		return self.prod['T'].interpret()+self.prod['Ep'].interpret()