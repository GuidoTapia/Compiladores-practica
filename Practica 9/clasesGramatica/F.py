import NNTerminalclass F(NNTerminal):
	#diccionario<NombreClase, Objeto >
	def __init__(self):
		super().__init__('F')
		self.prod['('] = None
		self.prod['E'] = None
		self.prod[')'] = None
		self.prod['num'] = None
		self.prod['id'] = None
	def interpret(self,anterior):
		if self.prod['E'] != None:
			return self.prod['E'].interpret()
		else:
			return self.prod['num'].interpret()