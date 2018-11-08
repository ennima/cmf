import os, shutil, json
import subprocess
import ftplib

from time import time as time_i
from datetime import datetime



def ftpSend(host,user,passs,destFolder,newFile):
    
    print("New File",newFile)
    passs = ""
    ftp = ftplib.FTP(host)
    ftp.login(user,passs)
    ftp.cwd(destFolder)
    #print ftp.pwd()
    print ("Enviando ",os.path.basename(newFile) ," a ftp Dest...")
    ftp.storbinary('STOR '+os.path.basename(newFile),open(newFile,'rb'))
    ftp.quit()
    print ("Listo.")


def transcode_media(clip,path,FinalVideo,render_engine, temp_dir, stratus_obj):
    print(FinalVideo)
    print(path)
    
    if(not "._" in clip) and (not ".textClipping" in clip):
        name_split = clip.strip().split(".")
        test = 0
        print(len(name_split))
        print(len(name_split[0].strip()))
        
        if(len(name_split[0].strip()) == 0):
            print("No lo hago ")
        else:
            print("#Transcodificando: ",clip.strip())
            
            if(os.path.exists(temp_dir)) and (test == 0):
				
                print("Existe el directorio de cache")
                if("." in path):
                	videoMerge = render_engine+' -y -i "'+clip+'" -vcodec mpeg2video -vtag xd5b -s 1920x1080 -aspect 16:9 -pix_fmt yuv420p -rtbufsize 50000k -b:v 50000k -dc 9 -flags +ilme+ildct -top 1 -f mxf "'+temp_dir+FinalVideo+'".mxf'
                else:
	                # videoMerge = ffmpeg_path+'ffmpeg -i "'+path+clip+'" -vcodec mpeg2video -vtag xd5b -s 1920x1080 -pix_fmt yuv420p -r 29.97 -rtbufsize 50000k -b:v 50000k -dc 9 -flags +ilme+ildct -top 1 -acodec pcm_s16le -ac 4 -f mxf "'+temp_dir+FinalVideo+'".mxf'
	                videoMerge = render_engine+' -y -i "'+path+"\\"+clip+'" -vcodec mpeg2video -vtag xd5b -s 1920x1080 -aspect 16:9 -pix_fmt yuv420p -rtbufsize 50000k -b:v 50000k -dc 9 -flags +ilme+ildct -top 1 -f mxf "'+temp_dir+FinalVideo+'".mxf'
                print(videoMerge)
               
                p = subprocess.Popen(videoMerge)
                p.wait()
                print("Enviando: "+temp_dir+FinalVideo)
                test += 1

                ftpSend(stratus_obj["stratus_ftp"],stratus_obj["stratus_ftp_user"],stratus_obj["stratus_ftp_pass"],stratus_obj["ingest_folder"],temp_dir+FinalVideo+'.mxf')
                drive =""
                
                print(FinalVideo,' ingestado.')
            else:
                print("no esta")
                if (temp_dir == "."):
                	temp_dir = ""
        

def seconds_timestamp(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)																																																																															
	restore_time = "%02d:%02d:%02d" % (h, m, s)
	# print ("Tardó:",restore_time)
	return(restore_time)        


def share_validate(drive_letter, pxy_server, pxy_path, share_user, share_pass):
	return_value = False
	print("Buscando: ",drive_letter)
	if(os.path.exists(drive_letter+":\\")):
		print("Existe ", drive_letter)
		return_value = True
	else:
		print("Mapeando p:")
		map_cmd = "net use "+drive_letter+": \\\\"+pxy_server+"\\"+pxy_path+" /user:"+share_user+" "+share_pass
		print(map_cmd)
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
pxy_file_hash = "e18e87aa772b4622a2f36380036e0c54"
dst_path = "."
dst_name_file = "metro_in"
render_engine = "C:\\Users\\ennima\\Desktop\\ffXperiments\\render.exe"
pxy_exists = share_validate(drive_letter, pxy_server, pxy_path, share_user, share_pass)

stratus_obj = {"stratus_ftp":"192.168.196.139","stratus_ftp_user":"mxfmovie","stratus_ftp_pass":"","ingest_folder":"test"}

tiempo_inicial = time_i()


if(pxy_exists):
	print("Buscando PXY")
	if(os.path.exists(drive_letter+":\\"+pxy_file_hash)):
		print("Has PXY")
		if(os.path.exists(drive_letter+":\\"+pxy_file_hash+"\\proxy.mp4")):
			print("Has Media")
			shutil.copy2(drive_letter+":\\"+pxy_file_hash+"\\proxy.mp4", dst_path+"\\"+dst_name_file+".mp4")
			transcode_media(dst_name_file+".mp4",dst_path,dst_path+"\\"+dst_name_file,render_engine,".",stratus_obj)
	else:
		print("Not PXY")

print(pxy_exists)


tiempo_final = time_i()
tiempo_ejecucion = tiempo_final - tiempo_inicial
print("Tardó: " , tiempo_ejecucion,"s")
print(seconds_timestamp(tiempo_ejecucion))