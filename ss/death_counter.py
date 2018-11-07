import os
from error import Error
import hashlib
"""
Death Counter v 0.1
Autor: Enrique Nieto Martínez
Fecha: 30/10/2018
La clase ayuda en la creación de un contador de bienestar de la aplicación

"""

class DeathCounter(object):
	installed_name = "installed.txt"
	installed_path = "."
	installed_open = 23
	installed_close = 10
	installed_factor = 100000
	counter_name = "counter.txt"
	counter_path = "."
	step = 1
	max_step = 5
	death = step * max_step
	installed = ""
	counter= ""
	er = Error()

	def __init__(self):
		# print(self.death)
		self.er.show_support_data = False
		self.er.support_data = "Por favor contacte a soporte: \n Contacto: Enrique Nieto \n Corta: 23930 \n Oficina: (0155)51404900 Ext. 23972 \n WhatsApp: (55)12657501 \n E-mail: enrique.nieto@milenio.com"
		# self.er.show("Test Error")

	def set_max_step(self,newStep):
		if(newStep > 1):
			self.max_step = newStep - 1
		else:
			self.max_step = 1

	def get_death(self):
		self.death = self.step * self.max_step
		return self.death

	def get_dependency(self, dependency_path):
		if(os.path.exists(dependency_path)):
			return True
		else:
			return False

	def get_hash_dependency(self,value):
		open_string = 0
		if(value == "open"):
			open_string = self.installed_open * self.installed_factor

		elif(value == "closed"):
			open_string = self.installed_close * self.installed_factor

		else:
			open_string_md5 = "none"

		open_string_md5 = hashlib.md5(str(open_string).encode('utf-8')).hexdigest()
		return open_string_md5

	def make_installed_dependency(self, value):
		if(value == "open"):
			# print("Making install Open")
			
			file_content = self.get_hash_dependency(value)
			# print("file_content:",file_content)
			with open(self.installed_path+"\\"+self.installed_name,"w") as installed_file:
				installed_file.write(file_content)

		elif(value == "closed"):
			file_content = self.get_hash_dependency(value)
			# print("file_content:",file_content)
			with open(self.installed_path+"\\"+self.installed_name,"w") as installed_file:
				installed_file.write(file_content)

		else:
			# print("Making install Close")
			self.er.show("Error 0x001")



	def read_installed_dependency(self):
		return_value = "none"
		dependency_file = self.installed_path+"\\"+self.installed_name
		if(self.get_dependency(dependency_file)):
			# print("Existe installed")
			with open(dependency_file,"r") as  d_file:
				data = d_file.read()

			# print(data)

			is_open = self.get_hash_dependency("open")
			is_closed = self.get_hash_dependency("closed")
			if(data == is_open):
				# print("Yeii trabajemos hoy :)")
				return_value = "open"

			elif(data == is_closed):
				# print("Se terminó tu poder sobre mi")
				return_value = "closed"
			else:
				# print("Se corrompió la dependencia installed")
				return_value = "corrupt"

		else:
			# print("Falta installed")
			self.make_installed_dependency("open")
			return_value = "open"

		return return_value

	def read_counter_dependency(self):
		return_value = "none"
		dependency_file = self.counter_path + "\\" +self.counter_name
		if(self.get_dependency(dependency_file)):
			# print("Existe Counter")

			# print(self.read_installed_dependency())

			is_installed = self.read_installed_dependency()
			if(is_installed == "closed"):
				with open(dependency_file,"w") as counter_file:
					counter_file.write(str(self.get_death()))

				return "death"

			elif(is_installed == "open"):
				with open(dependency_file,"r") as counter_file:
					count_data = counter_file.read()

				# print(count_data)
				if(int(count_data) >= self.get_death()):
					# print("Muerto")
					return_value = "death"
					is_installed = self.read_installed_dependency()
					if(is_installed == "open"):
						self.make_installed_dependency("closed")


				elif(int(count_data) < self.get_death()):
					# print("Vivo")
					count_content = str(int(count_data) + self.step)
					with open(dependency_file,"w") as counter_file:
						counter_file.write(count_content)
					return_value = "alive"

				else:
					self.er.show("Error 0x002")

			else:
				print("-----",is_installed)
		else:
			# print("No Counter")
			is_installed = self.read_installed_dependency()
			# print(is_installed)
			if(is_installed == "open"):
				# print("Open installed")
				# Make Counter first
				with open(dependency_file,"w") as counter_file:
					counter_file.write("0")

				return_value = "alive"

			elif(is_installed == "closed"):
				# print("closed installed")
				# Make counter full
				with open(dependency_file,"w") as counter_file:
					counter_file.write(str(self.get_death()))

			else:
				# print("Algo salió mal")
				# Error message
				self.er.show("Algo salió mal")

		return return_value

	def run_death_counter(self):
		is_installed = self.read_installed_dependency()
		is_counter = self.read_counter_dependency()

		return is_counter

dc = DeathCounter()
dc.step = 7000003 * 1000000 * 666
dc.set_max_step(100000)
# print("Installed: ",dc.read_installed_dependency())
# print("Counter: ",dc.read_counter_dependency())

for i in range(0,100003):
	print(str(i+1),"--",dc.run_death_counter())