import os, sys
# import pandas as pd
# from ftplib import FTP
# from ftplib import all_errors
# from subprocess import call
from time import time as time_i
# import time
from datetime import datetime
# # import sockett#

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
	parser.add_argument("muxer", help="preset de transcodificación")
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

		if("-i" in muxer_query_raw):
			return muxer_query_raw
		else:
			return False
		

	else:
		print("No existe muxer")

def run_muxer_single(muxer_query_raw,clip_name,local_dest_folder,render_engine_path,render_engine):
	""" params (muxer_query_raw,clip_name,local_dest_folder,render_engine_path,render_engine) """
	ffmpeg_query = muxer_query_raw.replace("$i_video",clip_name)
	extension = os.path.splitext(clip_name)[1]
	clip_name_not_Ext = os.path.splitext(clip_name) [0]
	local_dest = local_dest_folder + clip_name_not_Ext
	ffmpeg_query = render_engine_path+render_engine+" "+ffmpeg_query.replace("$o_video",local_dest)
	
	if(os.path.exists(render_engine_path+render_engine)):
		p = subprocess.Popen(ffmpeg_query)
		p.wait()
	else:
		print("No se encuentra el motor de render")

	return ffmpeg_query


if __name__ == '__main__':
	
	time_metric = TimeMetrics()
	time_metric.init()
	common_utils_test()


	# Cargar la configuración 
	conf = load_conf("conf.json")

	## Parametros de cmd
	muxer_file = "universal_h264"
	origin_path = "Y:\\Noticieros Octubre 2018\\Notis 011018"
	# origin_path = "C:\\Users\\ennima\\Documents\\Develops 2018\\Milenio\\cmf"

	clips_to_trans = get_transcode_clips_list(origin_path)

	# print(clips_to_trans)
	print("Clips:",len(clips_to_trans["clips"])," total_size:",clips_to_trans["total_size"])

	if(not ".mux" in muxer_file):
		muxer_file = muxer_file + ".mux"

	for clip in clips_to_trans["clips"]:
		# print(clip["path"]+"\\"+clip["name"])
		time_metric_clip = TimeMetrics()
		time_metric_clip.init()
		trans_clip = clip["path"]+"\\"+clip["name"]
		muxer_query = load_muxer(muxer_file)
		transcode_query = run_muxer_single(muxer_query,trans_clip,conf["local_dest_folder"],conf["render_engine_path"],conf["render_engine"])
		print(transcode_query)
		sleep(1000/1000)
		print(time_metric_clip.get_elapsed_time())


	print(time_metric.get_elapsed_time())


# # Rutina de salida del software
# input("Presiona cualquier tecla para cerrar el programa...")
