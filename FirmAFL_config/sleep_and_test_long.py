import os
import time
import sys

id=sys.argv[1]

time.sleep(110)
cmdstr ="python test_%s.py" %id
os.system(cmdstr)