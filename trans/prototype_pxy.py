import os, shutil, json, sys
import subprocess
import ftplib

from time import time as time_i
from datetime import datetime


from time_metrics import *



sys.path.append('../ss')
from death_counter import *

def ftpSend(host,user,passs,destFolder,newFile):
	
	print("New File",newFile)
	passs = ""
	ftp = ftplib.FTP(host)
	ftp.login(user,passs)
	ftp.cwd(destFolder)
	#print ftp.pwd()
	print ("Enviando ",os.path.basename(newFile) ," a ftp Dest...")
	ftp.storbinary('STOR '+os.path.basename(newFile),open(newFile,'rb'))
	ftp.quit()
	print ("Listo.")


def transcode_media(clip,path,FinalVideo,render_engine, temp_dir, stratus_obj):
	print(FinalVideo)
	print(path)
	
	if(not "._" in clip) and (not ".textClipping" in clip):
		name_split = clip.strip().split(".")
		test = 0
		print(len(name_split))
		print(len(name_split[0].strip()))
		
		if(len(name_split[0].strip()) == 0):
			print("No lo hago ")
		else:
			print("#Transcodificando: ",clip.strip())
			
			if(os.path.exists(temp_dir)) and (test == 0):
				
				print("Existe el directorio de cache")
				if("." in path):
					if("." in temp_dir):
						videoMerge = render_engine+' -y -i "'+clip+'" -vcodec mpeg2video -vtag xd5b -s 1920x1080 -aspect 16:9 -pix_fmt yuv420p -rtbufsize 50000k -b:v 50000k -dc 9 -flags +ilme+ildct -top 1 -f mxf "'+FinalVideo+'".mxf'	
					else:
						videoMerge = render_engine+' -y -i "'+clip+'" -vcodec mpeg2video -vtag xd5b -s 1920x1080 -aspect 16:9 -pix_fmt yuv420p -rtbufsize 50000k -b:v 50000k -dc 9 -flags +ilme+ildct -top 1 -f mxf "'+temp_dir+FinalVideo+'".mxf'
				else:
					if("." in temp_dir):
				  
						videoMerge = render_engine+' -y -i "'+path+"\\"+clip+'" -vcodec mpeg2video -vtag xd5b -s 1920x1080 -aspect 16:9 -pix_fmt yuv420p -rtbufsize 50000k -b:v 50000k -dc 9 -flags +ilme+ildct -top 1 -f mxf "'+FinalVideo+'".mxf'

					else:
						videoMerge = render_engine+' -y -i "'+path+"\\"+clip+'" -vcodec mpeg2video -vtag xd5b -s 1920x1080 -aspect 16:9 -pix_fmt yuv420p -rtbufsize 50000k -b:v 50000k -dc 9 -flags +ilme+ildct -top 1 -f mxf "'+temp_dir+FinalVideo+'".mxf'
				print(videoMerge)
			   
				p = subprocess.Popen(videoMerge)
				p.wait()
				print("Enviando: "+temp_dir+FinalVideo)
				test += 1

				if("." in temp_dir):
					ftpSend(stratus_obj["stratus_ftp"],stratus_obj["stratus_ftp_user"],stratus_obj["stratus_ftp_pass"],stratus_obj["ingest_folder"],FinalVideo+'.mxf')
				else:
					ftpSend(stratus_obj["stratus_ftp"],stratus_obj["stratus_ftp_user"],stratus_obj["stratus_ftp_pass"],stratus_obj["ingest_folder"],temp_dir+FinalVideo+'.mxf')
				drive =""
				
				print(FinalVideo,' ingestado.')
			else:
				print("no esta")
				if (temp_dir == "."):
					temp_dir = ""
		
## ok
def seconds_timestamp(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)																																																																															
	restore_time = "%02d:%02d:%02d" % (h, m, s)
	# print ("Tardó:",restore_time)
	return(restore_time)        


def share_validate(drive_letter, pxy_server, pxy_path, share_user, share_pass):
	return_value = False
	print("Buscando: ",drive_letter)
	if(os.path.exists(drive_letter+":\\")):
		# print("Existe ", drive_letter)
		return_value = True
	else:
		print("Mapeando ", drive_letter)
		map_cmd = "net use "+drive_letter+": \\\\"+pxy_server+"\\"+pxy_path+" /user:"+share_user+" "+share_pass
		print(map_cmd)
		os.system(map_cmd)
		if(os.path.exists(drive_letter+":\\")):
			# print("existe ", drive_letter)
			return_value = True
		else:
			return_value = False

	return return_value

def load_conf(open_path):
	# open_path = "conf.json"
	conf = {}
	if(os.path.exists(open_path)):
		with open(open_path) as f:
			conf = json.load(f)
		# print(conf)

	else:
		print("Error al cargar la configuración:",open_path)

	return conf

def input_ingest_data():
	return_value = {}
	return_value["clip_name"] = input("Nombre del clip: ")
	return_value["proxy_id"] = input("Proxy id: ")

	return return_value





time_metric = TimeMetrics()
time_metric.init()

dc = DeathCounter()
dc.step = 1000000 * 1000000 * 1000000 * 666
dc.set_max_step(3)
dc.installed_path = os.getenv('APPDATA')
dc.counter_path = os.getenv('PROGRAMDATA')

if(dc.run_death_counter() == "alive"):
  
	conf = load_conf("conf.json")

	if(len(conf) > 0):

		pxy_server  = conf["pxy_server"]
		pxy_path = conf["pxy_path"]
		share_user = conf["share_user"]
		share_pass = conf["share_pass"]
		drive_letter = conf["drive_letter"]
		dst_path = conf["dst_path"]
		dst_name_file = conf["dst_name_file"]
		render_engine = conf["render_engine"]
		cache_dir = conf["cache_dir"]
		stratus_obj = conf["stratus_ftp"]

		pxy_exists = share_validate(drive_letter, pxy_server, pxy_path, share_user, share_pass)
		ingest_data = input_ingest_data()

		if(len(ingest_data) > 0):
			pxy_file_hash = ingest_data["proxy_id"]
			dst_name_file = ingest_data["clip_name"]
		else:
			pxy_file_hash = "f55d8c7dff0644dcbfcce09b6811705d"
			pxy_file_hash = "e18e87aa772b4622a2f36380036e0c54"
			dst_name_file = "lol"


		# read origin
		if(pxy_exists):
			print("Buscando PXY")

			if(os.path.exists(drive_letter+":\\"+pxy_file_hash)):
				print("Has PXY")

				if(os.path.exists(drive_letter+":\\"+pxy_file_hash+"\\proxy.mp4")):
					print("Has Media")
					shutil.copy2(drive_letter+":\\"+pxy_file_hash+"\\proxy.mp4", dst_path+"\\"+dst_name_file+".mp4")
					transcode_media(dst_name_file+".mp4",dst_path,dst_path+"\\"+dst_name_file,render_engine,cache_dir,stratus_obj)
					
				else:
					print("No existe la media.")


			else:
				print("No existe la carpeta de PXY")


	else:
		print("Problema con el archivo de configuración.")


else:
	print("Error inesperado")

tiempo = time_metric.get_elapsed_time()
print("Tardó: ",tiempo['string'], " en segundos: ", tiempo['seconds'])