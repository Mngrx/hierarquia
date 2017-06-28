SIZEpag = 10
SIZEbloc = 20

class Disco:

	def __init__(self):
		self.paginas = list()
		count = 0
		for i in range(0, 30):
			aux = []
			for j in range(8):
				aux.append([count, count])
				count += 1
			self.paginas.append(aux)
		#print(self.paginas)	
	def retornarPagina(self, endereco):
		for i in range(0,30):
			for j in range(0, 8):
				if self.paginas[i][j][0] == endereco:
					return self.paginas[i]
	def atualizarPalavra(self, word, endereco):
		i = int(endereco / 8) 
		j = endereco % 8
		#print(j)
		self.paginas[i][j][1] = word
	def print(self):
		print("Disco: \n")
		for i in range(30):
			print("Página #%d:" % i)
			print(self.paginas[i])


class Memoria:
	def __init__(self):
		self.paginas = list()
		self.blocos = list()
		self.numpag = 0
		self.numbloc = 0
	def receberPagina(self, page):
		tmp = [page, 0]
		if (SIZEpag == self.numpag):
			aux = -1
			count = 0
			posi = 0
			for i in self.paginas:
				if i[1] < aux or aux == -1:
					aux = i[1]
					posi = count
				count += 1
			self.paginas[posi] = tmp
		else:
			self.paginas.append(tmp)
			self.numpag += 1

		aux1 = []
		aux2 = []

		
		for i in range(4):
			aux1.append(page[i])
			aux2.append(page[i+4])

		bl1 = [aux1, 0]
		bl2 = [aux2, 0]

		
		if (SIZEbloc > self.numbloc):
			self.blocos.append(bl1)
			self.blocos.append(bl2)
			self.numbloc += 2
		else:
			aux = -1
			count = 0
			posi = 0
			for i in self.blocos:
				if i[1] < aux or aux == -1:
					aux = i[1]
					posi = count
				count += 1
			self.blocos[posi] = bl1
			aux = -1
			count = 0
			posi = 0
			for i in self.blocos:
				if (i[1] < aux or aux == -1) and i != bl1:
					aux = i[1]
					posi = count
				count += 1
			self.blocos[posi] = bl2



	def retornarBloco(self, endereco):
		for i in self.blocos:
			for j in i[0]:
				if j[0] == endereco:
					i[1] += 1
					return i[0]
		return "false"

	def atualizarPalavra(self, word, endereco):
		for i in self.blocos:
			for j in i[0]:
				if j[0] == endereco:
					i[1] += 1
					j[1] = word
					break
		for i in self.paginas:
			for j in i[0]:
				if j[0] == endereco:
					i[1] += 1
					j[1] = word
					break
					return "true"
		return "false"
	def printPaginas(self):
		print("Memória: \n")
		for i in range(self.numpag):
			print("Página #%d:" % i)
			print(self.paginas[i][0])
	def printBlocos(self):
		print("Memória: \n")
		for i in range(self.numbloc):
			print("Bloco #%d:" % i)
			print(self.blocos[i][0])
		

class Cache:
	
	def __init__(self, tipo):
		self.blocos = list();
		self.numbloc = 0;
		if tipo == 2: self.SIZE = 5;
		elif tipo == 1: self.SIZE = 2;
	
	def receberBloco(self, bloco):
		tmp = [bloco, 0]
		if self.numbloc == self.SIZE:
			aux = -1
			count = 0
			posi = 0
			for i in self.blocos:
				if i[1] < aux or aux == -1:
					aux = i[1]
					posi = count
				count += 1
			self.blocos[posi] = tmp
		else:
			self.blocos.append(tmp)
			self.numbloc += 1

	def retornarBloco(self, endereco):
		for i in self.blocos:
			for j in i[0]:
				if j[0] == endereco:
					i[1] += 1
					return i[0]
		return "false"

	def atualizarPalavra(self, word, endereco):
		for i in self.blocos:
			for j in i[0]:
				if j[0] == endereco:
					i[1] += 1
					j[1] = word
					break
		return "false"

	def retornarPalavra(self, endereco):
		if self.blocos == []:
			return "false"


		for i in self.blocos:
			for j in i[0]:
				if j[0] == endereco:
					i[1] += 1
					return j[1]

		return "false"

	def print(self):
		if self.SIZE == 2:
			print("Cache L1: \n")
		else:
			print("Cache L2: \n")
		for i in range(self.numbloc):
			print("Bloco #%d:" % i)
			print(self.blocos[i][0])


class Core:
	
	def __init__(self):
		self.cache = Cache(1)

		


