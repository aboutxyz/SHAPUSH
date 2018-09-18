#coding:utf-8
from __future__ import unicode_literals
import MySQLdb
from Tkinter import _flatten
from sqlalchemy import Column,Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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

resultslist3 = []  
for i in shavessellist:
    actsql = r"""select * From sipgkg1 where id = (select max(id) from sipgkg1 where trim(replace(VESSELEN, ' ',  ''))=trim(replace("""+r'"'+i.lower()+r'"'+r""",' ','')))"""
    result = session.execute(actsql).fetchall()
    resultslist3.append(result)
        
        
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