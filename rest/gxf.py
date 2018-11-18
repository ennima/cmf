import os, json, ftplib, pathlib, sys

def ftpSend(host,user,passs,destFolder,newFile):
	return_value = False

	# print("New File",newFile)
	passs = ""
	

	try:
		ftp = ftplib.FTP(host)
	except:
		print("No se pudo establecer conexión con el servidor FTP:",host)
	else:
		try:
			ftp.login(user,passs)
		except ftplib.error_perm as e:
			print("Error de login: ",e)
		else:
			ftp.cwd(destFolder)
			#print ftp.pwd()
			print ("Enviando ",os.path.basename(newFile) ,"a destino FTP...")
			try:
				ftp.storbinary('STOR '+os.path.basename(newFile),open(newFile,'rb'))
			except ftplib.error_temp as e:
				print("Error al enviar el archivo:", e)
			else:
				
				print ("Listo.")
				return_value = True

			finally:
				# print("Cerrando FTP...")
				ftp.quit()
			
		finally:
			pass

	finally:
		pass

	return return_value
	
def open_conf(open_path):
	# open_path = "conf.json"
	with open(open_path) as f:
		conf = json.load(f)
	return conf

def gxf_valid_name(gxf_path):
	# print(os.path.basename(gxf_path))
	extension = pathlib.Path(os.path.basename(gxf_path)).suffix
	# print(extension)
	# print(len(extension))
	is_ingestable = {"ingestable":False,"gxf_name":gxf_path}
	
	if(len(extension) == 0):
		is_ingestable["ingestable"] = True
		is_ingestable["gxf_name"] = gxf_path + ".gxf"

	elif(extension == ".gxf") or (extension == ".GXF"):
		# print("Cool")
		is_ingestable["ingestable"] = True
	else:
		print("El archivo no es media adecuada para ingestar")
		is_ingestable["ingestable"] = False
	
	return is_ingestable

def gxf_send(gxf_path,conf):

	is_gxf_valid_name = gxf_valid_name(gxf_path)
	if(is_gxf_valid_name["ingestable"]):
		
		stratus_obj = conf["stratus_ftp"]
		
		# validar la existencia del clip de origen
		if(os.path.exists(is_gxf_valid_name["gxf_name"])):
			# Enviar el clip
			send_gxf = ftpSend(stratus_obj["stratus_ftp"],stratus_obj["stratus_ftp_user"],stratus_obj["stratus_ftp_pass"],stratus_obj["ingest_folder"],is_gxf_valid_name["gxf_name"])
			if (send_gxf):
				print("Ingestado correctamente")
			else:
				print("No se pudo ingestar")
		else:
			print("No existe el GXF")
	else:
		print("GXF No valido")

def get_gxf_clip():
	gxf_path = ""
	if(len(sys.argv)>1):
		# print(sys.argv[1])
		gxf_path = sys.argv[1]
	else:
		# print("No args")
		gxf_path = input("Clip to restore:")

	return gxf_path



def main():
	conf1 = open_conf("conf.json")
	gxf_send(get_gxf_clip(),conf1)

if __name__ == '__main__':
	main()
	exit_string = input("Presiona cualquier tecla para terminar ...")