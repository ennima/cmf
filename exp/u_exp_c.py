import os, sys
from shutil import copyfile
from pathlib import Path
import subprocess
import requests


######## Cmf modules ############
# sys.path.append('../arq')
# from muxer import *
import json
import os,sys

import subprocess
# from common_utils import *
from ftplib import FTP
from ftplib import all_errors
import json
import os,sys

import subprocess
# sys.path.append('../trans')
# from time_metrics import *
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





# sys.path.append('../trans')
# from time_metrics import *

def validate_clip(clip):
	clip_type = ""
	media_know_ext = load_conf("media_know.json")
	extension = os.path.splitext(clip)[1].replace(".","")
	is_video = [video for video in media_know_ext["video"] if video == extension]
		
	if(len(is_video) != 0):
		# print("Puede ser video")
		clip_type = "video"
	else:
		# print("No es video")
		is_audio = [audio for audio in media_know_ext["audio"] if audio == extension]
		if(len(is_audio) != 0):
			# print("Puede ser audio")
			clip_type = "audio"
		else:
			# print("No es audio")
			clip_type = False

	return clip_type

def get_transcode_clips_list(origin_path):
	""" 
		Lee el directorio y regresa la cantidad de clips que puedetranscodificar.
		Return dict {"clips":list,"total_size":bytes}
	"""
	if(os.path.exists(origin_path)):
		print("Buscando lista de clips")
		total_size = 0
		clips = []
		for root, dirs, files in os.walk(origin_path, topdown = True):
			for name in files:
				media_type = validate_clip(name)
				if(media_type != False):
					clip_size = os.path.getsize(os.path.join(root, name))
					total_size += clip_size
					clip = {"path":root, "name":name, "size":clip_size}
					clips.append(clip)
				else:
					# print("No es media:",name)
					pass

		return {"clips":clips,"total_size":total_size}

	else:
		print("No existe el path")
		return False

def load_muxer(mux_file):
	if(os.path.exists(mux_file)):
		# print("Existe Muxer")
		
		with open(mux_file) as muxer:
			muxer_query_raw = muxer.read()

		# print(muxer_query_raw)
		muxer_data = json.loads(muxer_query_raw)

		if("-i" in muxer_data["core_query"]):
			return muxer_data
		else:
			return False
		

	else:
		print("No existe muxer")

def run_muxer_single(muxer,clip_name,local_dest_folder,render_engine_path,render_engine):
	""" params (muxer,clip_name,local_dest_folder,render_engine_path,render_engine) """
	print("MUXER:",muxer)
	if(muxer["type"] == "single"):
		return_val = {"success":False}
		ffmpeg_query = muxer["core_query"].replace("$i_video",clip_name)
		extension = os.path.splitext(clip_name)[1]
		clip_name_not_Ext = os.path.splitext(clip_name) [0]
		local_dest = local_dest_folder + os.path.basename(clip_name_not_Ext) +"."+ muxer["render_ext"]
		ffmpeg_query = render_engine_path+render_engine+" "+ffmpeg_query.replace("$o_video",local_dest)
		
		if(os.path.exists(clip_name)):
			# print("Existe Clip")
			print(render_engine_path+render_engine)
			if(os.path.exists(render_engine_path+render_engine)):
				
				p = subprocess.Popen(ffmpeg_query)
				p.wait()
				if(os.path.exists(local_dest)):
					return_val["result"] = local_dest
					return_val["success"] = True

				else:
					return_val["result"] = "bad_rednder"
					
			else:
				# print("No se encuentra el motor de render")
				return_val["result"] = "missing_render"
		else:
			# print("No existe el clip")
			return_val["result"] = "missing_clip"

		# print("local_dest",local_dest)
	else:
		return_val["result"] = "invalid muxer type"



	return return_val

