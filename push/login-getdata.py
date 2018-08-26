#coding:utf-8

#from __future__ import unicode_literals
import requests
import random
import re
import time
import datetime
import sys 
import MySQLdb
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
loginurl = "http://ebusiness.sinolines.com.cn/snlebusiness/Default.aspx"
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
        "__VIEWSTATEGENERATOR":self.get__VIEWSTATEGENERATOR(loginurl),
        "__VIEWSTATE":self.get__VIEWSTATE(loginurl),
        "__EVENTVALIDATION":self.get__EVENTVALIDATION(loginurl),
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
        "TBUsername":"LYNBYY",
        "TBPassword":"123",
        "BTLogin":"�� ¼"}
        r= self.s.post(loginurl,data=postdata)
     

    def get_VIEWSTATEGENERATOR(self,url):
        r = self.s.post(url)
        VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
        
    def get__VIEWSTATE2(self,url):
        r = self.s.post(url)
        VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
        
        
    def get__SCROLLPOSITIONX(self,url):
        r = self.s.post(url)
        VIEWSTATE =re.findall(r'<input type="hidden" name="__SCROLLPOSITIONX" id="__SCROLLPOSITIONX" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
        
    def get__SCROLLPOSITIONY(self,url):
        r = self.s.post(url)
        VIEWSTATE =re.findall(r'<input type="hidden" name="__SCROLLPOSITIONY" id="__SCROLLPOSITIONY" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
        
    def get__EVENTVALIDATION2(self,url):
        r = self.s.post(url)
        VIEWSTATE =re.findall(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />', r.content,re.I)
        return VIEWSTATE[0]
        
        
    def get__alldata(self,url):
        aheaders = {"Connection":"keep-alive","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Host":"ebusiness.sinolines.com.cn","Origin":"http://ebusiness.sinolines.com.cn","Referer":"http://ebusiness.sinolines.com.cn/snlebusiness/SchedulePort.aspx","Upgrade-Insecure-Requests":"1",'User-Agent': agent,}
        r = self.s.post(url,headers = aheaders)
        __VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', r.content,re.I)
        __VIEWSTATEGENERATOR =re.findall(r'<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="(.*?)" />', r.content,re.I)
        __EVENTVALIDATION =re.findall(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />', r.content,re.I)
        return __VIEWSTATE[0],__VIEWSTATEGENERATOR[0],__EVENTVALIDATION[0],r.content
        

    
    def feed(self, args):
        self.s.headers={"Connection":"keep-alive","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Host":"ebusiness.sinolines.com.cn","Origin":"http://ebusiness.sinolines.com.cn","Referer":"http://ebusiness.sinolines.com.cn/snlebusiness/SchedulePort.aspx","Upgrade-Insecure-Requests":"1",'User-Agent': agent,}
        #self.s.headers.update({'Referer': 'http://ebusiness.sinolines.com.cn/snlebusiness/SchedulePort.aspx'})
        
        aa = self.get__alldata(vesselurl)
        
        nowweekday = datetime.date.today().weekday()
        lastsunday = datetime.date.today()+datetime.timedelta(days=-1-nowweekday) 
        nextsunday = datetime.date.today()+datetime.timedelta(days=6-nowweekday)
        lastsunday = lastsunday.strftime("%Y-%m-%d")
        nextsunday = nextsunday.strftime("%Y-%m-%d")
        
        postdata={"__EVENTTARGET":"",
        "__EVENTARGUMENT":"",
        #"__VIEWSTATE":self.get__VIEWSTATE2(vesselurl),
        "__VIEWSTATE":aa[0],
        #"__VIEWSTATEGENERATOR":self.get_VIEWSTATEGENERATOR(vesselurl),
        "__VIEWSTATEGENERATOR":aa[1],
        #"__SCROLLPOSITIONX":self.get__SCROLLPOSITIONX(vesselurl),
        "__SCROLLPOSITIONX":0,
        #"__SCROLLPOSITIONY":self.get__SCROLLPOSITIONY(vesselurl),
        "__SCROLLPOSITIONY":292,
        "__VIEWSTATEENCRYPTED":"",
        #"__EVENTVALIDATION":self.get__EVENTVALIDATION2(vesselurl),
        "__EVENTVALIDATION":aa[2],
        "autocomplete":"CNSHA",
        "ModeRBL":"vsl",
        "Calendarfromtime":lastsunday,
        "Calendartotime":nextsunday,
        "BTbyport":"�� ѯ"}
        r= self.s.post(vesselurl,data=postdata)
        resultdict = {}
        
        revname = re.compile(r'RowIndex="(.*?)" href="(.*?)">(.*?)</a>',re.I)
        result_name = revname.findall(r.content)
        resultname = [i[2].split("/")[0] for i in result_name]
        
        resultvoyage = [i[2].split("/")[1] for i in result_name]
        resultexvoyage = [i.split("  ")[0] for i in resultvoyage]
        resultimvoyage = [i.split("  ")[1] for i in resultvoyage]
        
        #���Ĵ����ÿո����
        resultnamecn = [" " ]*len(resultname)
        _status = [" " ]*len(resultname)
        _atb = [" " ]*len(resultname)
        _atd = [" " ]*len(resultname)
        
        revterminal = re.compile(r'ScheduleByportGridView_TERMINALH(.*?) target="_blank">(.*?)</a>',re.I)
        resultterminal = revterminal.findall(r.content)
        resultterminal = [i[1] for i in resultterminal]
        
        reveta = re.compile(r'ScheduleByportGridView_ATAL_(.*?)">(.*?)</span>',re.I)
        resulteta = reveta.findall(r.content)
        resulteta = [i[1] for i in resulteta]
        
        revetb = re.compile(r'ScheduleByportGridView_ATBL_(.*?)">(.*?)</span>',re.I)
        resultetb = revetb.findall(r.content)
        resultetb = [i[1] for i in resultetb]
        
        revetd = re.compile(r'ScheduleByportGridView_ATDL_(.*?)">(.*?)</span>',re.I)
        resultetd = revetd.findall(r.content)
        resultetd = [i[1] for i in resultetd]
        #��������ETA��ETB
        result = zip(_status,resultterminal,resultnamecn,resultname,resultimvoyage,resultexvoyage,resultetb,_atb,resultetd,_atd,resulteta)
        
        db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='900502',db='voyagecheck',port=3306,charset='utf8')
        cursor=db.cursor()
        #ʵ�����ݾ���ҪӢ�Ĵ��������Ĵ��������ں��Σ����ں��Σ���ͷ��ETA,ETB,ETU
        for i in result:
            try:
                actsql = "INSERT INTO snlvessel(STATUS,MATOU,VESSELCN,VESSELEN,IMVOYAGE,EXVOYAGE,ETA,ATA,ETD,ATD,ETASNL) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(actsql,(i))
                db.commit()
            except:
                db.rollback()
        db.close()
        
        return resultname,resulteta
      
        
p=GetLoginSHAVessel()
p.login("x")
time.sleep(3)
with open("shavessel.txt","wb")as f:
    for i in p.feed('x')[0]:
        f.write(i+"\r\n")
        