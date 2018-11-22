import os, sys
from time import time as time_i
from datetime import datetime
from shutil import copyfile
from pathlib import Path
import subprocess
import requests


######## Cmf modules ############
sys.path.append('../arq')
from common_utils import *
sys.path.append('../trans')
from time_metrics import *


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


# command_data = get_arguments()
# print(command_data)
######### Cabecera de comando #########


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


if __name__ == '__main__':
	
	time_metric = TimeMetrics()
	time_metric.init()
	# common_utils_test()

	# Program vars
	continue_runing = True

	# Cargar la configuración 
	conf = load_conf("conf.json")
	if(conf != False):

		conf_keys_required = ["min_original_part_represent_trust","min_clip_size_for_transcode","local_dest_folder","render_engine_path","render_engine","muxer","muxer_folder"]
		continue_runing = validate_conf_data(conf_keys_required,conf)

		if(continue_runing):
			# transcode vars
			min_clip_size_for_transcode = conf["min_clip_size_for_transcode"]
			transcoding_jobs = []


			## Parametros de cmd
			muxer_file = "gxf_h264"
			# muxer_file = "avi"
			# origin_path = "Y:\\Noticieros Octubre 2018\\Notis 011018"
			# origin_path = "C:\\Users\\ennima\\Documents\\Develops 2018\\Milenio\\cmf"
			origin_path = "C:\\Users\\ennima\\Desktop\\ffXperiments\\mxf_test_archive"

			clips_to_trans = get_transcode_clips_list(origin_path)

			# print(clips_to_trans)
			print("Clips:",len(clips_to_trans["clips"])," total_size:",clips_to_trans["total_size"])

			if(not ".mux" in muxer_file):
				muxer_file = muxer_file + ".mux"

			
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
			
				# break
				

			print(transcoding_jobs)
		
		else:
			print("Faltan algunos parametros de configuración.")

	else:
		print("Problema al cargar configuración.")

	print(time_metric.get_elapsed_time())


# # Rutina de salida del software
# input("Presiona cualquier tecla para cerrar el programa...")
