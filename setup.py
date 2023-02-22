import os
import sys
import subprocess
import time
import threading

firmadyne_dir = "/home/yaowen/firmadyne/"
dependence_dir = "home/yaowen/firmadyne/dependence"

os.system("echo core >/proc/sys/kernel/core_pattern")
os.system("cd /sys/devices/system/cpu\necho performance | tee cpu*/cpufreq/scaling_governor\ncd -")

print("##################prepare QEMU dependance#######################")
cmd = "cp dependence/vgabios-cirrus.bin %s" %image_dir
os.system(cmd)
cmd = "cp dependence/efi-e1000.rom %s" %image_dir
os.system(cmd)
cmd = "cp dependence/efi-pcnet.rom %s" %image_dir
os.system(cmd)

print("##################copy QEMU#######################")
res = os.popen("%s/scripts/getArch.sh ./images/%s.tar.gz" %(firmadyne_dir, image_id))
text =res.read()

arch = ""
if "mipsel" in text:
	QEMU = "./qemu-mipsel"
	arch = "mipsel"
	copy_str = "cp %s/qemu-system-mipsel-full %s/qemu-system-mipsel"  %(dependence_dir, image_id)
	os.system(copy_str)
elif "mipseb" in text:
	QEMU = "./qemu-mips"
	arch = "mipseb"
	copy_str = "cp %s/qemu-system-mips-full %s/qemu-system-mips" %(dependence_dir, image_id)
	os.system(copy_str)
elif "armel" in text:
	QEMU = "./qemu-arm"
	arch = "armel"
	copy_str = "cp %s/qemu-system-arm-full %s/qemu-system-arm" %(dependence_dir, image_id)
	os.system(copy_str)
else:
	print("#########################error########################")

cmd = "cp scratch/%s/image.raw %s" %(image_id, image_dir)
os.system(cmd)
if int(image_id) in [16385]:
	cmd = "cp %s/vmlinux.%s %s" %(dependence_dir, arch, image_dir)
else:
	cmd = "cp %s/vmlinux.%s_3.2.1 %s/vmlinux.%s" %(dependence_dir, arch, image_dir, arch)
os.system(cmd)


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
		
cmd = "cp dependence/procinfo.ini %s" %(dependence_dir, image_dir)
os.system(cmd)

cmdstr = "cp dependence/afl-fuzz-full %s/" %(dependence_dir, image_dir)
os.system(cmdstr)
cmdstr = "cp dependence/test.py %s/" %(dependence_dir, image_dir)
os.system(cmdstr)
cmdstr = "python generate_run_full.py %s %s" %(image_id, arch)
os.system(cmdstr)
cmdstr = "cp -f scratch/%s/run_full.sh %s/" %(image_id, image_dir)
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
fp.write("feed_type=FEED_HTTP\n")
fp.write("id=%s" %image_id)
fp.close()