#coding:utf-8
from __future__ import unicode_literals
import MySQLdb
from flask import Flask, render_template,request,session
app = Flask(__name__)

with open("shavessel.txt","r")as f:
    shavessel = f.read()

db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='900502',db='voyagecheck',port=3306,charset='utf8')
cursor=db.cursor()

shavessellist = shavessel.split("\n")
shavessellist = filter(None,[i.strip() for i in shavessellist])
resultslist = []
for i in shavessellist:
    actsql = r"select * From sipg1 where id = (select max(id) from sipg1 where trim(replace(VESSELEN, ' ',  ''))=trim(replace(%s,' ','')))"
    cursor.execute(actsql,(i.lower(),))
    result = cursor.fetchall()
    resultslist.append(result)


@app.route('/', methods=["GET","POST"])
def index():
    return render_template('push.html',data=resultslist)
    
if __name__ =="__main__":
    app.run(debug=True)