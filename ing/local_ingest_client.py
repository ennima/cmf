from ingest_drives import *


sys.path.append('../communication')
from ingest_client import *


class LocalIngestClient(IngestClient):
	""" Extends Ingest client functionality transcoding """
	def __init__(self):
		pass



conf = load_conf("conf.json")
# print(conf)
required_keys=["client","istorage_api_servers"]

continue_runing = validate_conf_data(required_keys, conf)
print(continue_runing)



if(continue_runing):

	client = conf["client"]
	print(client)

	api_server = conf["istorage_api_servers"][0]

		


drives_to_discard = ['C:\\','V:\\']
ingest_device_conf1 = "./ingest_device.json"

drive_reader = IngestDrivers(drives_to_discard,ingest_device_conf1)

drives = drive_reader.read_clips_from_devices()


if(continue_runing):

	client = conf["client"]
	# print(client)

	api_server = conf["istorage_api_servers"][0]
	# print(api_server)

	# Create a Ingest Client Instance
	ingest_client_1 = LocalIngestClient()
	# Set client Data from Conf
	ingest_client_1.set_client(client)
	# Set media_api server from conf
	ingest_client_1.set_api_server(api_server)

	# Turn Online Ingest Client
	start = ingest_client_1.start()
	print(start)
	if(start):
		print("Working")


# print(drives)
# def make_audio_query(drive_letter,temp_dir,video,channels):
# 	unidad = drive_letter
# 	# temp_dir = "temp"
# 	ffmpeg_path = ""
# 	audio_channels_string = ""
# 	filter_complex_string = "-filter_complex "
# 	audio_merge_string = ffmpeg_path+'ffmpeg '
# 	end_line = " "
# 	for channel in range(0,channels):
		
# 		if(channel<10):
# 			channel_num = "0"+str(channel)
# 		else:
# 			channel_num = str(channel)
# 		filter_complex_string += '['+str(channel)+':a]'
# 		audio_channels_string += '-y -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+channel_num+'.mxf' + end_line
# 	audio_filter = filter_complex_string+'amerge=inputs='+str(channels)+'[aout] -map [aout] -ac '+str(channels)+' '
# 	audio = audio_merge_string+audio_channels_string+audio_filter+temp_dir+video+'.flac'
# 	print(audio)
# 	return audio

# def run_muxer_complex(ftp_material_name,clip):

# 	print(clip["full_path"])
# 	extension = os.path.splitext(clip["name"])[1]
# 	print(extension)
# 	clip_name_not_Ext = clip["name"].replace(extension,"")
# 	print(clip_name_not_Ext)
# 	FinalVideo = ftp_material_name +"_"+ clip_name_not_Ext
# 	print(FinalVideo)
# 	muxer = load_muxer("avci.json")
# 	print(muxer)

# 	channels = 2
# 	print("Channels: ",channels)
	
# 	virtual_drive = "\\\\192.168.196.99\\B_Workflow\\dev\\virtual_ingest_p2\\TEST_INGEST\\T1"
# 	virtual_drive_audio = "CONTENTS\\AUDIO\\"
# 	temp_dir = "C:\\Users\\gvadmin\\Desktop\\ingestapy_\\temp\\"

# 	make_audio_query(virtual_drive,temp_dir,clip_name_not_Ext,channels)







# print(len(drives))
# for drive in drives:
# 	# print(drive["letter"])
# 	# print(drive["total_size"])
# 	# print(drive["info"])
# 	# print(drive["clips"])
# 	for clip in drive["clips"]:
# 		print(clip)
# 		print(validate_clip(clip["full_path"]))
		
# 		# run_muxer_complex("ingest_name",clip)
# 		break
# virtual_drives = drive_reader.read_clips_from_virtual_devices()
# print(virtual_drives)