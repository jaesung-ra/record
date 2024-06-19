from openpyxl import load_workbook
from h11 import Data
from surprise import SVD, Prediction, SVDpp, SlopeOne, NMF, NormalPredictor, KNNBasic, KNNBaseline, KNNWithMeans, KNNWithZScore, BaselineOnly, CoClustering, dump
from surprise.model_selection import cross_validate
from surprise import Reader
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
import random
import pandas as pd
from surprise import dump
import pymysql


submit_log=pd.read_csv('./surp.csv')
reader = Reader(rating_scale=(0,1))
data=Dataset.load_from_df(submit_log,reader)


sim_options={'user_based': False}
algo=KNNBasic(k=40,min_k=1,sim_options=sim_options)
trainset=data.build_full_trainset()
print('KNN')
algo.fit(trainset)
testset=trainset.build_testset()
prediction=algo.test(testset)
accuracy.rmse(prediction)

conn = pymysql.connect(host='127.0.0.1', user='root',
                       password='0000', db='recodb', charset='utf8')
cur = conn.cursor()
cur.execute("select username from test group by username")
users = list(list(zip(*cur.fetchall()))[0])
cur.execute("select code from tmp")
codes=list(list(zip(*cur.fetchall()))[0])
for user in users:
  predictions=[algo.predict(user,code)for code in codes]
  def sortest(pred):
    return pred.est
  predictions.sort(key=sortest,reverse=True)
  length=len(predictions)
  top=predictions[:20]
  bot=predictions[length-20:]
  mid=predictions[length//2-10:length//2+10]
  for pred in top:
    user=pred.uid
    code=pred.iid
    data=(user,code,"t")
    query="insert into recommend (username,code,tooltip) values (%s,%s,%s)"
    cur.execute(query,data)
  for pred in bot:
    user=pred.uid
    code=pred.iid
    data=(user,code,"b")
    query="insert into recommend (username,code,tooltip) values (%s,%s,%s)"
    cur.execute(query,data)
  for pred in mid:
    user=pred.uid
    code=pred.iid
    data=(user,code,"m")
    query="insert into recommend (username,code,tooltip) values (%s,%s,%s)"
    cur.execute(query,data)







