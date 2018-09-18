#coding:utf-8
from __future__ import unicode_literals
import requests
import hashlib
import re
import time
import urllib
import random
from lxml import html
import urlparse
import logging
import json
# import socks  
# import socket
# from stem import Signal  
# from stem.control import Controller  
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# controller = Controller.from_port(port=9051)  
# controller.authenticate()  
# socks.set_default_proxy(socks.SOCKS5,"127.0.0.1",9050)  
# socket.socket = socks.socksocket  
# controller.signal(Signal.NEWNYM)


UserAgent_List = [
 "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
 "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
 "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
 "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
 "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
 "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
 "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
 "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
 "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
 "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
 "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
 "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
 "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
 "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
]


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler

handler = logging.FileHandler('/home/www/myappcron/finish.log')
handler.setLevel(logging.INFO)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger

logger.addHandler(handler)


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def get_cookie():
    with open('/home/www/myappcron/cookie','r') as f:
        cookies={}
        for line in f.read().split(';'):
            name,value=line.strip().split('=',1)  #1代表只分割一次
            cookies[name]=value 
        return cookies       
#agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
headers = {"Accept":"*/*",'User-Agent': random.choice(UserAgent_List),}
url= "http://www.hb56.com/PublicQuery/Schdule.ashx"
s = requests.session()
dictlist = []
dictlist1 = []
proxyi = 5
while proxyi>0:
    proxy = get_proxy()
    for x in "NSEW":
        data = {"vo":x,"shipName": "@1278","method": "0","terid": "-1","type": "0"}
        retry_count = 3
        while retry_count > 0:
            try:
                r= s.post(url,data=data,headers = headers,cookies=get_cookie(),proxies={"http": "http://{}".format(proxy)})
                #content = ('').join(r.content)
		print r.content
                resu = re.compile("~~")
                resua = resu.split(r.content)
                contentdict = json.loads(resua[1])
                dictlist.append(contentdict)
                contentdict1 = json.loads(resua[2])
                dictlist1.append(contentdict1)
                proxyi = 0
                break
            except Exception:
                logger.exception("Exception Logged")
                logger.info('aaaaaa')
                retry_count -= 1
        if retry_count<=0:
            delete_proxy(proxy)
            logger.info('proxy error')
            proxyi = proxyi-1
            break
        
        time.sleep(random.randint(16,21))
    
db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='900502',db='voyagecheck',port=3306,charset='utf8')
cursor=db.cursor()
try:
    for n in dictlist:
        for i in n["rows"]:
            #cursor.execute("SET NAMES utf8")
            if not(str(i["SBT_PSTTM"]).endswith("00:00") and str(i["SBT_PEDTM"]).endswith("00:00")):
                if (str(i["SBT_PSTTM"]) or str(i["SBT_PEDTM"]))!="None":
                    actsql = "INSERT INTO sipg1(STATUS,MATOU,VESSELCN,VESSELEN,IMVOYAGE,EXVOYAGE,ETA,ATA,ETD,ATD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(actsql,(str(i["VBTSTATUS"].encode("utf-8")),i["TERM"].encode("utf-8"),str(i["VSL_CHN_NAME"].encode("utf-8")),str(i["SCD_ENG_NAME"]),str(i["IVOYAGE"]),str(i["EVOYAGE"]),str(i["SBT_PSTTM"]),str(i["SBT_ASTTM"]),str(i["SBT_PEDTM"]),str(i["SBT_AEDTM"])))        
        db.commit()
        
        
    for n in dictlist1:
        for i in n["rows"]:
            actsql = "INSERT INTO sipgkg1(MATOU,VESSELCN,VESSELEN,EXVOYAGE,KAIGANG,JIEGANG) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(actsql,(i["TERM"].encode("utf-8"),str(i["SCD_CHN_NAME"].encode("utf-8")),str(i["SCD_ENG_NAME"]),str(i["EVOYAGE"]),str(i["SCD_RCVSTDT"]),str(i["SCD_RCVEDDT"])))      
        db.commit()
        
    
except:
    db.rollback()
    logger.exception("Exception Logged")
db.close()
logger.info('finish')
