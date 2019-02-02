# -*- coding: utf-8 -*-
"""
@author: Rajkumar
"""
import pandas as pd
import numpy as np
#import sklearn
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV, train_test_split, cross_validate
from sklearn.metrics import confusion_matrix, accuracy_score


# Read CSV file #####
lsp = pd.read_csv('D:\Raj_kumar\Rajkumar\learninGit\dummy\FlaskApp\data\lsp.csv')
df = pd.read_excel('D:\Raj_kumar\Rajkumar\learninGit\dummy\FlaskApp\data\winequality-white.xlsx')

## Split the training and tesing datasets from main datasets
#test= lsp.iloc[11:16,1:10] 
#train = lsp.iloc[np.r_[1:11,16:21],3:10]
X,y = df.iloc[:,1:11], df.iloc[:,11]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


## import support vector machine #####
from sklearn.svm import SVC
parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
svc= SVC()
## gridsearchCV & cross_validate
clf = GridSearchCV(svc, parameters, cv=3)
#svc.fit(train.iloc[:,0:6],train.iloc[:,6])
clf.fit(X_train, y_train)
#pred = svc.predict(test.iloc[:,2:8])
pred = clf.predict(X_test)


## confusion matrix
confusion_matrix(y_test, pred)
tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()

## precision & recall of true positive
precision = tp / (tp + fp)
recall = tp / (tp + fn)

## precision & recall of true negative
precision = tn / (tn + fn)
recall = tn / (tn + fp)

## accuracy of model
accuracy_score(y_test, pred)*100


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

