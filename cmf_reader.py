# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

#----- Obtiene la información de 
def get_audio_format(cmf):
	audio_format = {}	
	tree = ET.parse(cmf)
	root = tree.getroot()
	
	for child in root:
		if(child.tag == 'Track'):
			if(child.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] == 'AudioTrack'):
				segment = child.find('Segment')
				hires_format = segment.find('HiResFormat')
				audio_format = {'type':hires_format.attrib['AudioType'], 'sample_rate':hires_format.attrib['SampleRate']}
			break
	return audio_format


# cmf = "X:\\Recup\\ENTREVISTA REBECA DE ALBA\\ENTREVISTA REBECA DE ALBA(2).cmf\\ENTREVISTA REBECA DE ALBA(2).xml"
# print(get_audio_format(cmf))