class Gerencia:
	
	def __init__(self, cores):
		self.disco = Disco()
		self.memoria = Memoria()
		self.organiza = []
		tmp = int(cores/2)
		for i in range(tmp):
			self.organiza.append([Cache(2), [Core(), Core()]])

	def leitura(self, core, endereco):
		aux = int(core/2)
		tmp = core % 2
		proc = self.organiza[aux][1][tmp]
		
		
		if (proc.cache.retornarPalavra(endereco) == "false" and self.organiza[aux][0].retornarPalavra(endereco) == "false" and self.memoria.retornarBloco(endereco) == "false"):
			pagina = self.disco.retornarPagina(endereco)
			self.memoria.receberPagina(pagina)
			bloco = self.memoria.retornarBloco(endereco)
			self.organiza[aux][0].receberBloco(bloco)
			proc.cache.receberBloco(bloco)
			return bloco
		elif(proc.cache.retornarPalavra(endereco) == "false"and self.organiza[aux][0].retornarPalavra(endereco) == "false"):
			bloco = self.memoria.retornarBloco(endereco)
			self.organiza[aux][0].receberBloco(bloco)
			proc.cache.receberBloco(bloco)
			return bloco
		elif(proc.cache.retornarPalavra(endereco) == "false"):
			bloco = self.organiza[aux][0].retornarBloco(endereco)
			proc.cache.receberBloco(bloco)
			return bloco
		else:
			return proc.cache.retornarPalavra(endereco)
		
	def escrita(self, core, word, endereco):
		aux = int(core/2)
		tmp = core % 2
		proc = self.organiza[aux][1][tmp]

		if (proc.cache.retornarPalavra(endereco) == "false" and self.organiza[aux][0].retornarPalavra(endereco) == "false" and self.memoria.retornarBloco(endereco) == "false"):
			self.disco.atualizarPalavra(word, endereco)
			pagina = self.disco.retornarPagina(endereco)
			self.memoria.receberPagina(pagina)
			bloco = self.memoria.retornarBloco(endereco)
			self.organiza[aux][0].receberBloco(bloco)
			proc.cache.receberBloco(bloco)
			#return proc.cache.retornarPalavra(endereco)
		elif(proc.cache.retornarPalavra(endereco) == "false"and self.organiza[aux][0].retornarPalavra(endereco) == "false"):
			self.disco.atualizarPalavra(word, endereco)
			self.memoria.atualizarPalavra(word, endereco)
			bloco = self.memoria.retornarBloco(endereco)
			self.organiza[aux][0].receberBloco(bloco)
			proc.cache.receberBloco(bloco)
			#return proc.cache.retornarPalavra(endereco)	
		elif(proc.cache.retornarPalavra(endereco) == "false"):
			self.disco.atualizarPalavra(word, endereco)
			self.memoria.atualizarPalavra(word, endereco)
			self.organiza[aux][0].atualizarPalavra(word, endereco)
			bloco = self.organiza[aux][0].retornarBloco(endereco)
			proc.cache.receberBloco(bloco)
			self.mudarCacheL2(word, endereco)
			#return proc.cache.retornarPalavra(endereco)
		else:
			self.disco.atualizarPalavra(word, endereco)
			self.memoria.atualizarPalavra(word, endereco)
			self.organiza[aux][0].atualizarPalavra(word, endereco)
			proc.cache.atualizarPalavra(word, endereco)
			self.mudarCacheL2(word, endereco)
			self.mudarCacheL1(word, endereco)

	def mudarCacheL2(self, word, endereco):
		for i in self.organiza:
			i[0].atualizarPalavra(word, endereco)
	def mudarCacheL1(self, word, endereco):
		for i in self.organiza:
			for j in i[1][j]:
				j.atualizarPalavra(word, endereco)

	def printDisco(self):
		self.disco.print()
	def printMemoriaBlocos(self):
		self.memoria.printBlocos()
	def printMemoriaPaginas(self):
		self.memoria.printPaginas()
	def printL2(self, numero):
		self.organiza[numero][0].print()
	def printL1(self, core):
		aux = int(core/2)
		tmp = core % 2
		proc = self.organiza[aux][1][tmp]
		proc.cache.print()


"""d = Disco()
#d.print()

aux = d.retornarPagina(88)

m = Memoria()
m.receberPagina(aux)

aux = m.retornarBloco(88)

c = Cache(2)

c.receberBloco(aux)

c.print()"""


print("Bem-vindo ao simulador de hierarquia de memória!!\n\n")

numCores = input("Por favor digite o número de cores (deve ser um número par): ")

gerenciador = Gerencia(int(numCores))


while 1:
	
	print("Tabela de comandos:\n>>> 1 - Escrita\n>>> 2 - Leitura\n>>> 3 - Imprimir alguma memoria\n>>> 4 - Encerrar execução")
	caso = int(input())

	if caso == 4:
		break
	if caso == 1:
		print("Operação de escrita, digite o core, a palavra e o endereço desejados, respectivamente.")
		core = int(input("Core: #"))
		palavra = int(input("Palavra: "))
		endereco = int(input("Endereço: "))
		gerenciador.escrita(core, palavra, endereco)
	if caso == 2:
		print("Operação de leitura, digite o core e o endereço desejados, respectivamente.")
		core = int(input("Core: #"))
		endereco = int(input("Endereço: "))
		print(gerenciador.leitura(core, endereco))
	if caso == 3:
		print("Imprimir qual memoria?\n>>> 1 - Disco\n>>> 2 - Memoria Principal\n>>> 3 - Cache L2\n>>> 4 - Cache L1")
		casoMem = int(input())
		if (casoMem == 1):
			gerenciador.printDisco()
		if (casoMem == 2):
			print("Imprimir páginas ou blocos?\n>>> 1 - Blocos\n>>> 2 - Páginas")
			testePrincipal = int(input())
			if testePrincipal == 2:
				gerenciador.printMemoriaPaginas()
			elif testePrincipal == 1:
				gerenciador.printMemoriaBlocos()
		if casoMem == 3:
			num = int(input("\nDigite o número da Cache L2: "))
			gerenciador.printL2(num)
		if casoMem == 4:
			num = int(input("\nDigite o número da Cache L1: "))
			gerenciador.printL1(num)




"""g = Gerencia(4)

print(g.leitura(3, 88))

g.escrita(3, 30, 5)

print(g.organiza[1][1][1].cache.blocos)

g.escrita(3, 50, 200)

g.leitura(3, 200)

print(g.organiza[1][1][1].cache.blocos)"""
