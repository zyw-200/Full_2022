import os
import sys

def generate_run_full(image_id, arch):
	script_src = "scratch/%s/run.sh" %image_id
	script_dst = "scratch/%s/run_full.sh" %image_id
	file_src = open(script_src)
	file_dst = open(script_dst, "w+")
	remove_flag = 0
	device_flag = 0
	mount_flag = 0
	for line in file_src.readlines():
		if "DEVICE=" in line:
			mount_flag = 1
			continue
		elif "del_partition" in line:
			mount_flag = 0
			continue
		if mount_flag == 1:
			continue

		if remove_flag == 1:
			remove_flag = 0
		if device_flag == 1:
			device_flag = 0
			file_dst.write("	-aflFile @@ \n")
		elif "Starting emulation of firmware" in line:
			file_dst.write(line)
			archh = arch
			if cmp(arch, "mipseb") == 0:
				archh = "mips"
			newline_0 = "QEMU=./qemu-system-%s\n" %archh
			newline_1 = "KERNEL='./vmlinux.%s'\n" %arch
			newline_2 = "IMAGE='./image.raw'\n"
			#newline1 = "AFL=\"./afl-fuzz-full -m none -t 800000+  -i ./inputs -o ./outputs_full -x keywords -QQ -- \"\n"
			newline1 = "AFL=\"./afl-fuzz-full -m none -t 800000+  -i ./inputs -o ./outputs_full -QQ -- \"\n"
			newline2 = "${AFL} "
			file_dst.write(newline_0)
			file_dst.write(newline_1)
			file_dst.write(newline_2)
			file_dst.write(newline1)
			file_dst.write(newline2)
			remove_flag = 1 #next line should be removed
		elif "-serial" in line:
			continue
		elif "-monitor" in line:
			continue
		elif "-display none" in line:
			file_dst.write("	-nographic \\\n")
			continue
		elif "| true" in line:
			new_line = line.split("|")[0] + "\\\n"
			file_dst.write(new_line)
			device_flag = 1			
		else:
			file_dst.write(line)
	
	file_src.close()
	file_dst.close()
	chmod_str = "chmod 777 %s" %script_dst
	os.system(chmod_str)


#single

image_id = sys.argv[1]	
arch = sys.argv[2]
generate_run_full(image_id, arch)

'''
fp = open("testlist")
for line in fp.readlines():
	array = line.split(":")
	image_id = array[0].strip()
	generate_run_full(image_id)
fp.close()
'''