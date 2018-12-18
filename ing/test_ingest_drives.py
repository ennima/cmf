from ingest_drives import *

drives_to_discard = ['C:\\','V:\\']
ingest_device_conf1 = "./ingest_device.json"

drive_reader = IngestDrivers(drives_to_discard,ingest_device_conf1)

drives = drive_reader.read_clips_from_devices()

print(len(drives))
for drive in drives:
	
	for clip in drive["clips"]:
		print(clip)
		print(validate_clip(clip["full_path"]))
		
		
		break

