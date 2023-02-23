import os
import sys


def find_http_helper(dir_name, str_name):
	os.chdir(dir_name)
	cmd = "find  . -name '%s'" %(str_name)
	res = os.popen(cmd)
	text =res.read()
	arr = text.split("\n")
	for i in range(0, len(arr)):
		if "config" in arr[i] or "." in arr[i][1:] or "-" in arr[i]:
			continue
		elif os.path.isfile(arr[i].strip("\n")) == 0:
			continue
		else:
			break
	os.chdir("../")
	#print "*sssssss", os.getcwd(),arr[i]
	return arr[i]

def find_http(dir_name):
	http_name = find_http_helper(dir_name, "*http*")
	if len(http_name)!=0:
		return http_name
	http_name = find_http_helper(dir_name, "*boa*")
	if len(http_name)!=0:
		return http_name
	http_name = find_http_helper(dir_name, "*web*")
	if len(http_name)!=0:
		return http_name
	http_name = find_http_helper(dir_name, "*hydra*")
	if len(http_name)!=0:
		return http_name

def get_short_name(http_name):
	arr = http_name.split("/")
	short_name = arr[len(arr) - 1].strip("\n")
	return short_name

#need testlink.py, recoverlink.py, vgabios-cirrus.bin, efi-e1000.rom, procinfo.ini
image_id = sys.argv[1]
image_dir = "image_%s_bak" %image_id

cmd = "cp -r image_%s %s" %(image_id, image_dir)
print cmd
os.system(cmd)
cmd = "cp scratch/%s/run.sh %s" %(image_id, image_dir)
print cmd
os.system(cmd)

print "##################copy testlink.py#######################"
cmd = "cp testlink.py %s" %image_dir
os.system(cmd)
print "##################copy recoverlink.py#######################"
cmd = "cp recoverlink.py %s" %image_dir
os.system(cmd)

print "##################prepare QEMU dependance#######################"
cmd = "cp vgabios-cirrus.bin %s" %image_dir
os.system(cmd)
cmd = "cp efi-e1000.rom %s" %image_dir
os.system(cmd)
cmd = "cp efi-pcnet.rom %s" %image_dir
os.system(cmd)

print "##################copy QEMU#######################"
res = os.popen("./scripts/getArch.sh ./images/%s.tar.gz" %image_id)
text =res.read()

if "mipsel" in text:
	QEMU = "./qemu-mipsel"
	copy_str = "cp /home/zyw/FirmAFL_new/qemu_mode/DECAF_qemu_2.10/mipsel-softmmu/qemu-system-mipsel %s/"  %image_dir
	os.system(copy_str)
elif "mipseb" in text:
	QEMU = "./qemu-mips"
	copy_str = "cp /home/zyw/FirmAFL_new/qemu_mode/DECAF_qemu_2.10/mips-softmmu/qemu-system-mips %s/" %image_dir
	os.system(copy_str)
elif "armel" in text:
	QEMU = "./qemu-arm"
	copy_str = "cp /home/zyw/FirmAFL_new/qemu_mode/DECAF_qemu_2.10/arm-softmmu/qemu-system-arm %s/"  %image_dir
	os.system(copy_str)

print "##################copy procinfo.ini#######################"
cmd = "cp procinfo.ini %s" %image_dir
os.system(cmd)

http_name =  find_http(image_dir)
short_name = get_short_name(http_name)

os.chdir(image_dir)

print "##################create FirmAFL_config#######################"

fp = open("FirmAFL_config", "w+")
fp.write("mapping_filename=../mapping_table\n")
fp.write("init_read_pipename=../user_cpu_state\n")
fp.write("write_pipename=../full_cpu_state\n")
fp.write("program_analysis=%s\n" %short_name)
fp.write("feed_type=NONE\n")
fp.write("id=%s" %image_id)
fp.close()


print "##################testlink#######################"
os.system("python testlink.py")
print "##################run.sh#######################"
os.system("./run.sh")
print "##################recoverlink#######################"
os.system("python recoverlink.py")