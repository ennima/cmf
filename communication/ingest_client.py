import os,sys
import requests
import json
import socket

class IngestClient(object):
	""" Ingest client object """
	_client = {}
	_api_server = {}
	_allow = 0

	uid = 0
	name = ""
	host_name = ""
	ip = ""
	status = ""
	message = ""
	cli_type = ""
	jobs = 0

	log = ""

	def __init__(self):
		pass

	def init(self):
		pass

	def set_client(self,client):
		self._client = client

	def set_api_server(self,api_server):
		self._api_server = api_server

	def _get(self,route,playload):
		r = requests.get(self._api_server["http"]+'://'+self._api_server["host"]+':'+self._api_server["port"]+'/'+route, params=playload)
		return json.loads(r.text)

	def _post(self,route,playload):
		r = requests.post(self._api_server["http"]+'://'+self._api_server["host"]+':'+self._api_server["port"]+'/'+route, params=playload)
		return json.loads(r.text)

	def _get_client_info_name(self):
		playload = {"name":self._client["name"]}
		return self._get("ingest_client_name",playload)

	def _validate_client(self):
		return_val = ""
		client_info = self._get_client_info_name()

		# print(client_info.keys())
		if("result" in client_info.keys()):
			if(client_info["result"] == "false"):
				return "fail_name"

		if(self._client["type"] == client_info["type"]):
			# print("Coincide el tipo")
			if(client_info["allow"]):
				# print("Adelante")
				self._allow = client_info["allow"]
				self.uid = client_info["ingest_client_id"]
				self.name = client_info["name"]
				self.host_name = client_info["host_name"]
				self.ip = client_info["IP"]
				self.status = client_info["status"]
				self.message = client_info["message"]
				self.cli_type = client_info["type"]
				self.jobs = client_info["jobs"]
				return_val = "loaded"
			else:
				# print("Sorry :(")
				return_val = "fail"
		else:
			# print("No es el mismo tipo")
			return_val = "bad_type"
		return return_val
	
	def start(self):
		validate = self._validate_client()
		if(validate == "loaded"):
			if(self._allow):
				return True
				self.log = "not allow"
			else:
				return False
		else:
			self.log = validate
			return False

	
	def add(self,name,cli_type):
		""" Create a new ingest client on db"""
		self.ip = socket.gethostbyname(socket.gethostname())
		self.name = name
		self.host_name = socket.gethostname()
		self.cli_type = cli_type
		self.status = "online"
		self._allow = 1
		self.message = "First step"

		playload = {"name":self.name,"host_name":self.host_name,"IP":self.ip,"status":self.status,"message":self.message,"type":self.cli_type,"allow":self._allow,"jobs":self.jobs}
		result = self._post("add_ingest_client",playload)
		
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

	def get_data_for_conf(self):
		""" Return dict ready to append to conf"""
		return {"client":{"name":self.name,"type":self.cli_type}}

	def add_job(self):
		""" ++ job to Ingest Client Table Row column jobs """
		self.jobs += 1
		playload = {"jobs":self.jobs,"ingest_client_id":self.uid}
		result = self._post("set_ingest_client_jobs",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False
	

	def remove_job(self):
		""" -- job to Ingest Client Table Row column jobs """
		self.jobs = self.jobs - 1
		if(self.jobs < 0):
			self.jobs = 0

		playload = {"jobs":self.jobs,"ingest_client_id":self.uid}
		result = self._post("set_ingest_client_jobs",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

	


	def add_ingest_job(self,origin_clip,dest_clip,time,reduction,original_represents, job_log):
		""" Add a job to the table ingest jobs"""
		# print("---------------------------------------Add TIME: ",time)
		playload = {"ingest_client_id":self.uid,"origin_clip":origin_clip,"dest_clip":dest_clip,"time":time,"reduction":reduction,"original_represents":original_represents,"job_log":job_log}
		result = self._post("ingest_jobs/add",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False


	def ingesting(self,num_clips):
		playload = {"num_clips":num_clips,"ingest_client_id":self.uid}
		result = self._post("ingesting_ingest_client",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

	def fail(self,fail_msg):
		playload = {"fail_msg":fail_msg,"ingest_client_id":self.uid}
		result = self._post("fail_ingesting_ingest_client",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

	def offline(self):
		playload = {"ingest_client_id":self.uid}
		result = self._post("offline_ingest_client",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

	def online(self):
		playload = {"ingest_client_id":self.uid}
		result = self._post("online_ingest_client",playload)
		if(result["rows"]["affectedRows"] == 1):
			return True
		else:
			return False

