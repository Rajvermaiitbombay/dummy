# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:46:59 2019

@author: Rajkumar
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.feature_selection import SelectKBest, chi2, RFE
from sklearn.linear_model import LogisticRegression 
import statsmodels.api as sm
from sklearn.svm import SVC
data_dir = os.getcwd()
train = pd.read_csv('bank-additional-full.csv', sep=';')
test = pd.read_csv('bank-additional.csv', sep=';')

# data summarization ###
def summary(df):
    print('--- Description of numerical variables')
    print(df.describe())
    print('--- Description of categorical variables')
    print(df.describe(include=['object']))
    print('--- Gerenal information about variables')
    print(df.info())
    print('--- view the 5 rows of dataset')
    print(df.head(5))
    return None

summary(train)

# outlier detection & treatment ###
def detect_outliers(col):
    outlier1 = []
    threshold = 3
    mean = np.mean(col)
    std =np.std(col)
    for i in col:
        z_score = (i - mean)/std 
        if np.abs(z_score) > threshold:
            outlier1.append(i)
    outlier2 = []
    sorted(col)
    q1, q3 = np.percentile(col,[25,75])
    iqr = q3 - q1
    lower_bound = q1 -(1.5 * iqr) 
    upper_bound = q3 +(1.5 * iqr)
    for i in col:
        if ((i > upper_bound) | (i < lower_bound)):
            outlier2.append(i)
    lst1 = np.unique(outlier1)
    lst2 = np.unique(outlier2)
    output = list(set(lst1) & set(lst2))
    return output 

# treat outliers ###
def treat_outliers(df):
	df = df.apply(lambda x: x.replace(detect_outliers(x), x.median())
				  if(x.dtypes != object) else x)
	return df

train = treat_outliers(train)
test = treat_outliers(test)

# feature engineering ##
def featureEngineering(dataset):
    labelencoder_x = LabelEncoder()
    for i in list(dataset.columns):
        if dataset[i].dtypes == object:
            dataset[i] = labelencoder_x.fit_transform(dataset[i])
        else:
            pass
    return None

featureEngineering(train)
featureEngineering(test)

# Feature Selection using 3 techniques ###

def Feature_selection(x,y):
    #Backward Elimination
    cols = list(x.columns)
    pmax = 1
    while (len(cols)>0):
        p= []
        X_1 = x[cols]
        X_1 = sm.add_constant(X_1)
        model = sm.OLS(y,X_1).fit()
        p = pd.Series(model.pvalues.values[1:],index = cols)      
        pmax = max(p)
        feature_with_p_max = p.idxmax()
        if(pmax>0.05):
            cols.remove(feature_with_p_max)
        else:
            break
    print('selected_features_set1:' + str(cols))
    
    # using statistics method
    x = x.drop(['cons.conf.idx','emp.var.rate'], 1)
    X_new = SelectKBest(chi2, k=15).fit_transform(x, y)
    cols = X_new.columns
    print('selected_features_set2:' + str(cols))
    
    # Recursive Feature Elimination
    model = LogisticRegression()
    rfe = RFE(model, 6)
    fit = rfe.fit(x, y)
    print("Feature Ranking: %s" % (fit.ranking_))
    return None

# selected set of columns from 3 feature selection techniques ##
    
set1 = ['marital','default','contact','previous', 'poutcome', 'emp.var.rate','cons.conf.idx', 'euribor3m','day_of_week']
set2 = ['age', 'marital', 'education', 'default', 'contact', 'month', 'day_of_week', 'duration', 'campaign', 'pdays', 'poutcome', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']
set3 = ['age','education', 'default','duration', 'campaign','pdays','previous','euribor3m', 'nr.employed']
selected_features = ['age','education', 'default','duration', 'campaign','pdays','previous','euribor3m', 'nr.employed', 'cons.conf.idx', 'emp.var.rate', 'y']

train = train[selected_features]
test = test[selected_features]

### Split the features and target variable from datasets

train_X, train_y = train.iloc[:,0:11], train.iloc[:,11]
test_X, test_y = test.iloc[:,0:11], test.iloc[:,11]

## import support vector machine #####

def Gridsearch_SVM(model):
    parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],'C': [1, 10, 100, 1000]},
						{'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
## gridsearchCV & cross_validate
    grid = GridSearchCV(model, parameters, cv=2)
    grid_result = grid.fit(train_X, train_y)
# summarize results
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, stdev, param))
    return None

# run gridsearch function to find the optimum value of model parameters
model = SVC()
Gridsearch_SVM(model)

model = SVC(kernel='linear', C=10)
model.fit(train_X, train_y)
predictions = model.predict(test_X)

## Accuracy of model
acc = accuracy_score(predictions, test_y)
print("model accuracy: {} %".format(round(acc*100, 2)))
## Confusion matrix
confusion_matrix(predictions, test_y)


