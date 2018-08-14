#coding:utf-8

#from __future__ import unicode_literals
import requests
import random
import re

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
headers = {"Accept":"*/*",'User-Agent': random.choice(UserAgent_List),}
url = "http://ebusiness.sinolines.com.cn/snlebusiness/Default.aspx"

class GetLoginSHAVessel:
    def __init__(self):
        agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        self.headers_snl={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Origin":"http://ebusiness.sinolines.com.cn","Referer":"http://ebusiness.sinolines.com.cn/snlebusiness/Default.aspx",'User-Agent': agent,}
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

        
        
       
    def feed(self, args):
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
        r= self.s.post(url,data=postdata,headers = headers)
        content = r.content
        templist = []
        for k,v in self.s.cookies.items():
            templist.append(str(k)+"="+str(v))
        sym = ";"
        with open("cookie","w+")as f:
            f.write(sym.join(templist))
        
        
p=GetLoginSHAVessel()
p.feed("x")
    
        