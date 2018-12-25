# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 16:21:06 2018

@author: Rajkumar
"""
import pandas as pd
import glob
import numpy as np
import sklearn
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt

# Read CSV file #####
lsp = pd.read_csv('D:\Rajkumar\Python\FlaskApp\data\lsp.csv')

## Split the training and tesing datasets from main datasets
test= lsp.iloc[11:16,1:10] 
train = lsp.iloc[np.r_[1:11,16:21],3:10]

## import support vector machine #####
from sklearn.svm import SVC
svc= SVC(kernel='rbf')
svc.fit(train.iloc[:,0:6],train.iloc[:,6])
pred = svc.predict(test.iloc[:,2:8])

#test1 = pd.DataFrame(test,index=[0,1,2,3,4])
pred1 = pd.DataFrame(pred)

## Reset the index in pred file
test=test.reset_index(drop=True)

## concatnate two dataframes into one dataframe
total=pd.concat([test,pred1],axis=1)

## Change the column name in total dataframe
total.columns = ['Name','Date','x','y','z','xi','yi','zi','output','prediction']

### Take the subset dataframe from large dataframe
new = total[['Name','y','x','prediction']]

## Export the final prediction 
total.to_csv('result.csv',index=False)

