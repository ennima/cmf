import os
from cmf import *
# import pandas as pd
# import numpy as np

print("hola")

data_path = "\\\\192.168.196.59\\c$\\Users\\Ingest\\Documents\\dev\\data\\"
file_csv = "stratus_report_out_19072018.csv"
count = 0
with open(data_path+file_csv) as csv:
	data = csv.readlines()

for linea in data:
	# print(linea)
	if("051018" in linea):
		print(linea)
		# break
# if(os.path.exists(data_path)):
# 	print("existe")

# 	for root, dirs, files in os.walk(data_path, topdown=False):
# 		for name in files:
# 			if("report" in name):
# 				print(name)
# 				count += 1
# 	print("Total:",count)


# bd7572d01d6840c8bdbb112ced555a14
# c89380e8e961438f8b94e60de4635e67 ---
# 833f3dbf0fd44146930b077949b21c6c


# stratus_path = "V:\\media\\Especiales Noticias\\"

# if(os.path.exists(stratus_path)):
# 	print("existe: ", stratus_path)
# 	print("existe: ", stratus_path)
# 	for root, dirs, files in os.walk(stratus_path, topdown=False):
# 		for name in dirs:
# 			cmf = root+"\\"+name
# 			if("ABEJAS UNAM 051018" in name):
# 				print("---------------------------------Si está------------------")
# 				break

# 			# print(root)
# 			cmf_path = ""
# 			if (root[-1:] == "\\"):
# 				# print(root+name)
# 				cmf_path = root+name
# 			else:
# 				# print(root+"\\"+name)
# 				cmf_path = root+"\\"+name
# 			# if(os.path.exists(cmf_path)):
# 			# 	pass
# 			# 	# print("Existe: ", cmf_path)
				
# 			# 	# my_cmf1 = Cmf(cmf)
# 			# 	# if(my_cmf1._is_xml_load):
# 			# 	# 	print("revisando:",cmf)
# 			# 	# 	id = my_cmf1.get_asset_id()
# 			# 	# 	# print(id)
# 			# 	# 	if("863f9f09c57849d3b2183aa44762a9d2" in id):
# 			# 	# 		print("----------- Encontrado:",cmf)
# 			# 	# 		break

# 			# 	# else:
# 			# 	# 	# print("Corrupto")
# 			# 	# 	pass
# 			# else:
# 			# 	print("No es un CMF")
# 	print("----------------FIN--------------")		



# cmf = "X:\\Recup\\ENTREVISTA REBECA DE ALBA\\ENTREVISTA REBECA DE ALBA(2).cmf"
# my_cmf1 = Cmf(cmf)
# print(my_cmf1.get_construction())