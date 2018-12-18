import json
import os,sys

import subprocess
from common_utils import *
sys.path.append('../trans')
from time_metrics import *


print("muxer")
def validate_clip(clip):
	clip_type = ""
	media_know_ext = load_conf("media_know.json")
	# print("MediaKnow:",media_know_ext)
	if(media_know_ext == False):
		print("No se encontró la configuración: media_know")
		clip_type = False
	else:
		extension = os.path.splitext(clip)[1].replace(".","")
		is_video = [video for video in media_know_ext["video"] if video == extension.lower()]
			
		if(len(is_video) != 0):
			# print("Puede ser video")
			clip_type = "video"
		else:
			# print("No es video")
			is_audio = [audio for audio in media_know_ext["audio"] if audio == extension.lower()]
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

