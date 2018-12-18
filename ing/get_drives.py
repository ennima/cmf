import psutil
import os,sys
from os import walk

sys.path.append('../arq')
from common_utils import *


drives_to_discard = ['C:\\','V:\\']



def is_discard_drive(drive):
	# print("Testing ",drive)
	discard = 0
	for discard in drives_to_discard:
		if(drive == discard):
			# print("descartado")
			discard = 1
			break
		else:
			discard = 0
	# print("Discard:",discard)
	return discard


def get_external_drives():
	drive_available = psutil.disk_partitions()
	
	cards = []
	for drive in drive_available:
		if(drive.fstype != ''):
			# print(drive)
			# print(drive.device)
			# print(is_discard_drive(drive.device))
			if(not is_discard_drive(drive.device)):
				# print("Tarjeta: ",drive.device)
				cards.append(drive.device)
		# print("\n")
			# if(is_discard_drive(drive.device)):
			# 	pass
			# else:
			# 	print("-----",drive.device)
	# print(cards)
	return cards

def find_device_path(drive_paths,drive):
	return_value = False
	if(drive == ""):
		return False
	else:
		for drive_path in drive_paths:
			path_to_check = drive+drive_path["dir_map"]['video']
			# print("path_to_check",path_to_check)
			existe = os.path.exists(path_to_check)
			# print(existe)
			if(os.path.exists(path_to_check)):
				# print("Drive: ",drive_path["name"])
				return drive_path
			else:
				# print("No existe:",path_to_check)
				pass

	return return_value


def read_clips_from_devices(ingest_device_paths,drives):
	ingest_list_by_device = []
	clips_to_ingest = []
	drives_to_ingest = []

	for drive in drives:
		drive_map = find_device_path(ingest_device_paths,drive)
		
		if(drive_map != False):
			# print(drive_map["name"])
			# print(drive + drive_map["dir_map"]["video"])
			drives_to_ingest.append(drive_map)
			for root, dirs, files in os.walk(drive + drive_map["dir_map"]["video"], topdown=False):
			    for name in files:
			        # print(os.path.join(root, name))
			        clip = {"name":name,"full_path":os.path.join(root, name)}
			        clips_to_ingest.append(clip)
			    for name in dirs:
			        # print(os.path.join(root, name))
			        pass
			
			ingest_list_by_device.append({"drive":{"letter":drive,"info":drive_map,"clips":clips_to_ingest}})

	# print(drives_to_ingest)
	return ingest_list_by_device


def read_clips_from_virtual_devices(virtual_ingest_device_paths):
	clips = []
	ingest_list_by_device = []	
	drives_to_ingest = []

	for virtual_ingest_device in virtual_ingest_device_paths:
		# print(virtual_ingest_device)
		# print(virtual_ingest_device["dir_map"]["video"])
		if(os.path.exists(virtual_ingest_device["dir_map"]["video"])):
			# print("existe virtual")
			for root, dirs, files in os.walk(virtual_ingest_device["dir_map"]["video"], topdown=False):
				for name in files:
					# print(os.path.join(root, name))
					clip = {"name":name,"full_path":os.path.join(root, name)}
					clips.append(clip)
					# print(clip)
				for name in dirs:
					# print(os.path.join(root, name))
					pass
			ingest_list_by_device.append({"drive":{"virtual_path":virtual_ingest_device,"clips":clips}})
	# print(ingest_list_by_device)
	return ingest_list_by_device



drives = get_external_drives()
print(drives)
drive_map_list = load_conf("./ingest_device.json")
print(drive_map_list)
ingest_device_paths = drive_map_list['ingest_device_paths']
print(ingest_device_paths)
virtual_ingest_device_paths = drive_map_list['virtual_ingest_device_paths']

# Read all drives and get information for ingest
drives = read_clips_from_devices(ingest_device_paths,drives)
print(drives)
virtual_drives = read_clips_from_virtual_devices(virtual_ingest_device_paths)
print(virtual_drives)


# print("Drives detected:\n 	 {} - {} del tipo: {} con {} clips".format(len(drives),drives[0]["drive"]["letter"],drives[0]["drive"]["info"]["name"],len(drives[0]["drive"]["clips"])))

# print("Virtual drives detected:\n 	 {} del tipo: {} con {} clips".format(len(virtual_drives),virtual_drives[0]["drive"]["virtual_path"]["name"],len(virtual_drives[0]["drive"]["clips"])))
