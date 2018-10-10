# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET


class Cmf(object):
	"""
	La clase Cmf puede interpretar
	la información de un clip de GrassValley Stratus
	
	"""
	tree = {}
	root = {}
	def __init__(self,cmf_path):
		super(Cmf, self).__init__()
		self._is_xml_load = False
		
		### Load XML of CMF
		# print(cmf_path)
		metadata_file = os.path.basename(cmf_path).replace(".cmf",".xml")
		# print(metadata_file)
		metadata_file_path = cmf_path+"\\"+metadata_file
		if(os.path.exists(metadata_file_path)):
			self.tree = ET.parse(metadata_file_path)
			self.root = self.tree.getroot()
			self._is_xml_load = True
		else:
			print("ERROR: No existe el cmf:",metadata_file_path)


	
	def get_asset_id(self):
		return self.root.attrib['AssetId']

	def get_source_id(self):
		return self.root.attrib['SourceId']

	def get_asset_type(self):
		return self.root.attrib['AssetType']

	def get_reference_standard(self):
		return self.root.attrib['ReferenceStandard']

	def get_mark_in(self):
		return self.root.attrib['MarkIn']

	def get_mark_in_str(self):
		return self.root.attrib['MarkInStr']

	def get_mark_out(self):
		return self.root.attrib['MarkOut']

	def get_mark_out_str(self):
		return self.root.attrib['MarkOutStr']

	def get_size_mb(self):
		return self.root.attrib['Size']

	def get_created(self):
		return self.root.attrib['Created']

	def get_modified(self):
		return self.root.attrib['Modified']

	def get_locked(self):
		return self.root.find('Attributes').attrib['Locked']

	def get_construction(self):
		return self.root.find('Attributes').attrib['Construction']


	def get_audio_format(self):
		audio_format = {}
		for child in self.root:
			if(child.tag == 'Track'):
				if(child.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == 'AudioTrack'):
					segment = child.find('Segment')
					hires_format = segment.find('HiResFormat')
					audio_format = {'type':hires_format.attrib['AudioType'], 'sample_rate':hires_format.attrib['SampleRate']}
				break
		return audio_format
	
		

cmf = "X:\\Recup\\ENTREVISTA REBECA DE ALBA\\ENTREVISTA REBECA DE ALBA(2).cmf"
my_cmf = Cmf(cmf)
print(my_cmf.get_audio_format())
print(my_cmf.get_construction())

