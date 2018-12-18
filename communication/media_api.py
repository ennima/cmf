import os,sys
import requests
import json
import socket

from ingest_client import *
######## Cmf modules ############
sys.path.append('../arq')
from muxer import *

conf = load_conf("conf.json")
# print(conf)
required_keys=["client","istorage_api_servers"]

continue_runing = validate_conf_data(required_keys, conf)
print(continue_runing)

if(continue_runing):

	client = conf["client"]
	# print(client)

	api_server = conf["istorage_api_servers"][0]
	# print(api_server)

	# Create a Ingest Client Instance
	ingest_client_1 = IngestClient()
	# Set client Data from Conf
	ingest_client_1.set_client(client)
	# Set media_api server from conf
	ingest_client_1.set_api_server(api_server)

	# Turn Online Ingest Client
	start = ingest_client_1.start()
	print(start)
	if(start):
		print("Working")

		# if(ingest_client_1.add("MyClient","massive_transcoder")):
		# 	print("Bienvenido")
		# else:
		# 	print("Ups! :(")
		
		print(ingest_client_1.get_data_for_conf())
		print(ingest_client_1.jobs)
		print(ingest_client_1.online())
