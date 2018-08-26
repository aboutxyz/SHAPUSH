#coding:utf-8
from __future__ import unicode_literals
import MySQLdb
from Tkinter import _flatten
from flask import Flask, render_template,request,session
app = Flask(__name__)

with open("shavessel.txt","r")as f:
    shavessel = f.read()

db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='900502',db='voyagecheck',port=3306,charset='utf8')
cursor=db.cursor()

shavessellist = shavessel.split("\n")
shavessellist = filter(None,[i.strip() for i in shavessellist])

resultslist1 = []
for i in shavessellist:
    actsql = r"select * From sipg1 where id = (select max(id) from sipg1 where trim(replace(VESSELEN, ' ',  ''))=trim(replace(%s,' ','')))"
    cursor.execute(actsql,(i.lower(),))
    result = cursor.fetchall()
    resultslist1.append(result)
  
resultslist2 = []  
for i in shavessellist:
    actsql = r"select * From snlvessel where id = (select max(id) from snlvessel where trim(replace(VESSELEN, ' ',  ''))=trim(replace(%s,' ','')))"
    cursor.execute(actsql,(i.lower(),))
    result = cursor.fetchall()
    resultslist2.append(result)   
db.close()
resultall = []

for i in zip(resultslist1,resultslist2):
    if i[0]:
        if i[0][0][5]==i[1][0][5]:
            resultall.append(i[0][0]+(i[1][0][-1],))
        else:
            resultall.append(i[0][0]+("",))
    else:
        resultall.append(i[1][0])
    #break
@app.route('/', methods=["GET","POST"])
def index():
    return render_template('push.html',data=resultall)
    
if __name__ =="__main__":
    app.run(debug=True)