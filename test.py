import psutil
import os
import re

addrs = psutil.net_if_addrs()
print(addrs.keys())

test = "C:\\Users\\Guillaume\\Downloads\\ubuntu-22.04.3-live-server-amd64.iso"

if os.path.isfile(test.encode('unicode_escape')) == True:
    print("ok")