def massive_muxing_single(conf,origin_path,muxer_file,clips_to_trans):
	transcoding_jobs = []
	min_clip_size_for_transcode = conf["min_clip_size_for_transcode"]


	for clip in clips_to_trans["clips"]:
		time_metric_clip = TimeMetrics()
		time_metric_clip.init()
		trans_clip = clip["path"]+"\\"+clip["name"]
		print("Size:", clip["size"])
		if(clip["size"] < min_clip_size_for_transcode):
			print("El clip no contiene información")
		else:
			muxer_query = load_muxer(conf["muxer_folder"]+muxer_file)
			# print(muxer_query)
			transcode_work = run_muxer_single(muxer_query,trans_clip,conf["local_dest_folder"],conf["render_engine_path"],conf["render_engine"])
			# print(transcode_work)
			if(transcode_work["success"]):
				trans_clip_size = os.path.getsize(transcode_work["result"])
				trans_result = {"path":os.path.dirname(transcode_work["result"]),"name":os.path.basename(transcode_work["result"]),"size":trans_clip_size}
				
				original_part_represent = percentage(clip["size"],trans_result["size"])
				reduction = 100 - original_part_represent
				
				trans_job_log = {}
				if(original_part_represent < conf["min_original_part_represent_trust"]):
					print("## Warning ## Posible fallo al transcodificar, revise que el material está completo y bien formado.")
					trans_job_log = {"type":"warning","message":"Posible fallo al transcodificar, revise que el material está completo y bien formado."}
				
				trans_job = {"original_clip":clip,"final_clip":trans_result,"original_part_represent":original_part_represent,"reduction":reduction,"time_of_job":time_metric_clip.get_elapsed_time(),"trans_job_log":trans_job_log}
				# print(trans_job)
				transcoding_jobs.append(trans_job)
	
		break
		

	# print(transcoding_jobs)
	return transcoding_jobs




def massive_muxing_single_api(conf,origin_path,muxer_file,clips_to_trans,ingest_client_obj):
	transcoding_jobs = []
	min_clip_size_for_transcode = conf["min_clip_size_for_transcode"]

	clips_restantes = len(clips_to_trans["clips"])
	for clip in clips_to_trans["clips"]:
		time_metric_clip = TimeMetrics()
		time_metric_clip.init()
		trans_clip = clip["path"]+"\\"+clip["name"]
		print("Size:", clip["size"])
		if(clip["size"] < min_clip_size_for_transcode):
			print("El clip no contiene información")
		else:
			muxer_query = load_muxer(conf["muxer_folder"]+muxer_file)
			# print(muxer_query)
			transcode_work = run_muxer_single(muxer_query,trans_clip,conf["local_dest_folder"],conf["render_engine_path"],conf["render_engine"])
			# print(transcode_work)
			if(transcode_work["success"]):
				trans_clip_size = os.path.getsize(transcode_work["result"])
				trans_result = {"path":os.path.dirname(transcode_work["result"]),"name":os.path.basename(transcode_work["result"]),"size":trans_clip_size}
				
				original_part_represent = percentage(clip["size"],trans_result["size"])
				reduction = 100 - original_part_represent
				
				trans_job_log = {}
				if(original_part_represent < conf["min_original_part_represent_trust"]):
					print("## Warning ## Posible fallo al transcodificar, revise que el material está completo y bien formado.")
					trans_job_log = {"type":"warning","message":"Posible fallo al transcodificar, revise que el material está completo y bien formado."}
				time_of_working = time_metric_clip.get_elapsed_time()
				print("------------------------------------------------TIME OF WORKING:",time_of_working)
				trans_job = {"original_clip":clip,"final_clip":trans_result,"original_part_represent":original_part_represent,"reduction":reduction,"time_of_job":time_of_working,"trans_job_log":trans_job_log}
				# print(trans_job)
				transcoding_jobs.append(trans_job)

				clips_totales = len(clips_to_trans["clips"])
				clips_restantes = clips_restantes - 1
				clips_actuales = clips_totales - clips_restantes
				progress = percentage(clips_totales,clips_actuales)
				ingesting_string ="Ingestando: "+ "{0:.2}".format(str(progress))+"% "+" - "+str(clips_actuales) +" de " + str(clips_totales) + " clips"
				#"Faltan " + str(clips_restantes)+" de " + str(len(clips_to_trans["clips"]))
				ingest_client_obj.ingesting(ingesting_string)
				ingest_client_obj.add_job()
				ingest_client_obj.add_ingest_job(json.dumps(clip),json.dumps(trans_result),time_of_working['seconds'],reduction,original_part_represent, json.dumps(trans_job_log))
		# break
		

	# print(transcoding_jobs)
	return transcoding_jobs

