#coding:utf-8
from __future__ import unicode_literals
import MySQLdb
from Tkinter import _flatten
from flask import Flask, render_template,request,session
from sqlalchemy import Column,Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# 创建对象的基类:
Base = declarative_base()

class SNLVESSEL(Base):
    __tablename__ = 'snlvessel'
    ID = Column(Integer, primary_key=True)
    STATUS = Column(String(1200))
    MATOU = Column(String(1200))
    VESSELCN = Column(String(1200))
    VESSELEN = Column(String(1200))
    IMVOYAGE = Column(String(1200))
    EXVOYAGE = Column(String(1200))
    ETA = Column(String(1200))
    ATA = Column(String(1200))
    ETD = Column(String(1200))
    ATD = Column(String(1200))
    ETASNL = Column(String(1200))
    
    
class SIPG1(Base):
    __tablename__ = 'sipg1'
    ID = Column(Integer, primary_key=True)
    STATUS = Column(String(1200))
    MATOU = Column(String(1200))
    VESSELCN = Column(String(1200))
    VESSELEN = Column(String(1200))
    IMVOYAGE = Column(String(1200))
    EXVOYAGE = Column(String(1200))
    ETA = Column(String(1200))
    ATA = Column(String(1200))
    ETD = Column(String(1200))
    ATD = Column(String(1200))

    
with open("shavessel.txt","r")as f:
    shavessel = f.read()

shavessellist = shavessel.split("\n")
shavessellist = filter(None,[i.strip() for i in shavessellist])

@app.route('/', methods=["GET","POST"])
def index():
    engine = create_engine('mysql+mysqldb://root:900502@localhost:3306/voyagecheck?charset=utf8')
    DBSession = sessionmaker(bind=engine)

    # 创建Session:
    session = DBSession()
    resultslist1 = []
    for i in shavessellist:
        actsql = r"""select * From sipg1 where id = (select max(id) from sipg1 where trim(replace(VESSELEN, ' ',  ''))=trim(replace("""+r'"'+i.lower()+r'"'+r""",' ','')))"""
        result = session.execute(actsql).fetchall()
        resultslist1.append(result)
    resultslist2 = []  
    for i in shavessellist:
        actsql = r"""select * From snlvessel where id = (select max(id) from snlvessel where trim(replace(VESSELEN, ' ',  ''))=trim(replace("""+r'"'+i.lower()+r'"'+r""",' ','')))"""
        result = session.execute(actsql).fetchall()
        resultslist2.append(result)
    resultall = []
    for i in zip(resultslist1,resultslist2):
        if i[0]:
            if i[0][0][5]==i[1][0][5]:
                _temp = list(i[0][0],)
                _temp.append(i[1][0][-1])
                resultall.append(_temp)
            else:
                _temp = list(i[0][0],)
                _temp.append("")
                resultall.append(_temp)
        else:
            resultall.append(list(i[1][0]))
    
    return render_template('push.html',data=resultall)
    
if __name__ =="__main__":
    app.run(debug=True)