import os, sys, json
import subprocess

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

# command = "python sample_cmd.py"

conf = load_conf("params.json")

print(conf)


if(conf != False):

		conf_keys_required = ["params"]
		continue_runing = validate_conf_data(conf_keys_required,conf)

		if(continue_runing):
			print("WORKING")
			# print(conf["params"])

			for param in conf["params"]:
				print(param)
				p = subprocess.Popen(conf["command"]+" "+param)
				p.wait()


input("Presiona una tecla para continuar...")
