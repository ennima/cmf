from ftplib import FTP
from ftplib import all_errors
import json
import os
def common_utils_test():
	print("common_utils_test ok")

def percentage(max_value,eval_value):
	return (eval_value * 100) / max_value

def ftp_download(item,conf):
	""" Download media by FTP """
	tiempo_inicial = time_i()
	ftp = FTP(conf["origin_ftp_server"]["host"])
	print(ftp.login(conf["origin_ftp_server"]["user"],conf["origin_ftp_server"]["pass"]))
	print(ftp.pwd())
	# ftp.retrlines('LIST')
	ftp.cwd(item["folder"])
	print("Descargando: "+item["clip"])
	try:
		ftp.retrbinary('RETR '+item["clip"], open(item["clip"], 'wb').write)
		download_success = True
	except all_errors as e:
		print(e)

	ftp.quit()
	tiempo_final = time_i()
	tiempo_ejecucion = tiempo_final - tiempo_inicial
	print("Tardó: " , tiempo_ejecucion,"s")
	print(seconds_timestamp(tiempo_ejecucion))
	return tiempo_ejecucion

def ftpSend(host,user,passs,destFolder,newFile):
	""" Send media by FTP """
	return_value = False
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
			print ("Enviando ",os.path.basename(newFile) ,"a destino FTP...")
			try:
				ftp.storbinary('STOR '+os.path.basename(newFile),open(newFile,'rb'))
			except ftplib.error_temp as e:
				print("Error al enviar el archivo:", e)
			else:
				
				print ("Listo.")
				return_value = True

			finally:
				ftp.quit()
			
		finally:
			pass

	finally:
		pass

	return return_value


# Cargar la configuración 
def load_conf(conf_file):
	if(os.path.exists(conf_file)):
		with open(conf_file) as json_file:
			json_data = json_file.read()
			
		conf = json.loads(json_data)
	else:
		conf = False	
	return conf

def find_conf_value(key_conf, conf):
	""" Check that one value are in conf """
	if(key_conf in conf.keys()):
		return conf[key_conf]
	else:
		print("## Error: Se requiere valor: " + key_conf)
		return False

def validate_conf_data(required_keys, conf):
	""" Check that all values are in conf """
	return_val = True
	for key_conf_req in required_keys:
			if(find_conf_value(key_conf_req, conf) == False):
				return_val = False

	return return_val
