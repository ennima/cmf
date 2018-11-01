import os


te_path = os.getenv('APPDATA')
te1_path = os.getenv('PROGRAMDATA')
print(te_path,"----",te1_path)

file_txt = te_path + "te.txt"

# if(os.path.exists(file_txt)):
# 	print("Existe") 
# else:
# 	print("No Existe")


def read_te(te_location,deadth):
	au = 0
	if(os.path.exists(te_location)):
		print("Existe")
		with open(te_location,"r") as texto:
			data = texto.read()

		if(data ==  ""):
			print("Vacío")
		else:
			au = int(data,2)
			if(au >= deadth):
				print("###  Muerte Read  ###") 

		print("data:", data)
	else:
		print("No Existe")

	return au


def write_te(te_location, increment, deadth):


	u = bin(read_te(te_location,deadth))

	print(u)

	a = int(u,2)
	print(a)

	if(a >= deadth):
		print("###  Muerte  ###")
	b = a + increment

	nu = bin(b)
	# print(nu)


	with open(te_location,"w") as texto:
		texto.write(nu)


step = 7000003 * 1000000 * 666
deadth = (step) * 15
print(deadth)
bin_death = bin(deadth)
# print(bin_death)
# print(len(str(bin_death)))
write_te(file_txt,step, deadth)