#coding:utf-8
import MySQLdb
with open("shavessel.txt","r")as f:
    shavessel = f.read()
db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='900502',db='voyagecheck',port=3306,charset='utf8')
cursor=db.cursor()    
shavessellist = shavessel.split("\n")
shavessellist = [i.strip() for i in shavessellist]
resultslist = []
for i in shavessellist:
    actsql = r"select * From sipg1 where id = (select max(id) from sipg1 where trim(replace(VESSELEN, ' ',  ''))=trim(replace(%s,' ','')))" 
    cursor.execute(actsql,i.lower())
    result = cursor.fetchall()
    resultslist.append(result)


   
for i in resultslist:
    for j in i:
        print j[4]

# import difflib
# d = difflib.Differ()#创建Differ对象
# diff = d.compare(shavessellist[1].lower(),"sitc yokohama")
# print('\n'.join(list(diff)))

# actsql = "SELECT * FROM sipg1 WHERE VESSELEN LIKE %s"
# cursor.execute(actsql,shavessellist[1].split('/n')[0])
# result = cursor.fetchall()
# print result