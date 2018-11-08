import os



def share_validate(drive_letter, pxy_server, pxy_path, share_user, share_pass):
	return_value = False
	print("Buscando: ",drive_letter)
	if(os.path.exists(drive_letter+":\\")):
		print("Existe ", drive_letter)
		return_value = True
	else:
		print("Mapeando p:")
		map_cmd = "net use "+drive_letter+": \\\\"+pxy_server+"\\"+pxy_path+" /user:"+share_user+" "+share_pass
		os.system(map_cmd)
		if(os.path.exists(drive_letter+":\\")):
			print("existe ", drive_letter)
			return_value = True
		else:
			return_value = False

	return return_value



pxy_server  = "SMEX-PXYSVR"
pxy_path = "proxy"
share_user = "GVAdmin"
share_pass = "adminGV!"
drive_letter = "P"

pxy_file_hash = "f55d8c7dff0644dcbfcce09b6811705d"

pxy_exists = share_validate(drive_letter, pxy_server, pxy_path, share_user, share_pass)

if(pxy_exists):
	print("Buscando PXY")
	if(os.path.exists(drive_letter+":\\"+pxy_file_hash)):
		print("Has PXY")
		if(os.path.exists(drive_letter+":\\"+pxy_file_hash+"\\proxy.mp4")):
			print("Has Media")

	else:
		print("Not PXY")

print(pxy_exists)