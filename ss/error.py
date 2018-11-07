import os

"""
Error v 0.1
Autor: Enrique Nieto Martínez
Fecha: 31/10/2018
La clase ayuda a desplegar errores, de forma sencilla
con opción de mostrar los datos de soporte

"""

class Error(object):
	message = ""
	error_type = ""
	support_data = ""
	show_support_data = True
	display_type = "console"


	def __init__(self):
		# print("Error init")
		pass


	def show(self, message):
		self.message = message
		if(self.display_type == "console"):
			if(self.show_support_data):
				print("### Error "+self.error_type+" ###: "+self.message+"\n"+self.support_data)
			else:
				print("### Error "+self.error_type+" ###: "+self.message)

# er = Error()
# er.error_type = "Hola"
# er.show_support_data = False
# er.support_data = "Por favor contacte a soporte: \n Contacto: Enrique Nieto \n Corta: 23930 \n Oficina: (0155)51404900 Ext. 23972 \n WhatsApp: (55)12657501 \n E-mail: enrique.nieto@milenio.com"
# er.show("lor")