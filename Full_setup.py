import os
import sys
import subprocess
import time
import threading

firmadyne_dir = "./firmadyne/"
dependence_dir = "./dependence"


image_id = sys.argv[1]
type_name = sys.argv[2]



image_dir = "image_%s" %(image_id)



def find_program_helper(dir_name, str_name):
	os.chdir(dir_name)
	cmd = "find  . -name '%s'" %(str_name)
	res = os.popen(cmd)
	text =res.read()
	if len(text) == 0: #no results by find.
		os.chdir("../")
		return "", ""
	arr = text.strip().split("\n")
	for i in range(0, len(arr)):
		file_name = arr[i].strip("\n")
		file_cmd_str = "file %s" %file_name
		res = os.popen(file_cmd_str)
		text =res.read()
		if "executable" in text and "text executable" not in text: #executable not shell script
			os.chdir("../")
			return file_name, file_name.split("/")[-1].strip("\n")
		elif os.path.islink(file_name):
			real_file = os.readlink(file_name)
			os.chdir("../")
			return file_name, real_file.split("/")[-1].strip("\n")
		else:
			continue
	
	#not found
	os.chdir("../")
	return "", ""

def find_http_helper(dir_name, str_name):
	os.chdir(dir_name)
	cmd = "find  . -name '%s'" %(str_name)
	res = os.popen(cmd)
	text =res.read()
	if len(text) == 0: #no results by find.
		os.chdir("../")
		return "", ""
	arr = text.strip().split("\n")
	for i in range(0, len(arr)):
		file_name = arr[i].strip("\n")
		#for httpd finding (http.cgi")
		if "." in file_name[1:] or "-" in file_name or "config" in file_name or "_" in file_name:
			continue
		file_cmd_str = "file %s" %file_name
		res = os.popen(file_cmd_str)
		text =res.read()
		if "executable" in text and "text executable" not in text: #executable not shell script
			os.chdir("../")
			return file_name, file_name.split("/")[-1].strip("\n")
		else:
			continue
	
	#not found
	os.chdir("../")
	return "", ""

def get_short_name(http_name):
	arr = http_name.split("/")
	short_name = arr[len(arr) - 1].strip("\n")
	return short_name

def find_program(dir_name, test_name):
	#type_name in short, is real name for link. 
	#type name is short name of executable
	#type name is httpd, if test_name is "httpd"
	if "12933" in dir_name or "4671" in dir_name:
		prog_name, type_name = find_program_helper(dir_name, "mini_httpd")
		return prog_name, test_name
	if "20677" in dir_name or "19356" in dir_name:
		prog_name, type_name = find_program_helper(dir_name, "smd")
		return prog_name, test_name
		
	elif cmp(test_name, "httpd") == 0:
		prog_name, type_name = find_http_helper(dir_name, "*http*")
		if len(prog_name)!=0:
			return prog_name, "httpd"
		prog_name, type_name  = find_http_helper(dir_name, "*boa*")
		if len(prog_name)!=0:
			return prog_name, "httpd"
		prog_name, type_name  = find_http_helper(dir_name, "*web*")
		if len(prog_name)!=0:
			return prog_name, "httpd" 
		prog_name, type_name  = find_http_helper(dir_name, "*hydra*")
		if len(prog_name)!=0:
			return prog_name, "httpd" 
	else:
		prog_name, type_name = find_program_helper(dir_name, test_name)
		return prog_name, type_name

os.system("echo core >/proc/sys/kernel/core_pattern")
os.system("cd /sys/devices/system/cpu\necho performance | tee cpu*/cpufreq/scaling_governor\ncd -")

cmd = "cp %s/firmadyne.config ./" %firmadyne_dir
os.system(cmd)

print("##################prepare QEMU dependance#######################")
cmd = "cp dependence/vgabios-cirrus.bin %s" %image_dir
os.system(cmd)
cmd = "cp dependence/efi-e1000.rom %s" %image_dir
os.system(cmd)
cmd = "cp dependence/efi-pcnet.rom %s" %image_dir
os.system(cmd)