# sys.path.append('../communication')
# from ingest_client import *
import os,sys
import requests
import json
import socket

class IngestClient(object):
	""" Ingest client object """
	_client = {}
	_api_server = {}
	_allow = 0

	uid = 0
	name = ""
	host_name = ""
	ip = ""
	status = ""
	message = ""
	cli_type = ""
	jobs = 0

	log = ""

	def __init__(self):
		pass

	def init(self):
		pass

	def set_client(self,client):
		self._client = client

	def set_api_server(self,api_server):
		self._api_server = api_server

	def _get(self,route,playload):
		r = requests.get(self._api_server["http"]+'://'+self._api_server["host"]+':'+self._api_server["port"]+'/'+route, params=playload)
		return json.loads(r.text)

	def _post(self,route,playload):
		r = requests.post(self._api_server["http"]+'://'+self._api_server["host"]+':'+self._api_server["port"]+'/'+route, params=playload)
		return json.loads(r.text)

	def _get_client_info_name(self):
		playload = {"name":self._client["name"]}
		return self._get("ingest_client_name",playload)

	def _validate_client(self):
		return_val = ""
		client_info = self._get_client_info_name()

		# print(client_info.keys())
		if("result" in client_info.keys()):
			if(client_info["result"] == "false"):
				return "fail_name"

		if(self._client["type"] == client_info["type"]):
			# print("Coincide el tipo")
			if(client_info["allow"]):
				# print("Adelante")
				self._allow = client_info["allow"]
				self.uid = client_info["ingest_client_id"]
				self.name = client_info["name"]
				self.host_name = client_info["host_name"]
				self.ip = client_info["IP"]
				self.status = client_info["status"]
				self.message = client_info["message"]
				self.cli_type = client_info["type"]
				self.jobs = client_info["jobs"]
				return_val = "loaded"
			else:
				# print("Sorry :(")
				return_val = "fail"
		else:
			# print("No es el mismo tipo")
			return_val = "bad_type"
		return return_val
	
	
	def start(self):
		validate = self._validate_client()
		if(validate == "loaded"):
			if(self._allow):
				return True
				self.log = "not allow"
			else:
				return False
		else:
			self.log = validate
			return False

	

	def add(self,name,cli_type):
		self.ip = socket.gethostbyname(socket.gethostname())
		self.name = name
		self.host_name = socket.gethostname()
		self.cli_type = cli_type
		self.status = "online"
		self._allow = 1
		self.message = "First step"

		playload = {"name":self.name,"host_name":self.host_name,"IP":self.ip,"status":self.status,"message":self.message,"type":self.cli_type,"allow":self._allow,"jobs":self.jobs}
		result = self._post("add_ingest_client",playload)
		
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

	def add_ingest_job(self,origin_clip,dest_clip,time,reduction,original_represents, job_log):
		
		playload = {"ingest_client_id":self.uid,"origin_clip":origin_clip,"dest_clip":dest_clip,"time":time,"reduction":reduction,"original_represents":original_represents,"job_log":job_log}
		result = self._post("ingest_jobs/add",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

	def get_data_for_conf(self):
		return {"client":{"name":self.name,"type":self.cli_type}}

	def add_job(self):
		self.jobs += 1
		playload = {"jobs":self.jobs,"ingest_client_id":self.uid}
		result = self._post("set_ingest_client_jobs",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

	def remove_job(self):
		self.jobs = self.jobs - 1
		if(self.jobs < 0):
			self.jobs = 0

		playload = {"jobs":self.jobs,"ingest_client_id":self.uid}
		result = self._post("set_ingest_client_jobs",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

	def ingesting(self,num_clips):
		playload = {"num_clips":num_clips,"ingest_client_id":self.uid}
		result = self._post("ingesting_ingest_client",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

	def fail(self,fail_msg):
		playload = {"fail_msg":fail_msg,"ingest_client_id":self.uid}
		result = self._post("fail_ingesting_ingest_client",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

	def offline(self):
		playload = {"ingest_client_id":self.uid}
		result = self._post("offline_ingest_client",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

	def online(self):
		playload = {"ingest_client_id":self.uid}
		result = self._post("online_ingest_client",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False





import argparse
######### Cabecera de comando #########
def get_arguments():
	""" Read arguments from cmd"""
	parser = argparse.ArgumentParser()
	return_data = {}
	
	#Required
	parser.add_argument("path", help="ruta de origen, carpeta que contiene la media a transcodificar, debe escribirse entre comillas. Ej.: \"ruta\" ")
	parser.add_argument("--muxer", help="preset de transcodificación")
	args = parser.parse_args()

	# Validating arguments
	### Required
	if args.path:
		return_data["path"] = args.path
	
	if args.muxer:
		return_data["muxer"] = args.muxer

	return return_data


command_data = get_arguments()
print(command_data)
######### Cabecera de comando #########


if __name__ == '__main__':
	
	time_metric = TimeMetrics()
	time_metric.init()
	
	# Program vars
	continue_runing = True

	dir_path = os.path.dirname(os.path.realpath(__file__))
	print("dir_path:",dir_path)
	print(os.getcwd())
	# Cargar la configuración 
	conf = load_conf("conf.json")
	if(conf != False):

		conf_keys_required = ["min_original_part_represent_trust","min_clip_size_for_transcode","local_dest_folder","render_engine_path","render_engine","muxer","muxer_folder"]
		continue_runing = validate_conf_data(conf_keys_required,conf)

		if(continue_runing):

			# Ingest Client API
			client = conf["client"]
			api_server = conf["istorage_api_servers"][0]
			ingest_client_1 = IngestClient()
			ingest_client_1.set_client(client)
			ingest_client_1.set_api_server(api_server)

			is_allow = ingest_client_1.start()
			# print(is_allow)
			if(is_allow):
				print("Working")


				# transcode vars
				min_clip_size_for_transcode = conf["min_clip_size_for_transcode"]
				transcoding_jobs = []


				## Parametros de cmd
				muxer_file1 = conf["muxer"]
				# muxer_file = "avi"
				# origin_path1 = "Y:\\Noticieros Octubre 2018\\Notis 011018"
				# origin_path1 = "C:\\Users\\ennima\\Documents\\Develops 2018\\Milenio\\cmf"
				# origin_path1 = "C:\\Users\\ennima\\Desktop\\ffXperiments\\mxf_test_archive"

				origin_path1 = command_data["path"]
				clips_to_trans1 = get_transcode_clips_list(origin_path1)

				print(clips_to_trans1)
				print("Clips:",len(clips_to_trans1["clips"])," total_size:",clips_to_trans1["total_size"])

				ingest_client_1.ingesting(len(clips_to_trans1["clips"]))
				if(not ".mux" in muxer_file1):
					muxer_file1 = muxer_file1 + ".mux"
				
				jobs = massive_muxing_single_api(conf,origin_path1, muxer_file1, clips_to_trans1,ingest_client_1)
				
				ingest_client_1.online()
			
			else:
				print("No tiene permisos para ejecutar la tarea.")
								
		else:
			print("Faltan algunos parametros de configuración.")

	else:
		print("Problema al cargar configuración.")

	print(time_metric.get_elapsed_time())


# Rutina de salida del software
# input("Presiona cualquier tecla para cerrar el programa...")
