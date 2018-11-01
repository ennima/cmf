import os


"""
Death Counter v 0.1
Autor: Enrique Nieto Martínez
Fecha: 30/10/2018
La clase ayuda en la creación de un contador de bienestar de la aplicación

"""

class DeathCounter(object):
	step = 1
	max_step = 5
	death = step * max_step

	def __init__(self):
		print(self.death)

	def set_max_step(self,newStep):
		self.max_step = newStep

	def get_death(self)

dc = DeathCounter()