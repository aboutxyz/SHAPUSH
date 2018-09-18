#coding:utf-8
from __future__ import unicode_literals
import MySQLdb
#from Tkinter import _flatten
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
    
    
class SIPG2(Base):
    __tablename__ = 'sipg2'
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


@app.route('/', methods=["GET","POST"])
def index():
    with open("shavessel.txt","r")as f:
        shavessel = f.read()

    shavessellist = shavessel.split("\n")
    shavessellist = filter(None,[i.strip() for i in shavessellist])
    engine = create_engine('mysql+mysqldb://root:900502@127.0.0.1:3306/voyagecheck?charset=utf8')
    DBSession = sessionmaker(bind=engine)
    # 创建Session:
    session = DBSession()
    resultslist1 = []
    for i in shavessellist:
        actsql = r"""select * From sipg2 where trim(replace(VESSELEN, ' ',  ''))=trim(replace("""+r'"'+i.lower()+r'"'+r""",' ',''))"""
        result = session.execute(actsql).fetchall()
        resultlist = []
        bb=len(result)-1
        if bb>=0:
            data=result[bb]
            if data[1]==u'已离泊' and bb>0:
                data = result[bb-1]
                resultlist.append(data)
            else:
                resultlist.append(data)
        resultslist1.append(resultlist)

        
    resultslist2 = []  
    for i in shavessellist:
        actsql = r"""select * From snlvessel where id = (select max(id) from snlvessel where trim(replace(VESSELEN, ' ',  ''))=trim(replace("""+r'"'+i.lower()+r'"'+r""",' ','')))"""
        result = session.execute(actsql).fetchall()
        resultslist2.append(result)
        
    resultslist3 = []  
    for i in shavessellist:
        actsql = r"""select * From sipgkg2 where id = (select max(id) from sipgkg2 where trim(replace(VESSELEN, ' ',  ''))=trim(replace("""+r'"'+i.lower()+r'"'+r""",' ','')))"""
        result = session.execute(actsql).fetchall()
        resultslist3.append(result)
        
    session.close()    
    resultall = []
    for i in zip(resultslist1,resultslist2):
        if i[0]:
            if i[0][0][6]==i[1][0][6].replace(" ", ""):
                _temp = list(i[0][0],)
                _temp.append(i[1][0][-1])
                resultall.append(_temp)
            else:
                _temp1 = list(i[0][0],)
                _temp1.append("")
                resultall.append(_temp1)
        else:
            resultall.append(list(i[1][0]))

    resultallcopy = resultall
    for i in range(len(resultallcopy)):
        if resultslist3[i]:
            if resultallcopy[i][6].replace(" ", "")==resultslist3[i][0][4]:
                resultall[i].append(resultslist3[i][0][5])
            else:
                resultall[i].append(" ")
        else:
            resultall[i].append(" ")
    
    return render_template('push.html',data=resultall)
    
if __name__ =="__main__":
    app.run(debug=True)