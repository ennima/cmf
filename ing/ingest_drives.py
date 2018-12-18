import psutil
import os,sys
from os import walk

sys.path.append('../arq')
from common_utils import *
from muxer import *

class IngestDrivers(object):
	"""This class read external drives and search media devices"""
	drives_to_discard = []
	def __init__(self, drives_to_discard, ingest_device_conf):
		self.drives_to_discard = drives_to_discard
		drive_map_list = load_conf(ingest_device_conf)
		# print(drive_map_list)
		self.ingest_device_paths = drive_map_list['ingest_device_paths']
		# print(ingest_device_paths)
		self.virtual_ingest_device_paths = drive_map_list['virtual_ingest_device_paths']

	def _is_discard_drive(self,drive):
		discard = 0
		for discard in self.drives_to_discard:
			if(drive == discard):
				discard = 1
				break
			else:
				discard = 0
		return discard

	def get_external_drives(self):
		""" Return all conected external drive letters on array """
		drive_available = psutil.disk_partitions()
		cards = []
		for drive in drive_available:
			if(drive.fstype != ''):
				if(not self._is_discard_drive(drive.device)):
					cards.append(drive.device)
	
		return cards

	def find_device_path(self,drive_paths,drive):
		""" Return valid media drive if exists """
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

	def read_clips_from_devices(self):
		""" Return dic - a list of physical devisces with media and list of clips ready to ingest """
		ingest_list_by_device = []
		clips_to_ingest = []
		drives_to_ingest = []
		drives = self.get_external_drives()
		for drive in drives:
			drive_map = self.find_device_path(self.ingest_device_paths,drive)
			
			if(drive_map != False):
				total_size = 0
				drives_to_ingest.append(drive_map)
				for root, dirs, files in os.walk(drive + drive_map["dir_map"]["video"], topdown=False):
					for name in files:
						full_path = os.path.join(root, name)
						clip_size = os.path.getsize(full_path)
						# print(clip_size)
						total_size += clip_size
						clip = {"path":root,"name":name,"full_path":full_path,"size":clip_size}
						clips_to_ingest.append(clip)
				ingest_list_by_device.append({"letter":drive,"info":drive_map,"clips":clips_to_ingest,"total_size":total_size})
		return ingest_list_by_device

	def read_clips_from_virtual_devices(self):
		""" Return dic - a list of virtual path devisces with media and list of clips ready to ingest """
		clips = []
		ingest_list_by_device = []	
		drives_to_ingest = []

		for virtual_ingest_device in self.virtual_ingest_device_paths:
			if(os.path.exists(virtual_ingest_device["dir_map"]["video"])):
				for root, dirs, files in os.walk(virtual_ingest_device["dir_map"]["video"], topdown=False):
					for name in files:
						clip = {"name":name,"full_path":os.path.join(root, name)}
						clips.append(clip)
					for name in dirs:
						pass
				ingest_list_by_device.append({"virtual_path":virtual_ingest_device,"clips":clips})
		return ingest_list_by_device





