from ftplib import FTP
from ftplib import all_errors
import json

def common_utils_test():
	print("common_utils_test ok")

def ftp_download(item,conf):
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


# Cargar la configuración 
def load_conf(conf_file):
	# json_data=open(conf_file).read()
	with open(conf_file) as json_file:
		json_data = json_file.read()
		
	conf = json.loads(json_data)	
	return conf