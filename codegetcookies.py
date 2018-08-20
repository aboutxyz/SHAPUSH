# -*- coding:utf-8 -*-
import sys
import time
import datetime
import requests
# import urllib
# import urllib2
import re
import cookielib
import StringIO
# from aip import AipOcr
from PIL import Image
import random
import logging
from rk import RClient


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler

handler = logging.FileHandler('/home/www/myappcron/finishgetcode.log')
handler.setLevel(logging.INFO)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger

logger.addHandler(handler)

account1 = "MAERSKOP"
account2 = "CHECKSIPG"

begintime = datetime.date(2018,7,12)
now = datetime.date.today()
convert = divmod((now-begintime).days,2)[0]
if convert%2 == 0:
    account = account2
else:
    account = account1


url='http://www.hb56.com/'
loginurl = "http://www.hb56.com/Login.aspx"
indexurl = "http://www.hb56.com/index.aspx"
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

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


class SharkSearcher1():
    def __init__(self):
        #agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        self.headers_sipg={"Accept":"*/*","Origin":"http://www.hb56.com","Referer":"http://www.hb56.com/Login.aspx",'User-Agent': random.choice(UserAgent_List),}
        self.s=requests.Session()
        self.s.headers=self.headers_sipg
    
    
    def get_hiddenvalue(self,url,proxy):
        r = self.s.post(url,proxies={"http": "http://{}".format(proxy)})
        VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
        
        
    def get_hiddenvalue1(self,url,proxy):
        r = self.s.post(url,proxies={"http": "http://{}".format(proxy)})
        VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
    
    def get_code(self,imageUrl,proxy):
        textcode=""                
        try:  
            im = self.s.post(imageUrl,proxies={"http": "http://{}".format(proxy)})            
            img_buffer = StringIO.StringIO(im.content)
            img = Image.open(img_buffer)
            img.save("/home/www/myappcron/code.png","png")
            im = open('/home/www/myappcron/code.png', 'rb').read()
            tempcode = rc.rk_create(im, 3040)
            textcode = tempcode["Result"]            
            return textcode
        except Exception as e:  
            #print 'Failed to get imagecode!', e  
            return ''   
 
    def feed(self,args,proxy):
        
        #参数设置
        VIEWSTATE=self.get_hiddenvalue(loginurl,proxy)
        VIEWSTATE1=self.get_hiddenvalue1(loginurl,proxy)
        M_USER_NAME=account
        S_PASSWORD="Aa1107760775"
        rdcode=self.get_code(url+"LoginRdCode.aspx",proxy)
        #print rdcode
        
        
        postdata={
            "__VIEWSTATE": VIEWSTATE,
            "__VIEWSTATEGENERATOR": VIEWSTATE1,
            "M_USER_NAME": M_USER_NAME,
            "S_PASSWORD": S_PASSWORD,
            "rdcode": rdcode
            }
        
        r = self.s.post(loginurl,data=postdata,proxies={"http": "http://{}".format(proxy)})
        time.sleep(2)
        r = self.s.post(indexurl,proxies={"http": "http://{}".format(proxy)})
        content = r.content
        #print self.s.cookies
        templist = []
        for k,v in self.s.cookies.items():
            templist.append(str(k)+"="+str(v))
        sym = ";"
        with open("/home/www/myappcron/cookie","w+")as f:
            f.write(sym.join(templist))
        # new_cookie_jar = cookielib.LWPCookieJar(filename="cookies")
        # requests.utils.cookiejar_from_dict({c.name: c.value for c in self.s.cookies}, new_cookie_jar)
        # new_cookie_jar.save(ignore_discard=True)
        return content
        
        
p=SharkSearcher1()
rc =RClient('haishangmuxucao', 'Aa1107760775', '101242', '8f9d9d8f880d4ded8252285c85945b43')
for i in range(5):
    proxy = get_proxy()
    try:
        content = p.feed('x',proxy)
        if account in content:
            #print content
            break
        else:
            #print "error"
            logger.info('error')
    except:
        delete_proxy(proxy)
        logger.exception("Exception Logged")
        logger.info('bbbbbb')
    time.sleep(10)
    
logger.info('finish')
