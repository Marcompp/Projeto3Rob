class priorityq:
	def __init__(self):
		self.lista = []


	def put(self,valor,prioridade):
		self.lista.append((valor,prioridade))

	def get(self):
		tirardo = -1
		menor = 1000000000
		for a in range(len(self.lista)):
			leng = len(self.lista)
			if self.lista[leng-a-1][1] < menor:
				tirardo = leng-a-1
				menor = self.lista[leng-a-1][1]
		valorf = self.lista[tirardo][0]
		del(self.lista[tirardo])
		return valorf

	def empty(self):
		if self.lista == []:
			return True
		else:
			return False