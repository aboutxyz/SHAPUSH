# -*- coding:utf-8 -*-
import sys
import datetime
import time
from flask import Flask, g, request, make_response ,redirect
import hashlib
import xml.etree.ElementTree as ET
import threading
import MySQLdb


tips = u'请输入船名'
error_msg = u'暂无计划'
welcome = u"欢迎关注voyageschedule,查询最近船期,宁波船期请直接输入中文船名或英文船名,上海船期请输入sh+空格+船名(不用输+号)"

app = Flask(__name__)

app.debug = True
@app.route('/')
def hello():
    return redirect("http://voyagecheck.github.io/")
  
@app.route('/weixin', methods = ['GET', 'POST'] )
def wechat_auth():
  global Content1
  global msgcontent
  if request.method == 'GET':
    token = 'voyagett'
    query = request.args
    signature = query.get('signature', '')
    timestamp = query.get('timestamp', '')
    nonce = query.get('nonce', '')
    echostr = query.get('echostr', '')
    s = [timestamp, nonce, token]
    s.sort()
    s = ''.join(s)
    if ( hashlib.sha1(s).hexdigest() == signature ):  
      return make_response(echostr)
  else:
    #rec = request.stream.read()
    rec = request.data
    xml_recv1 = ET.fromstring(rec)
    msgtype = xml_recv1.find('MsgType').text
    if msgtype == "event":
        msgcontent = xml_recv1.find('Event').text
        if msgcontent == "subscribe":
            msgcontent = welcome
        ToUserName = xml_recv1.find("ToUserName").text
        FromUserName = xml_recv1.find("FromUserName").text
        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content></xml>"
        response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())),msgcontent ) )
        response.content_type='application/xml'
        return response
    else:
        xml_recv = ET.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text
        FromUserName = xml_recv.find("FromUserName").text
        Content = xml_recv.find("Content").text
        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"

        if Content == u'帮助':
            Content1 = tips
        elif Content.upper().startswith("SH "):
            db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='900502',db='voyagecheck',port=3306,charset='utf8')
            cursor=db.cursor()
            sql9 = r"select * from sipg where trim(replace(VESSELCN, ' ',  ''))=trim(replace(%s,' ','')) or trim(replace(VESSELEN, ' ',  ''))=trim(replace(%s,' ',''))"
            aa=cursor.execute(sql9,(Content[3:],Content[3:]))
            result =cursor.fetchmany(aa)
            Content1 = ''
            bb=len(result)-1
            if bb<0:
                Content1=error_msg
            else:
                data=result[bb]
                if data[1]==u'已离泊' and bb>0:
                    data = result[bb-1]
                    Content1=u'状态:'+data[1]+'\n'+u"码头:"+data[2]+'\n'+u"中文船名:"+data[3]+'\n'+u"英文船名:"+data[4]+'\n'+u"进口航次:"+data[5]+'\n'+u"出口航次:"+data[6]+'\n'+'ETA:'+data[7]+'\n'+'ATA:'+data[8]+'\n'+'ETD:'+data[9]+'\n'+'ATD:'+data[10]
                else:
                    Content1=u'状态:'+data[1]+'\n'+u"码头:"+data[2]+'\n'+u"中文船名:"+data[3]+'\n'+u"英文船名:"+data[4]+'\n'+u"进口航次:"+data[5]+'\n'+u"出口航次:"+data[6]+'\n'+'ETA:'+data[7]+'\n'+'ATA:'+data[8]+'\n'+'ETD:'+data[9]+'\n'+'ATD:'+data[10]
            data=()
            db.close()
            response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())), Content1 ) )
            response.content_type = 'application/xml'
            return response
        elif Content.upper().startswith("KG "):
            db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='900502',db='voyagecheck',port=3306,charset='utf8')
            cursor=db.cursor()
            sql9 = r"select * From sipgkg where id = (select max(id) from sipgkg where trim(replace(VESSELCN, ' ',  ''))=trim(replace(%s,' ','')) or trim(replace(VESSELEN, ' ',  ''))=trim(replace(%s,' ','')))"
            aa=cursor.execute(sql9,(Content[3:],Content[3:]))
            result =cursor.fetchmany(aa)
            Content1 = ''
            bb=len(result)-1
            if bb<0:
                Content1=error_msg
            else:
                data=result[bb]
                Content1=u"码头:"+data[1]+'\n'+u"中文船名:"+data[2]+'\n'+u"英文船名:"+data[3]+'\n'+u"出口航次:"+data[4]+'\n'+u'开港时间:'+data[5]+'\n'+u'截港时间:'+data[6]
            data=()
            db.close()
            response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())), Content1 ) )
            response.content_type = 'application/xml'
            return response
        else:
            # args = Content.split('@')
            # for i in range(len(args)): args[i] = args[i].encode('utf8') # pass test
            db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='900502',db='voyagecheck',port=3306,charset='utf8')
            cursor=db.cursor()
            sql9 = r"select * From voyagecheck where id = (select max(id) from voyagecheck where trim(replace(VESSELCN, ' ',  ''))=trim(replace(%s,' ','')) or trim(replace(VESSELEN, ' ',  ''))=trim(replace(%s,' ','')))"
            aa=cursor.execute(sql9,(Content,Content))
            result =cursor.fetchmany(aa)
            Content1 = ''
            bb=len(result)-1
            if bb<0:
                Content1=error_msg
            else:
                data=result[bb]
                Content1=u"码头:"+data[1]+'\n'+u"中文船名:"+data[2]+'\n'+u"英文船名:"+data[3]+'\n'+u"进口航次:"+data[4]+'\n'+u"出口航次:"+data[5]+'\n'+data[6]+'\n'+data[7]
            data=()
            db.close()
            response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())), Content1 ) )
            response.content_type = 'application/xml'
            return response


