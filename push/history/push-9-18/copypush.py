#coding:utf-8
from __future__ import unicode_literals
import requests
import time
import urlparse
import logging
import MySQLdb

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler

handler = logging.FileHandler('/home/www/push/finishcopypush.log')
handler.setLevel(logging.INFO)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger

logger.addHandler(handler)
    
db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='900502',db='voyagecheck',port=3306,charset='utf8')
cursor=db.cursor()
try:
    sql3 = "truncate sipg2;"
    cursor.execute(sql3)
    sql4 = "insert into sipg2 select * from sipg1;"
    cursor.execute(sql4)
    sql5 = "truncate sipgkg2;"
    cursor.execute(sql5)
    sql6 = "insert into sipgkg2 select * from sipgkg1;"
    cursor.execute(sql6)
except:
    logger.exception("Exception Logged")
db.close()
logger.info('finish')