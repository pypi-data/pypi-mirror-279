class curso:
	def __init__(self, name, duration, link):
		self.name=name
		self.duration=duration
		self.link=link

	def __repr__(self):
		return f"{self.name} : {self.duration} horas y link : {self.link}"


cursos = [
	curso("Introduccion a Linux" ,15, "https://www.mhbol.com"),
	curso("Personalizacion", 3, "https://www.sicbol.com"),
	curso("Hacking", 53,"https://www.eldeber.com.bo")
]

def lista_cursos():
	for curso in cursos:
		print(curso)

def search_by_name(name):
	for curso in cursos:
			if curso.name ==name:
				return curso
	return None

