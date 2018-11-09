import os


from time import time as time_i
from time import sleep
from datetime import datetime


"""
Time Metrics v 0.1
Autor: Enrique Nieto Martínez
Fecha: 08/11/2018
La clase ayuda en la medición del tiempo de ejecución de un proceso

"""

class TimeMetrics(object):
	tiempo_inicial = ""
	tiempo_final = ""
	

	def __init__(self):
		pass

	def init(self):
		self.tiempo_inicial = time_i()

	def seconds_timestamp(self,seconds):
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)																																																																															
		restore_time = "%02d:%02d:%02d" % (h, m, s)
		# print ("Tardó:",restore_time)
		return(restore_time)        


	def get_elapsed_time(self):
		return_value = {}
		self.tiempo_final = time_i()
		tiempo_ejecucion = self.tiempo_final - self.tiempo_inicial
		# print("Tardó: " , tiempo_ejecucion,"s")
		return_value["seconds"] = tiempo_ejecucion
		return_value["string"] = self.seconds_timestamp(tiempo_ejecucion)
		return return_value

