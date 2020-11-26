import NNTerminalclass Ep(NNTerminal):
	#diccionario<NombreClase, Objeto >
	def __init__(self):
		super().__init__('Ep')
		self.prod['+'] = None
		self.prod['T'] = None
		self.prod['Ep'] = None
		self.prod['-'] = None
		self.prod['T'] = None
		self.prod['Ep'] = None
		self.prod['lambda'] = None
	def interpret(self,anterior):
		if self.prod['+'] != None:
			return self.prod['T'].interpret() + self.prod['Ep'].interpret()
		elif self.prod['-'] != None:
			return (-self.prod['T'].interpret())+self.prod['Ep'].interpret()
		else:
			return 0