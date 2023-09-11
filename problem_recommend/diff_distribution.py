from collections import defaultdict
from turtle import color
from types import NoneType
import pymysql
import time
import matplotlib.pyplot as plt
import math



db=pymysql.connect(host='localhost',port=3306,user='root',passwd='0000',db='recodb',charset='utf8')
cursor=db.cursor()
diff=[]
sql=f"select difficulty,group_concat(tag separator', ') as tag from tmp group by code order by difficulty ;"
cursor.execute(sql)
result=cursor.fetchall()

for res in result:
    diff.append(res[0])
plt.hist(diff,bins=200)
per=len(result)//20

for i in range(1,20):
    xcor=diff[per*i]
    print(i,diff[per*i])
    plt.axvline(x=xcor,ymax=1,ymin=0, color='red',linestyle='dashed')
plt.show()
