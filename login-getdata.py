#coding:utf-8

#from __future__ import unicode_literals
import requests
import random
import re
import time
import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")

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
#headers = {"Accept":"*/*",'User-Agent': random.choice(UserAgent_List),}
agent = random.choice(UserAgent_List)
url = "http://ebusiness.sinolines.com.cn/snlebusiness/Default.aspx"
vesselurl = "http://ebusiness.sinolines.com.cn/snlebusiness/SchedulePort.aspx"

class GetLoginSHAVessel:
    def __init__(self):
        #agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        self.headers_snl={"Connection":"keep-alive","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Content-Type":"application/x-www-form-urlencoded","Host":"ebusiness.sinolines.com.cn","Origin":"http://ebusiness.sinolines.com.cn","Referer":"http://ebusiness.sinolines.com.cn/snlebusiness/Default.aspx","Upgrade-Insecure-Requests":"1",'User-Agent': agent,}
        self.s=requests.Session()
        self.s.headers=self.headers_snl
    
    
    def get__VIEWSTATE(self,url):
        r = self.s.post(url)
        VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
        
    def get__EVENTVALIDATION(self,url):
        r = self.s.post(url)
        VIEWSTATE =re.findall(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
        
    def get__VIEWSTATEGENERATOR(self,url):
        r = self.s.post(url)
        VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
        
    def login(self, args):
        postdata={"__EVENTTARGET":"",
        "__EVENTARGUMENT":"",
        "__LASTFOCUS":"",
        "__VIEWSTATEGENERATOR":self.get__VIEWSTATEGENERATOR(url),
        "__VIEWSTATE":self.get__VIEWSTATE(url),
        "__EVENTVALIDATION":self.get__EVENTVALIDATION(url),
        "dl_seltype":"blno",
        "CargoTrackingBLNOTB":"",
        "autocomplete":"",
        "autocompletemore":"",
        "ScheduleActivefromtime":"2018-08-14",
        "ScheduleActivetotime":"2018-08-24",
        "autocompletepol":"",
        "SchedulePortfromtime":"2018-08-13",
        "SchedulePorttotime":"2018-08-20",
        "ModeRBL":"all",
        "VslModeRBL":"vsl",
        "dlallvsl":"",
        "TxtVoy":"",
        "TBUsername":"LYNBAGT",
        "TBPassword":"123",
        "BTLogin":"µÇ Â¼"}
        r= self.s.post(url,data=postdata,headers = self.s.headers)
     

    def get_VIEWSTATEGENERATOR(self,url):
        r = self.s.post(vesselurl)
        VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
        
    def get__SCROLLPOSITIONX(self,url):
        r = self.s.post(vesselurl)
        VIEWSTATE =re.findall(r'<input type="hidden" name="__SCROLLPOSITIONX" id="__SCROLLPOSITIONX" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
        
    def get__SCROLLPOSITIONY(self,url):
        r = self.s.post(vesselurl)
        VIEWSTATE =re.findall(r'<input type="hidden" name="__SCROLLPOSITIONY" id="__SCROLLPOSITIONY" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
        
    def get__EVENTVALIDATION2(self,url):
        r = self.s.post(vesselurl)
        VIEWSTATE =re.findall(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]

    
    def feed(self, args):
        self.s.headers={"Connection":"keep-alive","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Content-Type":"application/x-www-form-urlencoded","Host":"ebusiness.sinolines.com.cn","Origin":"http://ebusiness.sinolines.com.cn","Referer":"http://ebusiness.sinolines.com.cn/snlebusiness/SchedulePort.aspx","Upgrade-Insecure-Requests":"1",'User-Agent': agent,}
        #self.s.headers.update({'Referer': 'http://ebusiness.sinolines.com.cn/snlebusiness/SchedulePort.aspx'})
        postdata={#"__EVENTTARGET":"",
        #"__EVENTARGUMENT":"",
        #"__VIEWSTATE":"",
        "__VIEWSTATEGENERATOR":self.get_VIEWSTATEGENERATOR(vesselurl),
        "__SCROLLPOSITIONX":self.get__SCROLLPOSITIONX(vesselurl),
        #"__SCROLLPOSITIONY":self.get__SCROLLPOSITIONY(vesselurl),
        "__SCROLLPOSITIONY":292,
        #"__VIEWSTATEENCRYPTED":"",
        "__EVENTVALIDATION":self.get__EVENTVALIDATION2(vesselurl),
        "autocomplete":"SHANGHAI , CHINA (CNSHA)",
        "ModeRBL":"vsl",
        "Calendarfromtime":"2018-08-12",
        "Calendartotime":"2018-08-19",
        "BTbyport":"²é Ñ¯"}
        r= self.s.post(vesselurl,data=postdata)
        print r.content
        resultlist = []
        recheck = re.compile(r'RowIndex="(.*?)" href="(.*?)">(.*?)</a>',re.I)
        resulta = recheck.findall(r.content)
        for i in range(len(resulta)):
            result = resulta[i][2].split("/")[0]
            resultlist.append(result)
        return resultlist
        
        
p=GetLoginSHAVessel()
p.login("x")
print "one step ok"
time.sleep(3)
with open("shavessel.txt","wb")as f:
    for i in p.feed('x'):
        f.write(i)
    
        