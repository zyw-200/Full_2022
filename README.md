# Full system emulation

## Setup

Our system is built upon the QEMU

### System mode
	cd qemu_mode/DECAF_qemu_2.10/
	./configure --target-list=mipsel-softmmu,mips-softmmu,arm-softmmu --disable-werror
	make

## Usage

1.  Download the Firmdyne repo to the **root directory of Full_2022**, then setup the firmadyne (e.g., ./download.sh) according to its instructions including importing its datasheet https://cmu.app.boxcn.net/s/hnpvf1n72uccnhyfe307rc2nb9rfxmjp into database.

2.  Replace the scripts/makeImage.sh, scripts/makeNetwork.py, scripts/getArch.sh, sources/extractor/extractor.py with modified one in **firmadyne_modify** directory.

3.  follow the guidance from firmadyne to generate the system running scripts. 
>Take DIR-815 router firmware as a example,
	
	cd firmadyne
	./sources/extractor/extractor.py -b dlink -sql 127.0.0.1 -np -nk "../firmware/DIR-815_FIRMWARE_1.01.ZIP" images
	./scripts/getArch.sh ./images/9050.tar.gz
	./scripts/makeImage.sh 9050
	./scripts/inferNetwork.sh 9050

	by using the makeImage.sh, the image_dir will be generated under Full_2022/


4. Setup for full-system emulation, 

	python Full_setup.py 9050 cgibin


5.  configuration for specific firmware

	e.g., for 9050 firmware, put following file in image_9050
	FirmAFL_config/9050/FirmAFL_config -> image_9050/
	FirmAFL_config/9050/test.py -> image_9050/
	FirmAFL_config/9050/seed -> image_9050/inputs/seed_get

6. run the fuzzing process
It will start the firmware emulation, and after the initialization of system and http process , send the request, then fuzzing process will start. (Maybe you should use root privilege to run it.)

	cd image_9050
	./run_full.sh
	python test.py 192.168.0.1



## Related Work

Our system is built on top of TriforceAFL, DECAF, AFL, and Firmadyne.

**TriforceAFL:** AFL/QEMU fuzzing with full-system emulation, https://github.com/nccgroup/TriforceAFL.

**DECAF:** "Make it work, make it right, make it fast: building a platform-neutral whole-system dynamic binary analysis platform", Andrew Henderson, Aravind Prakash, Lok Kwong Yan, Xunchao Hu, Xujiewen Wang, Rundong Zhou, and Heng Yin, to appear in the International Symposium on Software Testing and Analysis (ISSTA'14), San Jose, CA, July 2014. https://github.com/sycurelab/DECAF.

**AFL:** american fuzzy lop (2.52b), http://lcamtuf.coredump.cx/afl/.

**Firmadyne:** Daming D. Chen, Maverick Woo, David Brumley, and Manuel Egele. “Towards automated dynamic analysis for Linux-based embedded firmware,” in Network and Distributed System Security Symposium (NDSS’16), 2016. https://github.com/firmadyne.


## Troubleshooting

(1) error: static declaration of ‘memfd_create’ follows non-static declaration

Please see https://blog.csdn.net/newnewman80/article/details/90175033.

(2) failed to find romfile "efi-e1000.rom"  when run the "run.sh"

Use the run.sh in FirmAFL_config/9050/ instead.

(3) Fork server crashed with signal 11

Run scripts in start.py sequentially. First run "run.sh", when the testing program starts, run "python test.py", and "user.sh".

(4) For the id "12978", "16116" firmware, since these firmware have more than 1 test case, so we use different image directory name to distinguish them.
	
	Before FirmAFL_setup, 
	first, change image directory name image_12978 to image_129780, 
	then modify the firmadyne/scratch/12978 to firmadyne/scratch/129780
	After that, run python FirmAFL_setup.py 129780 mips
	(If you want to test another case for image_12978, you can use image_129781 instead image_129780)

