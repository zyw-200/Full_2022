import subprocess
import time
import os
import shutil
import sys

id=sys.argv[1]

cmdstr ="./run_full.sh"
subprocess.Popen(cmdstr,stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
time.sleep(80)
cmdstr ="python test.py"
os.system(cmdstr)

