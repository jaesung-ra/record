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

dump.dump('./dump_file',prediction,algo)







