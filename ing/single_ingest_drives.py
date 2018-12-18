import string
from ctypes import windll
import time
import os, sys, json
from os import walk
import subprocess
import ftplib

def load_conf(conf_file):
	if(os.path.exists(conf_file)):
		with open(conf_file) as json_file:
			json_data = json_file.read()
			
		conf = json.loads(json_data)
	else:
		conf = False	
	return conf

def find_tilde(clip):
	 ### Find tildes
	have_tilde = False
	tildes = ['ñ','Ñ','á','Á','É','é','í','Í','ó','Ó','ú','Ú']
	for tilde in tildes:
		if(tilde in clip):
			# print('No apto: ',clip)
			have_tilde = True
			break
	return have_tilde


def get_input_drives():
	input_drives = "f,g,h"
	print("Escribe la letra de las unidades")
	print("Sugerencia una: f")
	print("Sugerencia más de una: f,g")
	input_drives = input("Unidades:")

	# print("input_drives:",input_drives)

	drives = [drive.upper() for drive in input_drives.split(",")]

	print(drives)
	return drives


def change_tilde(clip):
	 ### Find tildes
	have_tilde = False
	tildes = [
			  'ñ','Ñ',
			  'á','Á','ä','Ä','à','À','â','Â',
			  'É','é','ë','Ë','è','È','ê','Ê',
			  'í','Í','ï','Ï','ì','Ì','î','Î',
			  'ó','Ó','ö','Ö','ò','Ò','ô','Ô',
			  'ú','Ú','ü','Ü','ù','Ù','û','Û',
			  ]

	tildes_dict = [
					{'ñ':'ni'}
					,{'Ñ':'N'}
					,{'Á':'A'}
					,{'á':'a'}
					,{'É':'E'}
					,{'é':'e'}
					,{'Í':'I'}
					,{'í':'i'}
					,{'Ó':'O'}
					,{'ó':'o'}
					,{'Ú':'U'}
					,{'ú':'u'}
				  ]

	for til in tildes:
		if(til in clip):
			# print("Tilde: ",til)
			til_in_dic = False
			for tilde in tildes_dict:
				# print(tilde)
				if(til in tilde):
					# print("CHANGE TILDE by:",tilde[til])
					clip = clip.replace(til,tilde[til])
					til_in_dic = True
			if(not til_in_dic):
				print("NO in dict: ",til)
				clip = clip.replace(til,"")
	# print("QUEDA: ",clip)
	return clip





def get_input_ingest_name():
	ingest_name = " ingest á nameñ "
	ingest_name = ingest_name.upper().strip().replace(" ","_")
	# print(ingest_name)
	if(not find_tilde(ingest_name)):
		# print("ingestable")
		pass
	else:
		# print("No ingestable")
		ingest_name = change_tilde(ingest_name)

	return ingest_name


def get_ingest_folder(ingest_name, conf):
	ingest_folder = "\\{}\\{}\\".format(conf["dest_folder"],ingest_name)
	return ingest_folder

# get_input_drives()

config = load_conf("local_ingest_conf.json")

print(get_input_ingest_name())

print(get_ingest_folder(get_input_ingest_name(),config))
temp_dir = config["temp_dir"]

stratus_ftp = config["stratus_ftp"]
stratus_ftp_user = config["stratus_ftp_user"]
stratus_ftp_pass = config["stratus_ftp_pass"]

drives = get_input_drives()
channels = input("Audio channels:")
print(drives)
print(channels)