owd = os.getcwd()
os.chdir(firmadyne_dir)
print("##################copy QEMU#######################")
cmd = "./scripts/getArch.sh images/%s.tar.gz" %(image_id)
print(cmd)
res = os.popen(cmd)
text =res.read()
print("arch is ", text)
os.chdir(owd)

arch = ""
if "mipsel" in text:
	QEMU = "./qemu-mipsel"
	arch = "mipsel"
	copy_str = "cp %s/qemu-system-mipsel-full %s/qemu-system-mipsel"  %(dependence_dir, image_dir)
	os.system(copy_str)
elif "mipseb" in text:
	QEMU = "./qemu-mips"
	arch = "mipseb"
	copy_str = "cp %s/qemu-system-mips-full %s/qemu-system-mips" %(dependence_dir, image_dir)
	os.system(copy_str)
elif "armel" in text:
	QEMU = "./qemu-arm"
	arch = "armel"
	copy_str = "cp %s/qemu-system-arm-full %s/qemu-system-arm" %(dependence_dir, image_dir)
	os.system(copy_str)
else:
	print("#########################error########################")

print("##################copy kernel & IMAGE#######################")

cmd = "cp %s/scratch/%s/image.raw %s" %(firmadyne_dir, image_id, image_dir)
os.system(cmd)
if int(image_id) in [16385]:
	cmd = "cp %s/vmlinux.%s %s" %(dependence_dir, arch, image_dir)
else:
	cmd = "cp %s/vmlinux.%s_3.2.1 %s/vmlinux.%s" %(dependence_dir, arch, image_dir, arch)
os.system(cmd)


print("##################copy fuzzing stuff #######################")


#need afl-fuzz-full test.py run_full.sh
keyword_file = "keywords/%s/%s" %(type_name, image_id)

cmdstr = "cp %s %s/keywords" %(keyword_file, image_dir)
os.system(cmdstr)
cmdstr = "mkdir %s/inputs" %image_dir
os.system(cmdstr)


cmdstr = "rm %s/inputs/*" %image_dir
os.system(cmdstr)
if cmp(image_id, "18627")!=0:
	cmdstr = "cp %s/seed_get %s/inputs/" %(dependence_dir, image_dir)
	print("############", cmdstr)
	os.system(cmdstr)
else:
	cmdstr = "cp %s/seed_post %s/inputs/" %(dependence_dir, image_dir)
	os.system(cmdstr)
		
cmd = "cp %s/procinfo.ini %s" %(dependence_dir, image_dir)
os.system(cmd)

cmdstr = "cp %s/afl-fuzz-full %s/" %(dependence_dir, image_dir)
os.system(cmdstr)
cmdstr = "cp %s/test.py %s/" %(dependence_dir, image_dir)
os.system(cmdstr)
cmdstr = "python generate_run_full.py %s %s" %(image_id, arch)
os.system(cmdstr)
cmdstr = "cp -f %s/scratch/%s/run_full.sh %s/" %(firmadyne_dir, image_id, image_dir)
os.system(cmdstr)
cmdstr = "chmod 777 %s/run_full.sh" %image_dir
os.system(cmdstr)

prog_name, type_name  =  find_program(image_dir, type_name)
short_name = get_short_name(prog_name)


os.chdir(image_dir)


print("##################create FirmAFL_config#######################")

fp = open("FirmAFL_config", "w+")
fp.write("mapping_filename=mapping_table\n")
fp.write("init_read_pipename=user_cpu_state\n")
fp.write("write_pipename=full_cpu_state\n")
fp.write("program_analysis=%s\n" %short_name)
if "http" in short_name:
	fp.write("feed_type=FEED_HTTP\n")
else:
	fp.write("feed_type=FEED_ENV\n")
fp.write("id=%s" %image_id)
fp.close()