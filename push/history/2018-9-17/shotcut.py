#coding:utf-8

import subprocess
import datetime

name = str(datetime.date.today())

result = subprocess.Popen(r'xvfb-run --server-args="-screen 0, 1024x768x24" CutyCapt --url=http://207.148.77.226:7070 --out='+name+'.png',shell=True)
result.wait()
