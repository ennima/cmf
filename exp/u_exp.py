import os, sys
from shutil import copyfile
from pathlib import Path
import subprocess
import requests


######## Cmf modules ############
sys.path.append('../arq')
from muxer import *

sys.path.append('../communication')
from ingest_client import *

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

			if(ingest_client_1.start()):
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
			print("Faltan algunos parametros de configuración.")

	else:
		print("Problema al cargar configuración.")

	print(time_metric.get_elapsed_time())


# # Rutina de salida del software
# input("Presiona cualquier tecla para cerrar el programa...")
